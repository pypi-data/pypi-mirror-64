# -*- coding: utf-8 -*-
# Copyright (c) 2019, PyRETIS Development Team.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""Test the C implementation of the Lennard Jones potential.

This test is comparing the three versions of the Lennard Jones
potential:

1) The pure python implementation

2) The numpy python implementation

3) The C implementation.
"""
# pylint: disable=invalid-name
import unittest
import numpy as np
from pyretis.core import System, create_box, Particles
from pyretis.core.units import create_conversion_factors
from pyretis.forcefield import ForceField
from pyretis.forcefield.potentials import PairLennardJonesCut
from pyretis.forcefield.potentials import PairLennardJonesCutnp
from pyretis.tools import generate_lattice
from ljpotentialc import PairLennardJonesCutC


def set_up_initial_state():
    """Create particles for the test."""
    create_conversion_factors('lj')
    lattice, size = generate_lattice('fcc', [5, 5, 5], density=0.9)
    size = np.array(size)
    npart = len(lattice)
    lattice += np.random.randn(npart, 3) * 0.05
    box = create_box(low=size[:, 0], high=size[:, 1],
                     periodic=[True, True, True])
    system = System(temperature=1.0, units='lj', box=box)
    system.particles = Particles(dim=3)
    for pos in lattice:
        system.add_particle(name='Ar', pos=pos, mass=1.0, ptype=0)
    msg = 'Created lattice with {} atoms.'
    print(msg.format(system.particles.npart))
    return system


def run_calculations(system, parameters):
    """Evaluate the LJ potential."""
    # Calculate with C:
    potential_ext = PairLennardJonesCutC(dim=3, shift=True)
    forcefield_ext = ForceField('Python + external c force field',
                                potential=[potential_ext],
                                params=[parameters])
    system.forcefield = forcefield_ext
    print('Evaluating with: {}'.format(forcefield_ext.print_potentials()))
    vpot_ext, forces_ext, virial_ext = system.potential_and_force()
    vpot_ext /= float(system.particles.npart)
    # Calculate with pure python implementation:
    potential = PairLennardJonesCut(dim=3, shift=True)
    forcefield = ForceField('Pure Python force field',
                            potential=[potential],
                            params=[parameters])
    system.forcefield = forcefield
    print('Evaluating with: {}'.format(forcefield.print_potentials()))
    vpot, forces, virial = system.potential_and_force()
    vpot /= float(system.particles.npart)
    # Calculate with numpy python implementation:
    potentialnp = PairLennardJonesCutnp(dim=3, shift=True)
    forcefieldnp = ForceField('Python force field with numpy',
                              potential=[potentialnp],
                              params=[parameters])
    system.forcefield = forcefieldnp
    print('Evaluating with: {}'.format(forcefieldnp.print_potentials()))
    vpotnp, forcesnp, virialnp = system.potential_and_force()
    vpotnp /= float(system.particles.npart)
    return ((vpot, forces, virial),
            (vpotnp, forcesnp, virialnp),
            (vpot_ext, forces_ext, virial_ext))


class LennardJonesTest(unittest.TestCase):
    """Run the tests for the C potential class."""

    def test_lj(self):
        """Test one-component system."""
        print('\nTesting for a one-component system')
        system = set_up_initial_state()
        param = {0: {'sigma': 1.0, 'epsilon': 1.0, 'rcut': 2.5}}
        maxcut = 0.5 * min(system.box.length)
        for key in param:
            if 'rcut' in param[key]:
                self.assertGreaterEqual(maxcut, param[key]['rcut'])
        result = run_calculations(system, param)
        keys = ['python', 'python-numpy', 'c']
        for i, keyi in enumerate(keys[:-1]):
            for j, key2 in enumerate(keys[i+1:]):
                print('\nCompare {} and {}'.format(keyi, key2))
                force = np.allclose(result[i][1], result[i+j+1][1])
                print(' -> Forces close: {}'.format(force))
                self.assertTrue(force)
                virial = np.allclose(result[i][2], result[i+j+1][2])
                print(' -> Virial close: {}'.format(virial))
                self.assertTrue(virial)
                self.assertAlmostEqual(result[i][0], result[i+j+1][0], 7)
                vdiff = np.abs(result[i][0] - result[i+j+1][0])
                print(' -> Difference in pot. energy: {:.15e}'.format(vdiff))

    def test_lj_mix(self):
        """Test for mixture."""
        print('\nTesting for a two-component mixture')
        system = set_up_initial_state()
        param = {0: {'sigma': 1.0, 'epsilon': 1.0, 'rcut': 2.5},
                 1: {'sigma': 2.0, 'epsilon': 1.2, 'rcut': 3.5}}
        idx = [i for i in range(system.particles.npart)]
        idx2 = np.random.choice(idx, size=int(system.particles.npart * 0.5),
                                replace=False)
        maxcut = 0.5 * min(system.box.length)
        for key in param:
            if 'rcut' in param[key]:
                self.assertGreaterEqual(maxcut, param[key]['rcut'])
        print('Mutating {} particles'.format(len(idx2)))
        for i in idx2:
            system.particles.ptype[i] = 1
        result = run_calculations(system, param)
        keys = ['python', 'python-numpy', 'c']
        for i, keyi in enumerate(keys[:-1]):
            for j, key2 in enumerate(keys[i+1:]):
                print('\nCompare {} and {}'.format(keyi, key2))
                force = np.allclose(result[i][1], result[i+j+1][1])
                print(' -> Forces close: {}'.format(force))
                self.assertTrue(force)
                virial = np.allclose(result[i][2], result[i+j+1][2])
                print(' -> Virial close: {}'.format(virial))
                self.assertTrue(virial)
                self.assertAlmostEqual(result[i][0], result[i+j+1][0], 7)
                vdiff = np.abs(result[i][0] - result[i+j+1][0])
                print(' -> Difference in pot. energy: {:.15e}'.format(vdiff))

    def test_lj_multi_mix(self):
        """Test for multi-mixture."""
        ncomp = np.random.randint(3, 11)
        print('\nTesting for a {}-component mixture'.format(ncomp))
        system = set_up_initial_state()
        param = {0: {'sigma': 1.0, 'epsilon': 1.0, 'rcut': 2.5}}
        maxcut = 0.5 * min(system.box.length)
        self.assertGreaterEqual(maxcut, param[0]['rcut'])

        idx = np.array([i for i in range(system.particles.npart)],
                       dtype=np.int32)
        np.random.shuffle(idx)
        for i, idx2 in enumerate(np.array_split(idx, ncomp)):
            system.particles.ptype[idx2] = i
            if i not in param:
                param[i] = {'sigma': np.random.uniform(low=0.5, high=1.5),
                            'epsilon': np.random.uniform(low=0.5, high=1.5),
                            'rcut': np.random.uniform(low=2.0, high=maxcut)}
        natoms = {}
        for i in range(system.particles.npart):
            ptype = system.particles.ptype[i]
            if ptype not in natoms:
                natoms[ptype] = 0
            natoms[ptype] += 1
        for atom in natoms:
            print('{} atoms of type {}'.format(natoms[atom], atom))
        result = run_calculations(system, param)
        keys = ['python', 'python-numpy', 'c']
        for i, keyi in enumerate(keys[:-1]):
            for j, key2 in enumerate(keys[i+1:]):
                print('\nCompare {} and {}'.format(keyi, key2))
                force = np.allclose(result[i][1], result[i+j+1][1])
                print(' -> Forces close: {}'.format(force))
                self.assertTrue(force)
                virial = np.allclose(result[i][2], result[i+j+1][2])
                print(' -> Virial close: {}'.format(virial))
                self.assertTrue(virial)
                self.assertAlmostEqual(result[i][0], result[i+j+1][0], 7)
                vdiff = np.abs(result[i][0] - result[i+j+1][0])
                print(' -> Difference in pot. energy: {:.15e}'.format(vdiff))


if __name__ == '__main__':
    unittest.main()
