# -*- coding: utf-8 -*-
# Copyright (c) 2019, PyRETIS Development Team.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""Test some methods for the internal engine."""
import unittest
import numpy as np
from pyretis.engines.internal import MDEngine, VelocityVerlet, Langevin
from pyretis.core.random_gen import MockRandomGenerator
from pyretis.orderparameter.orderparameter import Position
from .test_engines import prepare_test_system


class MockEngine(MDEngine):
    """Mock MD engine for testing."""

    def __init__(self, middle):
        """Set up the engine."""
        super().__init__(1, 'Mock engine for testing')
        self.middle = middle
        self.counter = 0

    def integration_step(self, system):
        """Do some fake integration steps."""
        particles = system.particles
        if self.counter < 5:
            particles.pos = np.ones_like(particles.pos) * (self.middle - 1)
            particles.vel = np.ones_like(particles.vel) * (self.middle - 1)
        elif 5 <= self.counter < 7:
            particles.pos = np.ones_like(particles.pos) * self.middle
            particles.vel = np.ones_like(particles.vel) * self.middle
        else:
            particles.pos = np.ones_like(particles.pos) * (self.middle + 1)
            particles.vel = np.ones_like(particles.vel) * (self.middle + 1)
        self.counter += 1


class TestKick(unittest.TestCase):
    """Test Kicking methods."""

    def test_kick_across_middle(self):
        """"Test test kick_across_middle method."""
        # Test with the Velocity Verlet engine:
        engine = VelocityVerlet(0.002)
        order_function = Position(0, dim='x', periodic=False)
        rgen = MockRandomGenerator(seed=1, norm_shift=True)
        system = prepare_test_system()
        tis_settings = {
            'maxlength': 1000,
            'sigma_v': -1,
            'aimless': True,
            'zero_momentum': False,
            'rescale_energy': False,
            'allowmaxlength': False,
        }
        interface = -1.123456789
        prev, curr = engine.kick_across_middle(system,
                                               order_function,
                                               rgen, interface,
                                               tis_settings)
        order_curr1 = engine.calculate_order(order_function, system)[0]
        order_curr2 = curr.particles.get_pos()[0][0]
        self.assertEqual(order_curr1, order_curr2)
        order_prev1 = prev.order
        order_prev2 = prev.particles.get_pos()[0][0]
        self.assertEqual(order_prev1, order_prev2)
        self.assertTrue(order_prev1 <= interface < order_curr1 or
                        order_curr1 < interface <= order_prev1)
        # Test with the Langevin engine:
        interface = -0.54321
        engine = Langevin(0.002, 0.3, rgen='mock', seed=1,
                          high_friction=False)
        prev, curr = engine.kick_across_middle(system,
                                               order_function,
                                               rgen, interface,
                                               tis_settings)
        order_curr1 = engine.calculate_order(order_function, system)[0]
        order_curr2 = curr.particles.get_pos()[0][0]
        self.assertEqual(order_curr1, order_curr2)
        order_prev1 = prev.order
        order_prev2 = prev.particles.get_pos()[0][0]
        self.assertEqual(order_prev1, order_prev2)
        self.assertTrue(order_prev1 <= interface < order_curr1 or
                        order_curr1 < interface <= order_prev1)
        # Test with a Mock Engine:
        interface = 3
        engine = MockEngine(interface)
        prev, curr = engine.kick_across_middle(system,
                                               order_function,
                                               rgen, interface,
                                               tis_settings)
        self.assertEqual(prev.order, 2)
        self.assertEqual(curr.order, 4)


if __name__ == '__main__':
    unittest.main()
