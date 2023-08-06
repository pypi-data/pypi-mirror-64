# -*- coding: utf-8 -*-
# Copyright (c) 2019, PyRETIS Development Team.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""Test the methods in pyretis.inout.setup.createsystem."""
import os
import logging
import filecmp
import unittest
import tempfile
import numpy as np
from pyretis.core.system import System
from pyretis.inout.common import make_dirs
from pyretis.engines.external import ExternalMDEngine
from pyretis.inout.formats.xyz import (
    read_xyz_file,
    convert_snapshot,
)
from pyretis.orderparameter.orderparameter import PositionVelocity
from pyretis.core.particles import ParticlesExt
from .test_helpers.test_helpers import remove_dir
logging.disable(logging.CRITICAL)


HERE = os.path.abspath(os.path.dirname(__file__))


class DummyExternal(ExternalMDEngine):
    """A dummy external engine. Only useful for testing."""

    def __init__(self, input_path, timestep, subcycles):
        """Initialise the dummy engine."""
        super().__init__('External engine for testing!', timestep,
                         subcycles)
        self.input_path = os.path.abspath(input_path)
        self.input_files = {
            'conf': os.path.join(self.input_path, 'dummy_config'),
            'template': os.path.join(self.input_path, 'dummy_template'),
        }

    def step(self, system, name):
        """Perform a single dummy step."""

    def _read_configuration(self, filename):
        """Read a xyz configuration."""
        xyz, vel, box, names = None, None, None, None
        for snapshot in read_xyz_file(filename):
            box, xyz, vel, names = convert_snapshot(snapshot)
            break
        return box, xyz, vel, names

    def _reverse_velocities(self, filename, outfile):
        """Reverse velocoties with a dummy method."""

    def _extract_frame(self, traj_file, idx, out_file):
        """Extract a frame, dummy method."""

    def _propagate_from(self, name, path, system, order_function, interfaces,
                        msg_file, reverse=False):
        """Propagate with the engine, dummy method."""
        # pylint: disable=too-many-arguments

    def modify_velocities(self, system, rgen, sigma_v=None, aimless=True,
                          momentum=False, rescale=None):
        """Modify velocities, dummy method."""
        # pylint: disable=too-many-arguments


class TestExternalEngine(unittest.TestCase):
    """Run tests for the external engine."""

    def test_exe_dir(self):
        """Test exe_dir property."""
        engine = DummyExternal('test', 1.0, 10)
        self.assertIsNone(engine.exe_dir)
        logging.disable(logging.INFO)
        with self.assertLogs('pyretis.engines.engine', level='WARNING'):
            engine.exe_dir = 'non-existing-dir'
        logging.disable(logging.CRITICAL)
        self.assertEqual('non-existing-dir', engine.exe_dir)

    def test_integration_step(self):
        """Test that the integration step fails for the external integrator."""
        engine = DummyExternal('test', 1.0, 10)
        with self.assertRaises(NotImplementedError):
            engine.integration_step(None)

    def test_read_input_settings(self):
        """Test that we can read input settings."""
        filename = os.path.join(HERE, 'input.txt')
        engine = DummyExternal('test', 1.0, 10)
        # pylint: disable=protected-access
        settings = engine._read_input_settings(filename)
        correct = {'b': '100', 'a': '1', 'another setting': 'text'}
        for key, val in correct.items():
            self.assertEqual(val, settings[key])

    def test_modify_input(self):
        """Test that we can modify input settings."""
        engine = DummyExternal('test', 1.0, 10)
        filename = os.path.join(HERE, 'input.txt')
        settings = {'another setting': 'hello', 'c': '101'}
        # pylint: disable=protected-access
        with tempfile.NamedTemporaryFile() as temp:
            engine._modify_input(filename, temp.name, settings)
            temp.flush()
            settings2 = engine._read_input_settings(temp.name)
            correct = {'b': '100', 'a': '1', 'another setting': 'hello',
                       'c': '101'}
            for key, val in correct.items():
                self.assertEqual(val, settings2[key])

    def test_move_file(self):
        """Test that we can move files."""
        engine = DummyExternal('test', 1.0, 10)
        filename = os.path.join(HERE, 'empty_file')
        with open(filename, 'w') as temp:
            temp.write('Hello!')
        outfile = os.path.join(HERE, 'empty_file2')
        # pylint: disable=protected-access
        engine._movefile(filename, outfile)
        self.assertTrue(os.path.isfile(outfile))
        self.assertFalse(os.path.isfile(filename))
        engine._removefile(outfile)
        engine._removefile(filename)

    def test_copy_file(self):
        """Test that we can copy files."""
        engine = DummyExternal('test', 1.0, 10)
        filename = os.path.join(HERE, 'empty_file')
        with open(filename, 'w') as temp:
            temp.write('Hello!')
        outfile = os.path.join(HERE, 'empty_file_copy')
        # pylint: disable=protected-access
        engine._copyfile(filename, outfile)
        self.assertTrue(os.path.isfile(outfile))
        self.assertTrue(os.path.isfile(filename))
        compare = filecmp.cmp(filename, outfile)
        self.assertTrue(compare)
        engine._removefile(outfile)
        engine._removefile(filename)

    def test_removefiles(self):
        """Test that we can remove several files."""
        engine = DummyExternal('test', 1.0, 10)
        files = []
        for i in range(3):
            basename = 'empty_file{}'.format(i)
            filename = os.path.join(HERE, basename)
            with open(filename, 'w') as temp:
                temp.write('Hello!')
            files.append(basename)
        # pylint: disable=protected-access
        engine._remove_files(HERE, files)
        for i in files:
            filename = os.path.join(HERE, i)
            self.assertFalse(os.path.isfile(filename))

    def test_cleanup(self):
        """Test the cleanup method."""
        dirname = os.path.join(HERE, 'testdir')
        make_dirs(dirname)
        files = []
        for i in range(3):
            basename = 'empty_file{}'.format(i)
            filename = os.path.join(dirname, basename)
            with open(filename, 'w') as temp:
                temp.write('Hello!')
            files.append(filename)
        engine = DummyExternal('test', 1.0, 10)
        engine.exe_dir = dirname
        engine.clean_up()
        for i in files:
            self.assertFalse(os.path.isfile(i))
        remove_dir(dirname)

    def test_read_configuration(self):
        """Test that we can read a configuration."""
        engine = DummyExternal('test', 1.0, 10)
        filename = os.path.join(HERE, 'config.xyz')
        # pylint: disable=protected-access
        box, xyz, vel, atoms = engine._read_configuration(filename)
        correct_box = np.array([1., 2., 3.])
        self.assertTrue(np.allclose(box, correct_box))
        correct_atoms = ['Ba', 'Hf', 'O', 'O', 'O']
        for i, j in zip(correct_atoms, atoms):
            self.assertEqual(i, j)
        correct_xyz = np.array([[0., 0., 0.], [0.5, 0.5, 0.5],
                                [0.5, 0.5, 0.], [0.5, 0., 0.5],
                                [0., 0.5, 0.5]])
        self.assertTrue(np.allclose(xyz, correct_xyz))
        correct_vel = np.array([[1., 1., 1.], [2., 2., 2.], [3., 3., 3.],
                                [4., 4., 4.], [5., 5., 5.]])
        self.assertTrue(np.allclose(vel, correct_vel))

    def test_calculate_order(self):
        """Test calculation of the order parameter."""
        engine = DummyExternal('test', 1.0, 10)
        filename = os.path.join(HERE, 'config.xyz')
        order_function = PositionVelocity(0, dim='x', periodic=False)
        system = System()
        system.particles = ParticlesExt(dim=3)
        system.particles.config = (filename, 0)
        order = engine.calculate_order(order_function, system)
        self.assertAlmostEqual(order[0], 0.0)
        self.assertAlmostEqual(order[1], 1.0)
        system.particles.vel_rev = True
        order = engine.calculate_order(order_function, system)
        self.assertAlmostEqual(order[1], -1.0)

    def test_execute_command(self):
        """Test what happens when the execution fails."""
        engine = DummyExternal('test', 1.0, 10)
        cmd = [os.path.join(HERE, 'aprogram.py')]
        engine.execute_command(cmd, cwd=HERE, inputs=b'')
        cmd.append('arg')
        with self.assertRaises(RuntimeError):
            engine.execute_command(cmd, cwd=HERE, inputs=b'')
        # The outputs should be reatined after the previous error:
        with open(os.path.join(HERE, 'stdout.txt'), 'r') as stdout:
            lines = stdout.readlines()
            self.assertEqual(len(lines), 1)
            self.assertEqual(
                lines[0].strip(),
                'This is a program for testing external commands.'
            )
        with open(os.path.join(HERE, 'stderr.txt'), 'r') as stdout:
            lines = stdout.readlines()
            self.assertEqual(len(lines), 2)
            self.assertEqual(
                lines[0].strip(),
                'ERROR: Program got arguments:'
            )
            self.assertEqual(
                lines[1].strip(),
                ' '.join(cmd)
            )
        for fname in ('stdout.txt', 'stderr.txt'):
            # pylint: disable=protected-access
            engine._removefile(os.path.join(HERE, fname))


if __name__ == '__main__':
    unittest.main()
