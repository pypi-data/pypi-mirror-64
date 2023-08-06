# -*- coding: utf-8 -*-
# Copyright (c) 2019, PyRETIS Development Team.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""Definition of the OpenMM engine.

This module defines the class for the OpenMM MD engine.

Important classes defined here
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

OpenMMEngine (:py:class:`.OpenMMEngine`)
    The class for running the OpenMM engine.

"""

import logging
from pyretis.core.particlefunctions import (calculate_kinetic_energy,
                                            reset_momentum)
from pyretis.engines.engine import EngineBase
from pyretis.core.box import box_matrix_to_list
try:
    from simtk import openmm
    HAS_OPENMM = True
except ImportError:
    HAS_OPENMM = False

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name
logger.addHandler(logging.NullHandler())

__all__ = ['OpenMMEngine']


class OpenMMEngine(EngineBase):
    """
    A class for interfacing with OpenMM.

    This class defines the interface to OpenMM.

    Attributes
    ----------
    simulation: OpenMM.simulation
        OpenMM simulation object.

    subcyles: int
        Number of OpenMM steps per PyRETIS step.

    """

    engine_type = 'openmm'

    def __init__(self, simulation, subcycles=1):
        """Set up the OpenMM Engine.

        Parameters
        ----------
        simulation : OpenMM.simulation
            The OpenMM simulation object.

        subcycles: int
            Number of OpenMM integration steps per PyRETIS step.

        """
        # Check if openmm is installed.
        if HAS_OPENMM is False:
            raise RuntimeError("OpenMM is not installed")
        super(OpenMMEngine, self).__init__(description='OpenMM')

        self.simulation = simulation
        self.subcycles = subcycles

    def calculate_order(self, order_function, system,
                        xyz=None, vel=None, box=None):
        """Return the order parameter.

        This method is just to help to calculate the order parameter
        in cases where only the engine can do it.

        Parameters
        ----------
        order_function : object like :py:class:`.OrderParameter`
            The object used for calculating the order parameter(s).
        system : object like :py:class:`.System`
            The system containing the current positions and velocities.
        xyz : numpy.array, optional
            The positions to use. Typically for internal engines, this
            is not needed. It is included here as it can be used for
            testing and also to be compatible with the generic function
            defined by the parent.
        vel : numpy.array, optional
            The velocities to use.
        box : numpy.array, optional
            The current box vectors.

        Returns
        -------
        out : list of floats
            The calculated order parameter(s).

        """
        if any((xyz is None, vel is None, box is None)):
            return order_function.calculate(system)
        system.particles.pos = xyz
        system.particles.vel = vel
        system.box.update_size(box)
        return order_function.calculate(system)

    def clean_up(self):
        """Clean up after using the engine.

        Currently, this is only included for compatibility with external
        integrators.

        """
        return

    def dump_phasepoint(self, phasepoint, deffnm=None):
        """For compatibility with external integrators."""
        return

    def integration_step(self, system):
        """Perform one integration step of n subcycles.

        Parameters
        ----------
        system : object like :py:class:`.System`
            The system to integrate/act on. Assumed to have a particle
            list in ``system.particles``.

        Returns
        -------
        out : None
            Does not return anything, but alters the state of the given
            system.

        """
        particles = system.particles
        pos = particles.pos
        vel = particles.vel
        box = system.box
        context = self.simulation.context

        # Update the simulation to the correct system:
        context.setPositions(pos)
        context.setVelocities(vel)

        # PyRETIS matrix.T is openmm boxvectors:
        if box is not None:
            vectors = list(box.box_matrix.T)
            context.setPeriodicBoxVectors(*vectors)

        # Run the simulation for n subcycles:
        self.simulation.step(self.subcycles)

        # Get the current state:
        state = context.getState(getPositions=True, getVelocities=True)

        # Update system:
        system.particles.pos = state.getPositions(asNumpy=True)
        system.particles.vel = state.getVelocities(asNumpy=True)
        if box is not None:
            box.update_size(
                box_matrix_to_list(state.getPeriodicBoxVectors(asNumpy=True).T)
            )

    def kick_across_middle(self, system, order_function, rgen, middle,
                           tis_settings):
        """Force a phase point across the middle interface.

        This is accomplished by repeatedly kicking the phase point so
        that it crosses the middle interface.

        Parameters
        ----------
        system : object like :py:class:`.System`
            This is the system that contains the particles we are
            investigating.
        order_function : object like :py:class:`.OrderParameter`
            The object used for calculating the order parameter.
        rgen : object like :py:class:`.RandomGenerator`
            This is the random generator that will be used.
        middle : float
            This is the value for the middle interface.
        tis_settings : dict
            This dictionary contains settings for TIS. Explicitly used here:

            * `zero_momentum`: boolean, determines if the momentum is zeroed.
            * `rescale_energy`: boolean, determines if energy is re-scaled.


        Returns
        -------
        out[0] : object like :py:class:`.System`
            The phase-point just before the interface.
        out[1] : object like :py:class:`.System`
            The phase-point just after the interface.

        Note
        ----
        This function will update the system state.

        """
        # Taken from MDEngine in internal.py
        # We search for crossing with the middle interface and do this
        # by sequentially kicking the initial phase point:
        previous = None
        curr = self.calculate_order(order_function, system)[0]
        while True:
            # Save current state:
            previous = system.copy()
            # Save previous box matrix:
            prev_box = system.box.box_matrix
            # Modify velocities:
            self.modify_velocities(system,
                                   rgen,
                                   sigma_v=None,
                                   aimless=True,
                                   momentum=tis_settings['zero_momentum'],
                                   rescale=tis_settings['rescale_energy'])
            # Update order parameter in case it is velocity dependent:
            curr = self.calculate_order(order_function, system)[0]
            previous.order = curr
            # Store modified velocities:
            previous.particles.set_vel(system.particles.get_vel())
            # Integrate forward one step:
            self.integration_step(system)
            # Compare previous order parameter and the new one:
            prev = curr
            curr = self.calculate_order(order_function, system)[0]
            if (prev < middle < curr) or (curr < middle < prev):
                # Middle interface was crossed, just stop the loop.
                logger.info('Crossing found: %9.6f %9.6f ', prev, curr)
                break
            elif (prev <= curr <= middle) or (middle <= curr <= prev):
                # We are getting closer, keep the new point.
                pass
            elif prev == middle:
                # Unlucky case, we want more than 1 point, so search more.
                pass
            else:  # We did not get closer, fall back to previous point.
                system.particles = previous.particles.copy()
                system.box.update_size(box_matrix_to_list(prev_box))
                curr = previous.order
        return previous, system

    def modify_velocities(self, system, rgen, sigma_v=None, aimless=True,
                          momentum=False, rescale=None):
        """Modify the velocities of the current state.

        This method will modify the velocities of a time slice.
        And it is part of the integrator since it, conceptually,
        fits here:  we are acting on the system and modifying it.

        Parameters
        ----------
        system : object like :py:class:`.System`
            The system is used here since we need access to the particle
            list.
        rgen : object like :py:class:`.RandomGenerator`
            This is the random generator that will be used.
        sigma_v : numpy.array, optional
            These values can be used to set a standard deviation (one
            for each particle) for the generated velocities.
        aimless : boolean, optional
            Determines if we should do aimless shooting or not.
        momentum : boolean, optional
            If True, we reset the linear momentum to zero after generating.
        rescale : float, optional
            In some NVE simulations, we may wish to re-scale the energy to
            a fixed value. If `rescale` is a float > 0, we will re-scale
            the energy (after modification of the velocities) to match the
            given float.

        Returns
        -------
        dek : float
            The change in the kinetic energy.
        kin_new : float
            The new kinetic energy.

        """
        particles = system.particles
        if rescale is not None and rescale is not False:
            if rescale > 0:
                kin_old = rescale - particles.vpot
                do_rescale = True
            else:
                logger.warning('Ignored re-scale 6.2%f < 0.0.', rescale)
                return 0.0, calculate_kinetic_energy(particles)[0]
        else:
            kin_old = calculate_kinetic_energy(particles)[0]
            do_rescale = False
        if aimless:
            vel, _ = rgen.draw_maxwellian_velocities(system=system)
            particles.vel = vel
        else:  # Soft velocity change, from a Gaussian distribution:
            dvel, _ = rgen.draw_maxwellian_velocities(system=system,
                                                      sigma_v=sigma_v)
            particles.vel = particles.vel + dvel
        if momentum:
            reset_momentum(particles)
        if do_rescale:
            system.rescale_velocities(rescale)
        kin_new = calculate_kinetic_energy(particles)[0]
        dek = kin_new - kin_old
        return dek, kin_new

    def propagate(self, path, initial_system, order_function, interfaces,
                  reverse=False):
        """Generate a path by integrating until a criterion is met.

        This function will generate a path by calling the function
        specifying the integration step repeatedly. The integration is
        carried out until the order parameter has passed the specified
        interfaces or if we have integrated for more than a specified
        maximum number of steps. The given system defines the initial
        state and the system is reset to its initial state when this
        method is done.

        Parameters
        ----------
        path : object like :py:class:`.PathBase`
            This is the path we use to fill in phase-space points.
            We are here not returning a new path - this since we want
            to delegate the creation of the path (type) to the method
            that is running `propagate`.
        initial_system : object like :py:class:`.System`
            The system object gives the initial state for the
            integration. The initial state is stored and the system is
            reset to the initial state when the integration is done.
        order_function : object like :py:class:`.OrderParameter`
            The object used for calculating the order parameter.
        interfaces : list of floats
            These interfaces define the stopping criterion.
        reverse : boolean, optional
            If True, the system will be propagated backward in time.

        Returns
        -------
        success : boolean
            This is True if we generated an acceptable path.
        status : string
            A text description of the current status of the propagation.

        """
        status = 'Propagate w/OpenMM engine'
        logger.debug(status)
        success = False
        system = initial_system.copy()
        left, _, right = interfaces
        for i in range(path.maxlen):
            order = self.calculate_order(order_function, system)
            kin = calculate_kinetic_energy(system.particles)[0]
            snapshot = {'order': order,
                        'pos': system.particles.pos,
                        'vel': system.particles.vel,
                        'box': system.box,
                        'ekin': kin,
                        'vpot': None}
            phasepoint = self.snapshot_to_system(system, snapshot)
            status, success, stop, _ = self.add_to_path(path, phasepoint,
                                                        left, right)
            if stop:
                logger.debug('Stopping propagate at step: %i ', i)
                break

            if reverse:
                system.particles.vel *= -1.0
                self.integration_step(system)
                system.particles.vel *= -1.0
            else:
                self.integration_step(system)
        logger.debug('Propagate done: "%s" (success: %s)', status, success)
        return success, status
