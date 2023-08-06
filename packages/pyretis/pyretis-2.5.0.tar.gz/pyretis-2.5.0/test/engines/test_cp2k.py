# -*- coding: utf-8 -*-
# Copyright (c) 2019, PyRETIS Development Team.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""Test the CP2KEngine class."""
from io import StringIO
import logging
import os
import unittest
from unittest.mock import patch
import numpy as np
from pyretis.core.system import System
from pyretis.core.path import Path
from pyretis.core.particles import ParticlesExt
from pyretis.engines import CP2KEngine
from pyretis.inout.common import make_dirs
from pyretis.inout.formats.xyz import (
    read_xyz_file,
    convert_snapshot,
)
from pyretis.orderparameter.orderparameter import PositionVelocity
from .test_helpers.test_helpers import remove_dir
logging.disable(logging.DEBUG)

HERE = os.path.abspath(os.path.dirname(__file__))


def make_test_system(conf):
    """Just make a test system with particles."""
    system = System()
    system.particles = ParticlesExt(dim=3)
    system.particles.config = conf
    return system


class CP2KEngineTest(unittest.TestCase):
    """Run the tests for the CP2KEngine."""

    def test_init(self):
        """Test that we can initiate the engine."""
        dir_name = os.path.join(HERE, 'cp2k_input')
        extra_files = ['extra_file']
        engine = CP2KEngine('cp2k', dir_name, 0.002, 10,
                            extra_files=extra_files)
        self.assertEqual(len(engine.extra_files), 1)
        # Check that we get an error if we are missing files.
        with self.assertRaises(ValueError):
            CP2KEngine('cp2k', '', 0.002, 10, 'not-directory-file')

    def test_single_step(self):
        """Test that the single step method work as we intend."""
        cmd = os.path.join(HERE, 'mockcp2k.py')
        dir_name = os.path.join(HERE, 'cp2k_input')
        extra_files = ['extra_file']
        engine = CP2KEngine(cmd, dir_name, 0.002, 10, extra_files)
        rundir = os.path.join(HERE, 'generate')
        # Create the directory for running:
        make_dirs(rundir)
        engine.exe_dir = rundir
        # Create the system:
        system = make_test_system((engine.input_files['conf'], 0))
        # Run a single step:
        out = engine.step(system, 'cp2k_step')
        # Check that we have the expected files after the step:
        for i in ('extra_file', 'step.inp', 'conf.xyz', 'cp2k_step.xyz'):
            self.assertTrue(os.path.isfile(os.path.join(rundir, i)))
        self.assertAlmostEqual(system.particles.ekin, 0.9)
        self.assertAlmostEqual(system.particles.vpot, -0.9)
        # Get snapshot:
        box, xyz, vel, names = convert_snapshot(next(read_xyz_file(out)))
        for i, j in zip(names, ['H', 'H']):
            self.assertEqual(i, j)
        self.assertTrue(
            np.allclose(box,
                        np.array([1., 2., 3.]))
        )
        self.assertTrue(
            np.allclose(xyz,
                        np.array([[0.9, 1.8, 2.7], [1.9, 2.8, 3.7]]))
        )
        self.assertTrue(
            np.allclose(vel,
                        np.array([[9.9, 10.8, 11.7], [10.9, 11.8, 12.7]]))
        )
        engine.clean_up()
        remove_dir(rundir)

    def test_modify_velocities(self):
        """Test the modify velocities method."""
        cmd = os.path.join(HERE, 'mockcp2k.py')
        dir_name = os.path.join(HERE, 'cp2k_input')
        extra_files = ['extra_file']
        engine = CP2KEngine(cmd, dir_name, 0.002, 10, extra_files)
        rundir = os.path.join(HERE, 'generatevel')
        # Create the directory for running:
        make_dirs(rundir)
        engine.exe_dir = rundir
        # Create the system:
        system = make_test_system((engine.input_files['conf'], 0))
        # Modify velocities:
        dek, kin_new = engine.modify_velocities(system, None, sigma_v=None,
                                                aimless=True,
                                                momentum=False, rescale=None)
        self.assertAlmostEqual(kin_new, 0.9)
        self.assertTrue(dek == float('inf'))
        # Check that aiming fails:
        with self.assertRaises(NotImplementedError):
            engine.modify_velocities(system, None, sigma_v=None, aimless=False,
                                     momentum=False, rescale=None)
        # Check that rescaling fails:
        with self.assertRaises(NotImplementedError):
            engine.modify_velocities(system, None, sigma_v=None, aimless=False,
                                     momentum=False, rescale=10)
        dek, kin_new = engine.modify_velocities(system, None, sigma_v=None,
                                                aimless=True,
                                                momentum=False, rescale=None)
        self.assertAlmostEqual(kin_new, 0.9)
        self.assertAlmostEqual(dek, 0.0)
        engine.clean_up()
        remove_dir(rundir)

    def test_propagate_forward(self):
        """Test the propagate method forward in time."""
        cmd = os.path.join(HERE, 'mockcp2k.py')
        dir_name = os.path.join(HERE, 'cp2k_input')
        extra_files = ['extra_file']
        engine = CP2KEngine(cmd, dir_name, 0.002, 10, extra_files)
        rundir = os.path.join(HERE, 'generatef')
        # Create the directory for running:
        make_dirs(rundir)
        engine.exe_dir = rundir
        # Create the system:
        system = make_test_system((engine.input_files['conf'], 0))
        # Propagate:
        orderp = PositionVelocity(0, dim='x', periodic=False)
        path = Path(None, maxlen=4)
        with patch('sys.stdout', new=StringIO()):
            success, _ = engine.propagate(path, system, orderp,
                                          [0.2, 8.0, 9.0], reverse=False)
            self.assertFalse(success)
        engine.clean_up()
        remove_dir(rundir)

    def test_propagate_backward(self):
        """Test the propagate method forward in time."""
        cmd = os.path.join(HERE, 'mockcp2k.py')
        dir_name = os.path.join(HERE, 'cp2k_input')
        extra_files = ['extra_file']
        engine = CP2KEngine(cmd, dir_name, 0.002, 10, extra_files)
        rundir = os.path.join(HERE, 'generateb')
        # Create the directory for running:
        make_dirs(rundir)
        engine.exe_dir = rundir
        # Create the system:
        system = make_test_system((engine.input_files['conf'], 0))
        # Propagate:
        orderp = PositionVelocity(0, dim='x', periodic=False)
        path = Path(None, maxlen=4)
        with patch('sys.stdout', new=StringIO()):
            success, _ = engine.propagate(path, system, orderp,
                                          [0.2, 0.5, 0.8], reverse=True)
            self.assertTrue(success)
        # Check that initial velocities were reversed:
        infile = os.path.join(rundir, 'conf.xyz')
        _, _, vel, _ = convert_snapshot(next(read_xyz_file(infile)))
        outfile = os.path.join(rundir, 'r_conf.xyz')
        _, _, rvel, _ = convert_snapshot(next(read_xyz_file(outfile)))
        self.assertTrue(np.allclose(vel, -1.0 * rvel))
        engine.clean_up()
        remove_dir(rundir)

    def test_integrate(self):
        """Test the integrate method."""
        cmd = os.path.join(HERE, 'mockcp2k.py')
        dir_name = os.path.join(HERE, 'cp2k_input')
        extra_files = ['extra_file']
        engine = CP2KEngine(cmd, dir_name, 0.002, 10, extra_files)
        rundir = os.path.join(HERE, 'cp2kintegrate')
        # Create the directory for running:
        make_dirs(rundir)
        engine.exe_dir = rundir
        # Create the system:
        system = make_test_system((engine.input_files['conf'], 0))
        # Propagate:
        orderp = PositionVelocity(0, dim='x', periodic=False)
        correct_order = [
            [0.77317158100000005, 1.0],
            [0.9, 9.9],
            [0.9, 9.9],
        ]
        for i, step in enumerate(engine.integrate(system, 2,
                                                  order_function=orderp)):
            self.assertTrue(np.allclose(step['order'], correct_order[i]))
        # Call once more, without specifying order_function:
        for step in engine.integrate(system, 3):
            self.assertFalse("order" in step)
        # Call once more, after first creating a fake backup-file:
        bfile = os.path.join(rundir, 'backup.bak-1')
        with open(bfile, 'w') as output:
            output.write('Just a line')
        listoffiles = [entry.name for entry in os.scandir(rundir)]
        self.assertTrue("backup.bak-1" in listoffiles)
        for step in engine.integrate(system, 1):
            self.assertFalse("order" in step)
        # Check that PyRETIS has removed the backup-file.
        listoffiles = [entry.name for entry in os.scandir(rundir)]
        self.assertFalse("backup.bak-1" in listoffiles)
        engine.clean_up()
        remove_dir(rundir)

    def test_dump_config(self):
        """Test the dump_config method."""
        cmd = os.path.join(HERE, 'mockcp2k.py')
        dir_name = os.path.join(HERE, 'cp2k_input')
        extra_files = ['extra_file']
        engine = CP2KEngine(cmd, dir_name, 0.002, 10, extra_files)
        trajdir = os.path.join(HERE, 'cp2k_fake_trajectory')
        # Create the directory for storing a fake trajectory file:
        make_dirs(trajdir)
        engine.exe_dir = trajdir
        # Set up for a trajectory file:
        trajfile = os.path.join(trajdir, 'traj.xyz')
        # Set up for a config file:
        conffile = os.path.join(trajdir, 'conf.xyz')
        lines = [
            "2",
            "# Step: 0 Box:    1.0000    1.1    1.2",
            "O         0.71    -0.361     0.332  1.1 2.2 3.6",
            "H         0.72    -0.362     0.333  1.2 2.3 3.7",
            "2",
            "# Step: 1 Box:    1.0000    1.1    1.2",
            "O         0.61    -0.331     0.232  1.5 2.2 3.7",
            "H         0.62    -0.366     0.133  2.2 3.3 4.7",
        ]
        with open(trajfile, 'w') as output:
            output.write('\n'.join(lines))
        for i in range(3):
            config = (trajfile, i)
            if i == 0:  # Config file should not exist.
                self.assertFalse(os.path.isfile(conffile))
            if i == 1:  # Config file should exist, and will be overwritten.
                self.assertTrue(os.path.isfile(conffile))
            engine.dump_config(config)
            if i == 1:
                #  Note: is it possible to check the log-file here?
                #  logger.warning('CP2K will overwrite %s', out_file)
                continue
            if i == 2:
                # Note: is it possible to check the log-file here?
                # logger.error('CP2K could not extract index %i ....
                break
            lines2 = None
            with open(conffile, 'r') as infile:
                lines2 = infile.readlines()
            len2 = len(lines2)
            for j in range(len2):
                words1 = lines[i*len2+j].split()
                words2 = lines2[j].split()
                if j == 0:
                    self.assertEqual(1, len(words2))
                    self.assertEqual(words1, words2)
                if j == 1:
                    self.assertNotEqual(words1, words2)
                    self.assertEqual(words2[1], "Box:")
                if j > 1:
                    # First item is the particle type/elements:
                    self.assertEqual(words1[0], words2[0])
                    # The rest is just numbers:
                    for k in range(1, len(words2)):
                        self.assertAlmostEqual(
                            float(words1[k]),
                            float(words2[k])
                        )
        engine.clean_up()
        remove_dir(trajdir)


if __name__ == '__main__':
    unittest.main()
