# -*- coding: utf-8 -*-
# Copyright (c) 2019, PyRETIS Development Team.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""A CP2K external MD integrator interface.

This module defines a class for using CP2K as an external engine.

Important classes defined here
------------------------------

CP2KEngine (:py:class:`.CP2KEngine`)
    A class responsible for interfacing CP2K.
"""
import logging
import os
import re
import shlex
from pyretis.engines.external import ExternalMDEngine
from pyretis.core.random_gen import create_random_generator
from pyretis.inout.formats.xyz import (
    read_xyz_file,
    write_xyz_trajectory,
    convert_snapshot
)
from pyretis.inout.formats.cp2k import (
    update_cp2k_input,
    read_cp2k_restart,
    read_cp2k_box,
    read_cp2k_energy,
)
logger = logging.getLogger(__name__)  # pylint: disable=invalid-name
logger.addHandler(logging.NullHandler())


OUTPUT_FILES = {
    'energy': '{}-1.ener',
    'restart': '{}-1.restart',
    'pos': '{}-pos-1.xyz',
    'vel': '{}-vel-1.xyz',
    'wfn': '{}-RESTART.wfn',
    'wfn-bak': '{}-RESTART.wfn.bak-'
}


REGEXP_BACKUP = re.compile(r'\.bak-\d$')


def write_for_step_vel(infile, outfile, timestep, subcycles, posfile, vel,
                       name='md_step', print_freq=None):
    """Create input file for a single step.

    Note, the single step actually consists of a number of subcycles.
    But from PyRETIS' point of view, this is a single step.
    Further, we here assume that we start from a given xyz file and
    we also explicitly give the velocities here.

    Parameters
    ----------
    infile : string
        The input template to use.
    outfile : string
        The file to create.
    timestep : float
        The time-step to use for the simulation.
    subcycles : integer
        The number of sub-cycles to perform.
    posfile : string
        The (base)name for the input file to read positions from.
    vel : numpy.array
        The velocities to set in the input.
    name : string, optional
        A name for the CP2K project.
    print_freq : integer, optional
        How often we should print to the trajectory file.

    """
    if print_freq is None:
        print_freq = subcycles
    to_update = {
        'GLOBAL': {
            'data': ['PROJECT {}'.format(name),
                     'RUN_TYPE MD',
                     'PRINT_LEVEL LOW'],
            'replace': True,
        },
        'MOTION->MD':  {
            'data': {'STEPS': subcycles,
                     'TIMESTEP': timestep}
        },
        'MOTION->PRINT->RESTART': {
            'data': ['BACKUP_COPIES 0'],
            'replace': True,
        },
        'MOTION->PRINT->RESTART->EACH': {
            'data': {'MD': print_freq}
        },
        'MOTION->PRINT->VELOCITIES->EACH': {
            'data': {'MD': print_freq}
        },
        'MOTION->PRINT->TRAJECTORY->EACH': {
            'data': {'MD': print_freq}
        },
        'FORCE_EVAL->SUBSYS->TOPOLOGY': {
            'data': {'COORD_FILE_NAME': posfile,
                     'COORD_FILE_FORMAT': 'xyz'}
        },
        'FORCE_EVAL->SUBSYS->VELOCITY': {
            'data': [],
            'replace': True,
        },
        'FORCE_EVAL->DFT->SCF->PRINT->RESTART': {
            'data': ['BACKUP_COPIES 0'],
            'replace': True,
        },
    }
    for veli in vel:
        to_update['FORCE_EVAL->SUBSYS->VELOCITY']['data'].append(
            '{} {} {}'.format(*veli)
        )
    remove = [
        'EXT_RESTART',
        'FORCE_EVAL->SUBSYS->COORD'
    ]
    update_cp2k_input(infile, outfile, update=to_update, remove=remove)


def write_for_integrate(infile, outfile, timestep, subcycles, posfile,
                        name='md_step', print_freq=None):
    """Create input file for a single step for the integrate method.

    Here, we do minimal changes and just set the time step and subcycles
    and the starting configuration.

    Parameters
    ----------
    infile : string
        The input template to use.
    outfile : string
        The file to create.
    timestep : float
        The time-step to use for the simulation.
    subcycles : integer
        The number of sub-cycles to perform.
    posfile : string
        The (base)name for the input file to read positions from.
    name : string, optional
        A name for the CP2K project.
    print_freq : integer, optional
        How often we should print to the trajectory file.

    """
    if print_freq is None:
        print_freq = subcycles
    to_update = {
        'GLOBAL': {
            'data': ['PROJECT {}'.format(name),
                     'RUN_TYPE MD',
                     'PRINT_LEVEL LOW'],
            'replace': True,
        },
        'MOTION->MD':  {
            'data': {'STEPS': subcycles,
                     'TIMESTEP': timestep}
        },
        'MOTION->PRINT->RESTART': {
            'data': ['BACKUP_COPIES 0'],
            'replace': True,
        },
        'MOTION->PRINT->RESTART->EACH': {
            'data': {'MD': print_freq}
        },
        'MOTION->PRINT->VELOCITIES->EACH': {
            'data': {'MD': print_freq}
        },
        'MOTION->PRINT->TRAJECTORY->EACH': {
            'data': {'MD': print_freq}
        },
        'FORCE_EVAL->SUBSYS->TOPOLOGY': {
            'data': {'COORD_FILE_NAME': posfile,
                     'COORD_FILE_FORMAT': 'xyz'}
        },
        'FORCE_EVAL->DFT->SCF->PRINT->RESTART': {
            'data': ['BACKUP_COPIES 0'],
            'replace': True,
        },
    }
    remove = [
        'EXT_RESTART',
        'FORCE_EVAL->SUBSYS->COORD'
    ]
    update_cp2k_input(infile, outfile, update=to_update, remove=remove)


def write_for_continue(infile, outfile, timestep, subcycles,
                       name='md_continue'):
    """
    Create input file for a single step.

    Note, the single step actually consists of a number of subcycles.
    But from PyRETIS' point of view, this is a single step.
    Here, we make use of restart files named ``previous.restart``
    and ``previous.wfn`` to continue a run.

    Parameters
    ----------
    infile : string
        The input template to use.
    outfile : string
        The file to create.
    timestep : float
        The time-step to use for the simulation.
    subcycles : integer
        The number of sub-cycles to perform.
    name : string, optional
        A name for the CP2K project.

    """
    to_update = {
        'GLOBAL': {
            'data': ['PROJECT {}'.format(name),
                     'RUN_TYPE MD',
                     'PRINT_LEVEL LOW'],
            'replace': True,
        },
        'MOTION->MD':  {
            'data': {'STEPS': subcycles,
                     'TIMESTEP': timestep}
        },
        'MOTION->PRINT->RESTART': {
            'data': ['BACKUP_COPIES 0'],
            'replace': True,
        },
        'MOTION->PRINT->RESTART->EACH': {
            'data': {'MD': subcycles}
        },
        'MOTION->PRINT->VELOCITIES->EACH': {
            'data': {'MD': subcycles}
        },
        'MOTION->PRINT->TRAJECTORY->EACH': {
            'data': {'MD': subcycles}
        },
        'EXT_RESTART': {
            'data': ['RESTART_VEL',
                     'RESTART_POS',
                     'RESTART_FILE_NAME previous.restart'],
            'replace': True
        },
        'FORCE_EVAL->DFT': {
            'data': {'WFN_RESTART_FILE_NAME': 'previous.wfn'},
        },
        'FORCE_EVAL->DFT->SCF->PRINT->RESTART': {
            'data': ['BACKUP_COPIES 0'],
            'replace': True,
        },
    }
    remove = [
        'FORCE_EVAL->SUBSYS->TOPOLOGY',
        'FORCE_EVAL->SUBSYS->VELOCITY',
        'FORCE_EVAL->SUBSYS->COORD'
        'FORCE_EVAL->DFT->RESTART_FILE_NAME',
    ]
    update_cp2k_input(infile, outfile, update=to_update, remove=remove)


def write_for_genvel(infile, outfile, posfile, seed, name='genvel'):
    """Create input file for velocity generation.

    Parameters
    ----------
    infile : string
        The input template to use.
    outfile : string
        The file to create.
    posfile : string
        The (base)name for the input file to read positions from.
    seed : integer
        A seed for generating velocities.
    name : string, optional
        A name for the CP2K project.

    """
    to_update = {
        'GLOBAL': {
            'data': ['PROJECT {}'.format(name),
                     'SEED {}'.format(seed),
                     'RUN_TYPE MD',
                     'PRINT_LEVEL LOW'],
            'replace': True,
        },
        'FORCE_EVAL->DFT->SCF': {
            'data': {'SCF_GUESS': 'ATOMIC'}
        },
        'MOTION->MD':  {
            'data': {'STEPS': 1,
                     'TIMESTEP': 0}
        },
        'MOTION->PRINT->RESTART': {
            'data': ['BACKUP_COPIES 0'],
            'replace': True,
        },
        'MOTION->PRINT->RESTART->EACH': {
            'data': {'MD': 1}
        },
        'MOTION->PRINT->VELOCITIES->EACH': {
            'data': {'MD': 1}
        },
        'MOTION->PRINT->TRAJECTORY->EACH': {
            'data': {'MD': 1}
        },
        'FORCE_EVAL->SUBSYS->TOPOLOGY': {
            'data': {'COORD_FILE_NAME': posfile,
                     'COORD_FILE_FORMAT': 'xyz'}
        },
        'FORCE_EVAL->DFT->SCF->PRINT->RESTART': {
            'data': ['BACKUP_COPIES 0'],
            'replace': True,
        },
    }
    remove = [
        'EXT_RESTART',
        'FORCE_EVAL->SUBSYS->VELOCITY',
        'FORCE_EVAL->DFT->RESTART_FILE_NAME',
    ]
    update_cp2k_input(infile, outfile, update=to_update, remove=remove)


class CP2KEngine(ExternalMDEngine):
    """
    A class for interfacing CP2K.

    This class defines the interface to CP2K.

    Attributes
    ----------
    cp2k : string
        The command for executing CP2K.
    input_path : string
        The directory where the input files are stored.
    timestep : float
        The time step used in the CP2K MD simulation.
    subcycles : integer
        The number of steps each CP2K run is composed of.
    rgen : object like :py:class:`.RandomGenerator`
        An object we use to set seeds for velocity generation.
    extra_files : list
        List of extra files which may be required to run CP2K.

    """

    def __init__(self, cp2k, input_path, timestep, subcycles,
                 extra_files=None, seed=0):
        """Set up the CP2K engine.

        Parameters
        ----------
        cp2k : string
            The CP2K executable.
        input_path : string
            The path to where the input files are stored.
        timestep : float
            The time step used in the CP2K simulation.
        subcycles : integer
            The number of steps each CP2K run is composed of.
        extra_files : list
            List of extra files which may be required to run CP2K.
        seed : integer, optional
            A seed for the random number generator.
        extra_files : list
            List of extra files which may be required to run CP2K.

        """
        super().__init__('CP2K external engine', timestep,
                         subcycles)
        self.rgen = create_random_generator({'seed': seed})
        self.ext = 'xyz'
        self.cp2k = shlex.split(cp2k)
        logger.info('Command for execution of CP2K: %s', ' '.join(self.cp2k))
        # Store input path:
        self.input_path = os.path.abspath(input_path)
        # Store input files:
        input_files = {
            'conf': 'initial.xyz',
            'template': 'cp2k.inp',
        }
        self.input_files = self._look_for_input_files(
            self.input_path,
            input_files,
        )
        self.extra_files = {}
        if extra_files is not None:
            self.extra_files = self._look_for_input_files(
                self.input_path,
                {'file-{}'.format(i): val for i, val in enumerate(extra_files)}
            )

    def run_cp2k(self, input_file, proj_name):
        """
        Run the CP2K executable.

        Returns
        -------
        out : dict
            The files created by the run.

        """
        cmd = self.cp2k + ['-i', input_file]
        logger.debug('Executing CP2K %s: %s', proj_name, input_file)
        self.execute_command(cmd, cwd=self.exe_dir, inputs=None)
        out = {}
        for key, name in OUTPUT_FILES.items():
            out[key] = os.path.join(self.exe_dir, name.format(proj_name))
        return out

    def _extract_frame(self, traj_file, idx, out_file):
        """
        Extract a frame from a trajectory file.

        This method is used by `self.dump_config` when we are
        dumping from a trajectory file. It is not used if we are
        dumping from a single config file.

        Parameters
        ----------
        traj_file : string
            The trajectory file to dump from.
        idx : integer
            The frame number we look for.
        out_file : string
            The file to dump to.

        """
        for i, snapshot in enumerate(read_xyz_file(traj_file)):
            if i == idx:
                box, xyz, vel, names = convert_snapshot(snapshot)
                if os.path.isfile(out_file):
                    logger.warning('CP2K will overwrite %s', out_file)
                write_xyz_trajectory(out_file, xyz, vel, names, box,
                                     append=False)
                return
        logger.error('CP2K could not extract index %i from %s!',
                     idx, traj_file)

    def _name_output(self, basename):
        """Return the name of the output file."""
        out_file = '{}.{}'.format(basename, self.ext)
        return os.path.join(self.exe_dir, out_file)

    def _propagate_from(self, name, path, system, order_function, interfaces,
                        msg_file, reverse=False):
        """
        Propagate with CP2K from the current system configuration.

        Here, we assume that this method is called after the propagate()
        has been called in the parent. The parent is then responsible
        for reversing the velocities and also for setting the initial
        state of the system.

        Parameters
        ----------
        name : string
            A name to use for the trajectory we are generating.
        path : object like :py:class:`.PathBase`
            This is the path we use to fill in phase-space points.
        system : object like :py:class:`.System`
            The system object gives the initial state.
        order_function : object like :py:class:`.OrderParameter`
            The object used for calculating the order parameter.
        interfaces : list of floats
            These interfaces define the stopping criterion.
        msg_file : object like :py:class:`.FileIO`
            An object we use for writing out messages that are useful
            for inspecting the status of the current propagation.
        reverse : boolean, optional
            If True, the system will be propagated backward in time.

        Returns
        -------
        success : boolean
            This is True if we generated an acceptable path.
        status : string
            A text description of the current status of the
            propagation.

        """
        status = 'propagating with CP2K (reverse = {})'.format(reverse)
        logger.debug(status)
        success = False
        left, _, right = interfaces
        logger.debug('Adding input files for CP2K')
        # First, copy the required input files:
        self.add_input_files(self.exe_dir)
        # Get positions and velocities from the input file.
        initial_conf = system.particles.get_pos()[0]
        box, xyz, vel, atoms = self._read_configuration(initial_conf)
        if box is None:
            box, _ = read_cp2k_box(self.input_files['template'])
        # Add CP2K input for a single step:
        step_input = os.path.join(self.exe_dir, 'step.inp')
        write_for_step_vel(self.input_files['template'], step_input,
                           self.timestep, self.subcycles,
                           os.path.basename(initial_conf),
                           vel, name=name)
        # And create the input file for continuing:
        continue_input = os.path.join(self.exe_dir, 'continue.inp')
        write_for_continue(self.input_files['template'], continue_input,
                           self.timestep, self.subcycles, name=name)
        # Get the order parameter before the run:
        order = self.calculate_order(order_function, system,
                                     xyz=xyz, vel=vel, box=box)
        traj_file = os.path.join(self.exe_dir, '{}.{}'.format(name, self.ext))
        # Create a message file with some info about this run:
        msg_file.write(
            '# Initial order parameter: {}'.format(
                ' '.join(['{}'.format(i) for i in order])
            )
        )
        msg_file.write('# Trajectory file is: {}'.format(traj_file))
        # Run the first step:
        msg_file.write('# Running first CP2k step.')
        out_files = self.run_cp2k('step.inp', name)
        restart_file = os.path.join(self.exe_dir, out_files['restart'])
        prestart_file = os.path.join(self.exe_dir, 'previous.restart')
        wave_file = os.path.join(self.exe_dir, out_files['wfn'])
        pwave_file = os.path.join(self.exe_dir, 'previous.wfn')

        # Note: Order is calculated at the END of each iteration!
        i = 0
        # Write the config so we have a non-empty file:
        write_xyz_trajectory(traj_file, xyz, vel, atoms, box, step=i,
                             append=False)
        msg_file.write('# Running main CP2k propagation loop.')
        msg_file.write('# Step order parameter cv1 cv2 ...')
        for i in range(path.maxlen):
            msg_file.write(
                '{} {}'.format(i, ' '.join(['{}'.format(j) for j in order]))
            )
            snapshot = {'order': order, 'config': (traj_file, i),
                        'vel_rev': reverse}
            phase_point = self.snapshot_to_system(system, snapshot)
            status, success, stop, add = self.add_to_path(path, phase_point,
                                                          left, right)
            if add and i > 0:
                # Write the previous configuration:
                write_xyz_trajectory(traj_file, xyz, vel, atoms, box,
                                     step=i)
            if stop:
                logger.debug('CP2K propagation ended at %i. Reason: %s',
                             i, status)
                break
            if i == 0:
                pass
            elif i > 0:
                self._movefile(restart_file, prestart_file)
                self._movefile(wave_file, pwave_file)
                if i < path.maxlen - 1:
                    out_files = self.run_cp2k('continue.inp', name)
            self._remove_files(self.exe_dir,
                               self._find_backup_files(self.exe_dir))
            # Read config after the step
            if i < path.maxlen - 1:
                atoms, xyz, vel, box, _ = read_cp2k_restart(restart_file)
                order = self.calculate_order(order_function, system,
                                             xyz=xyz, vel=vel, box=box)
        msg_file.write('# Propagation done.')
        energy_file = out_files['energy']
        msg_file.write('# Reading energies from: {}'.format(energy_file))
        energy = read_cp2k_energy(energy_file)
        end = (i + 1) * self.subcycles
        path.update_energies(energy['ekin'][:end:self.subcycles],
                             energy['vpot'][:end:self.subcycles])
        for _, files in out_files.items():
            self._removefile(files)
        self._removefile(prestart_file)
        self._removefile(pwave_file)
        self._removefile(continue_input)
        self._removefile(step_input)
        return success, status

    def integrate(self, system, steps, order_function=None, thermo='full'):
        """
        Propagate several integration steps.

        This method will perform several integration steps using
        CP2K. It will also calculate the order parameter(s) and
        energy terms if requested.

        Parameters
        ----------
        system : object like :py:class:`.System`
            The system we are integrating.
        steps : integer
            The number of steps we are going to perform. Note that we
            do not integrate on the first step (e.g. step 0) but we do
            obtain the other properties. This is to output the starting
            configuration.
        order_function : object like :py:class:`.OrderParameter`, optional
            An order function can be specified if we want to
            calculate the order parameter along with the simulation.
        thermo : string, optional
            Select the thermodynamic properties we are to calculate.

        Yields
        ------
        results : dict
            The results from a MD step. This contains the state of the system
            and order parameter(s) and energies (if calculated).

        """
        logger.debug('Integrating with CP2K')
        # First, copy the required input files:
        logger.debug('Adding input files for CP2K')
        self.add_input_files(self.exe_dir)
        # Get positions and velocities from the input file.
        initial_conf = self.dump_frame(system)

        box, xyz, vel, atoms = self._read_configuration(initial_conf)
        if box is None:
            box, _ = read_cp2k_box(self.input_files['template'])

        name = 'pyretis-cp2k'

        logger.debug('Thermo was set to: %s', thermo)

        # Add CP2K input for a single step:
        step_input = os.path.join(self.exe_dir, 'step.inp')
        write_for_integrate(self.input_files['template'], step_input,
                            self.timestep, self.subcycles,
                            os.path.basename(initial_conf),
                            name=name)
        # And create the input file for continuing:
        continue_input = os.path.join(self.exe_dir, 'continue.inp')
        write_for_continue(self.input_files['template'], continue_input,
                           self.timestep, self.subcycles, name=name)
        # Get the order parameter before the run:
        if order_function:
            order = self.calculate_order(order_function, system,
                                         xyz=xyz, vel=vel, box=box)
        else:
            order = None
        traj_file = os.path.join(self.exe_dir, '{}.{}'.format(name, self.ext))
        # Run the first step:
        out_files = self.run_cp2k('step.inp', name)
        restart_file = os.path.join(self.exe_dir, out_files['restart'])
        prestart_file = os.path.join(self.exe_dir, 'previous.restart')
        wave_file = os.path.join(self.exe_dir, out_files['wfn'])
        pwave_file = os.path.join(self.exe_dir, 'previous.wfn')
        # Note: Order is calculated at the END of each iteration!
        i = 0
        # Write the config so we have a non-empty file:
        write_xyz_trajectory(traj_file, xyz, vel, atoms, box, step=i,
                             append=False)
        for i in range(steps):
            if i > 0:
                # Write the previous configuration:
                write_xyz_trajectory(traj_file, xyz, vel, atoms, box,
                                     step=i)
            if i == 0:
                pass
            elif i > 0:
                self._movefile(restart_file, prestart_file)
                self._movefile(wave_file, pwave_file)
                if i < steps - 1:  # Do not integrate the last step.
                    out_files = self.run_cp2k('continue.inp', name)
            self._remove_files(self.exe_dir,
                               self._find_backup_files(self.exe_dir))
            results = {}
            if order:
                results['order'] = order
            # Read config after the step
            if i < steps - 1:
                atoms, xyz, vel, box, _ = read_cp2k_restart(restart_file)
                if order_function:
                    order = self.calculate_order(order_function, system,
                                                 xyz=xyz, vel=vel, box=box)
            energy = read_cp2k_energy(out_files['energy'])
            end = (i + 1) * self.subcycles
            results['thermo'] = {}
            for key, val in energy.items():
                results['thermo'][key] = val[:end:self.subcycles][-1]
            yield results
        # Note we do not remove the run-files here as they might be
        # useful for the user.

    def step(self, system, name):
        """Perform a single step with CP2K.

        Parameters
        ----------
        system : object like :py:class:`.System`
            The system we are integrating.
        name : string
            To name the output files from the CP2K step.

        Returns
        -------
        out : string
            The name of the output configuration, obtained after
            completing the step.

        """
        initial_conf = self.dump_frame(system)
        # Prepare input files etc.:
        self.add_input_files(self.exe_dir)
        box, xyz, vel, atoms = self._read_configuration(initial_conf)
        if box is None:
            box, _ = read_cp2k_box(self.input_files['template'])
        # Add CP2K input for a single step:
        step_input = os.path.join(self.exe_dir, 'step.inp')
        write_for_step_vel(self.input_files['template'], step_input,
                           self.timestep, self.subcycles,
                           os.path.basename(initial_conf),
                           vel, name=name)

        # Execute single step CP2K...
        logger.debug('Executing CP2K')
        out_files = self.run_cp2k('step.inp', name)
        energy = read_cp2k_energy(out_files['energy'])
        # Get the output configuration:
        atoms, xyz, vel, box, _ = read_cp2k_restart(out_files['restart'])
        conf_out = os.path.join(self.exe_dir, '{}.{}'.format(name, self.ext))
        write_xyz_trajectory(conf_out, xyz, vel, atoms, box, append=False)
        system.particles.set_pos((conf_out, None))
        system.particles.set_vel(False)
        system.particles.ekin = energy['ekin'][-1]
        system.particles.vpot = energy['vpot'][-1]
        system.update_box(box)
        # Prepare input files etc.:
        logger.debug('Removing CP2K output after single step.')
        # Remove run-files etc:
        for _, files in out_files.items():
            self._removefile(files)
        self._remove_files(
            self.exe_dir,
            self._find_backup_files(self.exe_dir)
        )
        return conf_out

    def add_input_files(self, dirname):
        """Add required input files to a given directory.

        Parameters
        ----------
        dirname : string
            The full path to where we want to add the files.

        """
        for filei in self.extra_files:
            basename = os.path.basename(self.extra_files[filei])
            dest = os.path.join(dirname, basename)
            if not os.path.isfile(dest):
                logger.debug('Adding input file "%s" to "%s"',
                             basename, dirname)
                self._copyfile(self.extra_files[filei], dest)

    @staticmethod
    def _find_backup_files(dirname):
        """Return backup-files in the given directory."""
        out = []
        for entry in os.scandir(dirname):
            if entry.is_file():
                match = REGEXP_BACKUP.search(entry.name)
                if match is not None:
                    out.append(entry.name)
        return out

    @staticmethod
    def _read_configuration(filename):
        """
        Read CP2K output configuration.

        This method is used when we calculate the order parameter.

        Parameters
        ----------
        filename : string
            The file to read the configuration from.

        Returns
        -------
        box : numpy.array
            The box dimensions if we manage to read it.
        xyz : numpy.array
            The positions.
        vel : numpy.array
            The velocities.
        names : list of strings
            The atom names found in the file.

        """
        xyz, vel, box, names = None, None, None, None
        for snapshot in read_xyz_file(filename):
            box, xyz, vel, names = convert_snapshot(snapshot)
            break  # Stop after the first snapshot.
        return box, xyz, vel, names

    def _reverse_velocities(self, filename, outfile):
        """Reverse velocity in a given snapshot.

        Parameters
        ----------
        filename : string
            The configuration to reverse velocities in.
        outfile : string
            The output file for storing the configuration with
            reversed velocities.

        """
        box, xyz, vel, names = self._read_configuration(filename)
        write_xyz_trajectory(outfile, xyz, -1.0*vel, names, box, append=False)

    def _prepare_shooting_point(self, input_file):
        """
        Create initial configuration for a shooting move.

        This creates a new initial configuration with random velocities.

        Parameters
        ----------
        input_file : string
            The input configuration to generate velocities for.

        Returns
        -------
        output_file : string
            The name of the file created.
        energy : dict
            The energy terms read from the CP2K energy file.

        """
        box, xyz, vel, atoms = self._read_configuration(input_file)
        if box is None:
            box, _ = read_cp2k_box(self.input_files['template'])
        input_config = os.path.join(self.exe_dir, 'genvel_input.xyz')
        write_xyz_trajectory(input_config, xyz, vel, atoms, box, append=False)
        # Create input file for CP2K:
        run_file = os.path.join(self.exe_dir, 'run.inp')
        write_for_genvel(self.input_files['template'],
                         run_file,
                         'genvel_input.xyz',
                         self.rgen.random_integers(1, 999999999),
                         name='genvel')
        # Prepare to run it:
        self.add_input_files(self.exe_dir)
        out_files = self.run_cp2k(run_file, 'genvel')
        energy = read_cp2k_energy(out_files['energy'])
        # Get the output configuration:
        atoms, xyz, vel, box, _ = read_cp2k_restart(out_files['restart'])
        conf_out = os.path.join(self.exe_dir,
                                '{}.{}'.format('genvel', self.ext))
        write_xyz_trajectory(conf_out, xyz, vel, atoms, box, append=False)
        # Remove run-files etc:
        for _, files in out_files.items():
            self._removefile(files)
        self._remove_files(
            self.exe_dir,
            self._find_backup_files(self.exe_dir)
        )
        return conf_out, energy

    def modify_velocities(self, system, rgen, sigma_v=None, aimless=True,
                          momentum=False, rescale=None):
        """
        Modify the velocities of the current state.

        This method will modify the velocities of a time slice.

        Parameters
        ----------
        system : object like :py:class:`.System`
            System is used here since we need access to the particle
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
        dek, kin_old, kin_new = None, None, None
        if rescale is not None and rescale is not False and rescale > 0:
            msgtxt = 'CP2K engine does not support energy re-scale.'
            logger.error(msgtxt)
            raise NotImplementedError(msgtxt)
        else:
            kin_old = system.particles.ekin
        if aimless:
            pos = self.dump_frame(system)
            posvel, energy = self._prepare_shooting_point(pos)
            kin_new = energy['ekin'][-1]
            system.particles.set_pos((posvel, None))
            system.particles.set_vel(False)
            system.particles.ekin = kin_new
            system.particles.vpot = energy['vpot'][-1]
        else:  # Soft velocity change, from a Gaussian distribution:
            msgtxt = 'CP2K engine only support aimless shooting!'
            logger.error(msgtxt)
            raise NotImplementedError(msgtxt)
        if momentum:
            pass
        if kin_old is None or kin_new is None:
            dek = float('inf')
            logger.warning(('Kinetic energy not found for previous point.'
                            '\n(This happens when the initial configuration '
                            'does not contain energies.)'))
        else:
            dek = kin_new - kin_old
        return dek, kin_new
