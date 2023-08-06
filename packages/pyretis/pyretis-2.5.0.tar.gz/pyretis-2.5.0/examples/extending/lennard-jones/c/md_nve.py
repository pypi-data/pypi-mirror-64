# -*- coding: utf-8 -*-
# Copyright (c) 2019, PyRETIS Development Team.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""Example of running a MD NVE simulation.

The system considered is a simple Lennard-Jones fluid.
"""
# pylint: disable=invalid-name
from pyretis.core.units import create_conversion_factors
from pyretis.inout.setup import (
    create_simulation,
    create_system,
    create_engine,
    create_force_field,
)
from pyretis.inout.fileio import FileIO
from pyretis.inout.formats import ThermoTableFormatter
settings = {}
settings['simulation'] = {
    'task': 'md-nve',
    'steps': 1000
}
settings['system'] = {
    'units': 'lj',
    'temperature': 2.0,
    'dimensions': 3
}
settings['engine'] = {
    'class': 'velocityverlet',
    'timestep': 0.002
}
settings['output'] = {
    'backup': 'overwrite',
    'energy-file': 1,
    'screen': 10,
    'trajectory-file': 10
}
settings['potential'] = [
    {'class': 'PairLennardJonesCutC',
     'module': 'ljpotentialc.py',
     'dim': 3,
     'shift': True,
     'parameter': {0: {'sigma': 1, 'epsilon': 1, 'factor': 2.5}}}
]
settings['particles'] = {
    'position': {'generate': 'fcc', 'repeat': [3, 3, 3], 'density': 0.9},
    'velocity': {'generate': 'maxwell', 'momentum': True, 'seed': 0}
}
create_conversion_factors(settings['system']['units'])
print('# Creating system from settings.')
ljsystem = create_system(settings)
ljsystem.forcefield = create_force_field(settings)
print('# Creating simulation from settings.')
sim_args = {'system': ljsystem, 'engine': create_engine(settings)}
simulation_nve = create_simulation(settings, sim_args)
print('# Creating output tasks from settings.')
simulation_nve.set_up_output(settings, progress=False)
msg = 'Created fcc grid with {} atoms.'
print(msg.format(ljsystem.particles.npart))
# set up extra output:
thermo_file = FileIO('thermo-test.txt', 'w', ThermoTableFormatter())
thermo_file.open()
store_results = []
# run the simulation :-)
for result in simulation_nve.run():
    stepno = result['cycle']['stepno']
    thermo_file.output(stepno, result['thermo'])
    result['thermo']['stepno'] = stepno
    store_results.append(result['thermo'])
thermo_file.close()
