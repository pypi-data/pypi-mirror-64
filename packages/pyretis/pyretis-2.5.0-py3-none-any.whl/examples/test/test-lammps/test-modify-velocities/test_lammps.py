# -*- coding: utf-8 -*-
# Copyright (c) 2019, PyRETIS Development Team.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""A test using the LAMMPS engine."""
import math
import os
import colorama
import numpy as np
from pyretis.core.random_gen import create_random_generator
from pyretis.inout.common import make_dirs
from pyretis.engines.lammps import LAMMPSEngine
from pyretis.inout import print_to_screen
from pyretis.testing.systemhelp import create_system_ext
from pyretis.testing.helpers import clean_dir


HERE = os.path.abspath(os.path.dirname(__file__))


def backup_files(dirname, prefix='prev_'):
    """Backup some files so we can inspect them later."""
    files = {'generate_vel.in', 'generate_vel.lammpstrj',
             'generate_vel.log', 'generate_vel.screen',
             'order_generate_vel.txt'}
    backup = {}
    for i in files:
        new_name = os.path.join(dirname, '{}{}'.format(prefix, i))
        os.rename(os.path.join(dirname, i), new_name)
        backup[i] = new_name
    return backup


def modify_velocities():
    """Use the LAMMPS engine to run a MD simulation forward in time."""
    print_to_screen('\nTesting that we can draw randomized velocities.')
    engine = LAMMPSEngine('lmp_serial', 'lammps_input', 1)
    # Create a dummy system:
    system = create_system_ext(pos=('system.data', 0))
    exe_dir = os.path.join(HERE, 'generate')
    # Set up some directories:
    make_dirs(exe_dir)
    clean_dir(exe_dir)
    engine.exe_dir = exe_dir
    # Draw random velocities:
    dek, kin_new = engine.modify_velocities(system, rgen=None)
    # This system did not have a kinetic energy assigned.
    assert dek == float('inf')
    assert math.isclose(kin_new, 1.4970703)
    # The order parameter is the position and velocity of particle 1:
    assert np.allclose(system.order, [1.68543117318838, -0.234327230058829])
    print_to_screen('\n-> First draw worked as expected.', level='success')
    # Now, backup the input/output files so we can inspect
    # them later.
    prefix = 'prev_0_'
    files = backup_files(exe_dir, prefix=prefix)
    # Move the position file:
    filename = os.path.basename(system.particles.get_pos()[0])
    system.particles.set_pos((files[filename], 0))
    # Draw random velocities again:
    dek, kin_new = engine.modify_velocities(system, rgen=None)
    assert math.isclose(dek, 0.0)
    assert math.isclose(kin_new, 1.4970703)
    # Same seed, velocity should still be the same:
    assert np.allclose(system.order, [1.68543117318838, -0.234327230058829])
    print_to_screen('\n-> Second draw worked as expected.', level='success')
    # Bakcup files again:
    prefix = 'prev_1_'
    files = backup_files(exe_dir, prefix=prefix)
    filename = os.path.basename(system.particles.get_pos()[0])
    system.particles.set_pos((files[filename], 0))
    # Draw random velocities again, but with a different seed:
    rgen = create_random_generator({'seed': 0})
    dek, kin_new = engine.modify_velocities(system, rgen)
    assert math.isclose(dek, 0.0)
    assert math.isclose(kin_new, 1.4970703)
    # Different seed, velocity should have changed
    assert np.allclose(system.order, [1.68543117318838, 0.277207562198471])
    print_to_screen('\n-> Third draw worked as expected.', level='success')
    print_to_screen('\nAll draws were successful!', level='success')


def main():
    """Run the comparisons."""
    modify_velocities()


if __name__ == '__main__':
    colorama.init(autoreset=True)
    main()
