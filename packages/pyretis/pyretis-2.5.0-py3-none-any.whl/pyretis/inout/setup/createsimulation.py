# -*- coding: utf-8 -*-
# Copyright (c) 2019, PyRETIS Development Team.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""This module handles the creation of simulations from settings.

The different simulations are defined as objects which inherit
from the base :py:class:`.Simulation` class defined in
:py:mod:`pyretis.simulation.simulation`. Here, we are treating
each simulation with a special case.

Important methods defined here
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

create_simulation (:py:func:`.create_simulation`)
    Method for creating a simulation object from settings.

"""
import logging
from pyretis.core.random_gen import create_random_generator
from pyretis.simulation.md_simulation import (
    SimulationNVE,
    SimulationMDFlux,
    SimulationMD,
)
from pyretis.simulation.mc_simulation import UmbrellaWindowSimulation
from pyretis.simulation.path_simulation import (
    SimulationSingleTIS,
    SimulationRETIS,
)
from pyretis.core.pathensemble import (
    get_path_ensemble_class,
)
from pyretis.inout.setup.common import create_orderparameter
from pyretis.inout.settings import copy_settings
logger = logging.getLogger(__name__)  # pylint: disable=invalid-name
logger.addHandler(logging.NullHandler())


__all__ = ['create_simulation']


def create_path_ensemble(settings, ensemble_type):
    """Create a single path ensemble from simulation settings.

    Parameters
    ----------
    settings : dict
        This dict contains the settings needed to create the path
        ensemble.
    ensemble_type : string
        The kind of ensemble we are creating. This is typically defined
        by the engine.

    Returns
    -------
    out : object like :py:class:`.PathEnsemble`
        An object that can be used as a path ensemble in simulations.

    """
    interfaces = settings['simulation']['interfaces']
    exe_dir = settings['simulation'].get('exe-path', '')
    if len(interfaces) != 3:
        msgtxt = ('Wrong number of interfaces given for a TIS simulation. '
                  'Expected 3, got {}. Maybe you need task = "tis-multiple" '
                  'or "retis"').format(len(interfaces))
        raise ValueError(msgtxt)
    if 'detect' not in settings['tis']:
        detect = interfaces[-1]
        logger.warning(
            ('Detect interface not specified for the ensemble.'
             ' Using the "product" interface: %s'), detect
        )
    else:
        detect = settings['tis']['detect']
    if 'ensemble_number' not in settings['tis']:
        ensemble_name = 1
        logger.warning(
            ('Ensemble name not specified, '
             'using default ensemble "%s"'), ensemble_name
        )
    else:
        if settings['tis']['ensemble_number'] is None:
            ensemble_name = 1
            logger.warning(
                ('Ensemble name not specified, '
                 'using default ensemble "%s"'), ensemble_name
            )
        else:
            ensemble_name = int(settings['tis']['ensemble_number'])
    klass = get_path_ensemble_class(ensemble_type)
    return klass(ensemble_name, interfaces,
                 detect=detect, exe_dir=exe_dir)


def create_path_ensembles(interfaces, ensemble_type, include_zero=False,
                          exe_dir=None, zero_left='-inf'):
    """Create set set of path ensembles.

    This function will create and return a set of objects representing
    path ensembles for a given set of interfaces. This is useful when
    setting up TIS/RETIS simulations. Here we assume that the given
    interfaces define the path ensembles as follows:
    ``[0^-] | [0^+] | [1^+] | ... | [(n-1)^+] | state B``, where ``|``
    is the specified interface locations in the input `interfaces`.
    We assume that the reactant is to the left of `interfaces[0]` and
    that the product is to the right of `interfaces[-1]`. Given ``n``
    interfaces we generate ``n`` or ``n-1`` path ensembles, the former
    if we include the [0^-] ensemble.

    Parameters
    ----------
    interfaces : list of floats
        The interfaces we use to create path ensembles.
        ``interfaces[i]`` separates the [(i-1)^+] and [i^+] interfaces.
    ensemble_type : string
        The kind of ensemble we are creating. This is typically defined
        by the engine.
    include_zero : boolean, optional
        If `include_zero` is True, we include the [0^-] path ensemble.
    exe_dir : string, optional
        This string can be used to tell the path ensemble object
        where it is executed and where it can store files.
    zero_left : float, optional
        This defines the position of left interface of the {0^-} interface
        Default is -inf

    Returns
    -------
    ensembles : list of objects like :py:class:`.PathEnsemble`
        The generated path ensemble objects.
    detect : list of floats
        These are interfaces that can be used for an analysis, i.e. for
        detection and matching of probabilities.

    """
    detect = []
    ensembles = []
    reactant = interfaces[0]
    product = interfaces[-1]
    klass = get_path_ensemble_class(ensemble_type)
    if include_zero:
        interface = [float(zero_left), reactant, reactant]
        path_ensemble = klass(0, interface, detect=None, exe_dir=exe_dir)
        ensembles.append(path_ensemble)
    for i, middle in enumerate(interfaces[:-1]):
        interface = [reactant, middle, product]
        try:
            detect.append(interfaces[i+1])
        except IndexError:
            detect.append(product)
        path_ensemble = klass(i + 1, interface, detect=detect[-1],
                              exe_dir=exe_dir)
        ensembles.append(path_ensemble)
    return ensembles, detect


def create_nve_simulation(settings, system, engine):
    """Set up and create a NVE simulation.

    Parameters
    ----------
    settings : dict
        The settings needed to set up the simulation.
    system : object like :py:class:`.System`
        The system we are going to simulate.
    engine : object like :py:class:`.EngineBase`
        The engine to use for the simulation.

    Returns
    -------
    out : object like :py:class:`.SimulationNVE`
        The object representing the simulation to run.

    """
    sim = settings['simulation']
    order_function = create_orderparameter(settings)
    for key in ('steps',):
        if key not in sim:
            msgtxt = 'Simulation setting "{}" is missing!'.format(key)
            logger.critical(msgtxt)
            raise ValueError(msgtxt)
    return SimulationNVE(system, engine,
                         order_function=order_function,
                         steps=sim['steps'],
                         startcycle=sim.get('startcycle', 0))


def create_md_simulation(settings, system, engine):
    """Set up and create a generic MD simulation.

    Parameters
    ----------
    settings : dict
        The settings needed to set up the simulation.
    system : object like :py:class:`.System`
        The system we are going to simulate.
    engine : object like :py:class:`.EngineBase`
        The engine to use for the simulation.

    Returns
    -------
    out : object like :py:class:`.SimulationMD`
        The object representing the simulation to run.

    """
    sim = settings['simulation']
    order_function = create_orderparameter(settings)
    for key in ('steps',):
        if key not in sim:
            msgtxt = 'Simulation setting "{}" is missing!'.format(key)
            logger.critical(msgtxt)
            raise ValueError(msgtxt)
    return SimulationMD(system, engine,
                        order_function=order_function,
                        steps=sim['steps'],
                        startcycle=sim.get('startcycle', 0))


def create_mdflux_simulation(settings, system, engine):
    """Set up and create a MD FLUX simulation.

    Parameters
    ----------
    settings : dict
        The settings needed to set up the simulation.
    system : object like :py:class:`.System`
        The system we are going to simulate.
    engine : object like :py:class:`.EngineBase`
        The engine to use for the simulation.

    Returns
    -------
    out : object like :py:class:`.SimulationMDFlux`
        The object representing the simulation to run.

    """
    order_function = create_orderparameter(settings)
    engine.can_use_order_function(order_function)
    sim = settings['simulation']
    for key in ('steps', 'interfaces'):
        if key not in sim:
            msgtxt = 'Simulation setting "{}" is missing!'.format(key)
            logger.critical(msgtxt)
            raise ValueError(msgtxt)
    return SimulationMDFlux(system, order_function, engine,
                            sim['interfaces'],
                            steps=sim['steps'],
                            startcycle=sim.get('startcycle', 0))


def create_umbrellaw_simulation(settings, system):
    """Set up and create a Umbrella Window simulation.

    Parameters
    ----------
    settings : dict
        The settings needed to set up the simulation.
    system : object like :py:class:`.System`
        The system we are going to simulate.

    Returns
    -------
    out : object like :py:class:`.UmbrellaWindowSimulation`
        The object representing the simulation to run.

    """
    sim = settings['simulation']
    rgen = create_random_generator(sim)
    for key in ('umbrella', 'over', 'maxdx', 'mincycle'):
        if key not in sim:
            msgtxt = 'Simulation setting "{}" is missing!'.format(key)
            logger.critical(msgtxt)
            raise ValueError(msgtxt)
    return UmbrellaWindowSimulation(system, sim['umbrella'],
                                    sim['over'],
                                    sim['maxdx'],
                                    rgen=rgen,
                                    mincycle=sim['mincycle'],
                                    startcycle=sim.get('startcycle', 0))


def create_tis_simulations(settings, system, engine):
    """Set up and create a series of TIS simulations.

    This method will for each interface set up a single TIS simulation.
    These simulations can then be run in series, parallel or written
    out as settings files that PyRETIS can run.

    Parameters
    ----------
    settings : dict
        The settings needed to set up the simulation.
    system : object like :py:class:`.System`
        The system we are going to simulate.
    engine : object like :py:class:`.EngineBase`
        The engine to use for the simulation.

    Returns
    -------
    sim_settings : list of dicts
        `sim_settings[i]` is a dictionary with settings for running
        simulation i. Note that the actual simulation object is not
        created here.

    """
    sim_settings = []
    interfaces = settings['simulation']['interfaces']
    reactant = interfaces[0]
    product = interfaces[-1]
    if settings['simulation']['task'] == 'tis':
        return _create_tis_single_simulation(settings, system, engine)
    for i, middle in enumerate(interfaces[:-1]):
        lsetting = copy_settings(settings)
        lsetting['simulation']['task'] = 'tis'
        lsetting['simulation']['interfaces'] = [reactant, middle, product]
        lsetting['tis']['ensemble_number'] = i + 1
        try:
            lsetting['tis']['detect'] = interfaces[i + 1]
        except IndexError:
            lsetting['tis']['detect'] = product
        sim_settings.append(lsetting)
    return sim_settings


def _create_tis_single_simulation(settings, system, engine):
    """Set up and create a single TIS simulation.

    Parameters
    ----------
    settings : dict
        The settings needed to set up the simulation.
    system : object like :py:class:`.System`
        The system we are integrating.
    engine : object like :py:class`.EngineBase`
        The engine to use for the simulation.

    Returns
    -------
    out : object like :py:class:`.SimulationSingleTIS`
        The object representing the simulation to run.

    """
    order_function = create_orderparameter(settings)
    engine.can_use_order_function(order_function)
    path_ensemble = create_path_ensemble(settings, engine.engine_type)
    rgen = create_random_generator(settings['tis'])
    sim = settings['simulation']
    for key in ('steps',):
        if key not in sim:
            msgtxt = 'Simulation setting "{}" is missing!'.format(key)
            logger.critical(msgtxt)
            raise ValueError(msgtxt)
    return SimulationSingleTIS(system, order_function, engine,
                               path_ensemble,
                               settings,
                               rgen=rgen,
                               steps=sim['steps'],
                               startcycle=sim.get('startcycle', 0))


def create_retis_simulation(settings, system, engine):
    """Set up and create a RETIS simulation.

    Parameters
    ----------
    settings : dict
        The settings needed to set up the simulation.
    system : object like :py:class:`.System`
        The system we are going to simulate.
    engine : object like :py:class:`.EngineBase`
        The engine to use for the simulation.

    Returns
    -------
    out : object like :py:class:`.SimulationRETIS`
        The object representing the simulation to run.

    """
    order_function = create_orderparameter(settings)
    engine.can_use_order_function(order_function)
    sim = settings['simulation']
    exe_dir = sim.get('exe-path', '')
    zero_left = sim.get('zero_left', '-inf')
    path_ensembles, _ = create_path_ensembles(sim['interfaces'],
                                              engine.engine_type,
                                              include_zero=True,
                                              exe_dir=exe_dir,
                                              zero_left=zero_left
                                              )
    rgen = create_random_generator(settings['tis'])
    for key in ('steps',):
        if key not in sim:
            msgtxt = 'Simulation setting "{}" is missing!'.format(key)
            logger.critical(msgtxt)
            raise ValueError(msgtxt)
    return SimulationRETIS(system, order_function, engine,
                           path_ensembles,
                           settings,
                           rgen=rgen,
                           steps=sim['steps'],
                           startcycle=sim.get('startcycle', 0))


def create_simulation(settings, kwargs):
    """Create simulation(s) from given settings.

    This function will set up some common simulation types.
    It is meant as a helper function to automate some very common set-up
    task. It will here check what kind of simulation we are to perform
    and then call the appropriate function for setting that type of
    simulation up.

    Parameters
    ----------
    settings : dict
        This dictionary contains the settings for the simulation.
    kwargs : dict
        This dict contains objects that might be needed to initialise
        the simulation for instance:

        * system : object like :py:class:`.System`
            This is the system for which the simulation will run.

        * engine : object like :py:class:`.EngineBase`
            The engine to use for the simulation.

    Returns
    -------
    out : object like :py:class:`.Simulation`
        This object will correspond to the selected simulation type.

    """
    sim_type = settings['simulation']['task'].lower()

    sim_map = {
        'md': {'function': create_md_simulation,
               'args': ('system', 'engine')},
        'md-nve': {'function': create_nve_simulation,
                   'args': ('system', 'engine')},
        'md-flux': {'function': create_mdflux_simulation,
                    'args': ('system', 'engine')},
        'umbrellawindow': {'function': create_umbrellaw_simulation,
                           'args': ('system',)},
        'tis': {'function': create_tis_simulations,
                'args': ('system', 'engine')},
        'tis-multiple': {'function': create_tis_simulations,
                         'args': ('system', 'engine')},
        'retis': {'function': create_retis_simulation,
                  'args': ('system', 'engine')}
    }

    if sim_type not in sim_map:
        msgtxt = 'Unknown simulation task {}'.format(sim_type)
        logger.error(msgtxt)
        raise ValueError(msgtxt)
    else:
        function = sim_map[sim_type]['function']
        arg_name = sim_map[sim_type]['args']
        args = []
        msgtxt = 'Simulation "{}" requires a "{}"'
        for key in arg_name:
            if key not in kwargs or kwargs[key] is None:
                msg = msgtxt.format(sim_type, key)
                logger.error(msg)
                raise ValueError(msg)
            else:
                args.append(kwargs[key])
        simulation = function(settings, *args)
        if isinstance(simulation, list):
            msgtxt = sim_type
        else:
            msgtxt = '{}'.format(simulation)
        logger.info('Created simulation:\n%s', msgtxt)
        return simulation
