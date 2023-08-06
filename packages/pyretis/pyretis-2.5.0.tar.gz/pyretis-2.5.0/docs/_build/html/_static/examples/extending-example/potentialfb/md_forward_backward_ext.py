# -*- coding: utf-8 -*-
# Copyright (c) 2019, PyRETIS Development Team.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""
Example of running a MD NVE simulation.

Here we are running forward and then backward using a potential
written in FORTRAN or C. This can be selected below by the user.
"""

# pylint: disable=invalid-name
import sys
# For plotting:
from matplotlib import pyplot as plt
from matplotlib import gridspec
# PyRETIS imports:
from pyretis.core.units import create_conversion_factors
from pyretis.inout.setup import (create_simulation, create_force_field,
                                 create_system, create_engine)
from pyretis.inout.fileio import FileIO
from pyretis.inout.formats import ThermoTableFormatter
from pyretis.inout.plotting import mpl_set_style


# Define simulation settings:

klass = {'fortran': 'PairLennardJonesCutF',
         'cpython3': 'PairLennardJonesCutC'}
module = {'fortran': 'fortran/ljpotentialf.py',
          'cpython3': 'cpython3/ljpotentialc.py'}

USE = 'cpython3'  # or 'fortran'

settings = {}
settings['simulation'] = {
    'task': 'md-nve',
    'steps': 2000,
}
settings['system'] = {
    'units': 'lj',
    'temperature': 2.5,
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
    'trajectory-file': 1
}
settings['potential'] = [
    {'class': klass[USE],
     'module': module[USE],
     'parameter': {0: {'sigma': 1, 'epsilon': 1, 'factor': 2.5},
                   1: {'sigma': 1, 'epsilon': 1, 'factor': 2.5}},
     'shift': True}
]
settings['particles'] = {
    'position': {'file': 'initial.gro'},
    'velocity': {'generate': 'maxwell', 'momentum': True, 'seed': 0}
}

create_conversion_factors(settings['system']['units'])
print('# Creating system from settings.')
ljsystem = create_system(settings)
ljsystem.forcefield = create_force_field(settings)
kwargs = {'system': ljsystem, 'engine': create_engine(settings)}
simulation_nve = create_simulation(settings, kwargs)

# Set up extra output:
thermo_file = FileIO('thermo.txt', 'w', ThermoTableFormatter(), backup=False)
thermo_file.open()
store_results = []
# Also create some other outputs:
simulation_nve.set_up_output(settings, progress=False)
# Run the simulation forward:
for result in simulation_nve.run():
    stepno = result['cycle']['stepno']
    thermo_file.output(stepno, result['thermo'])
    result['thermo']['stepno'] = stepno
    store_results.append(result['thermo'])
# Run backward:
ljsystem.particles.vel *= -1.0
simulation_nve.extend_cycles(settings['simulation']['steps'] - 1)
for result in simulation_nve.run():
    stepno = result['cycle']['stepno']
    thermo_file.output(stepno, result['thermo'])
    result['thermo']['stepno'] = stepno
    store_results.append(result['thermo'])
thermo_file.close()

mpl_set_style()  # Load PyRETIS plotting style
step = [res['stepno'] for res in store_results]
pot_e = [res['vpot'] for res in store_results]
kin_e = [res['ekin'] for res in store_results]
tot_e = [res['etot'] for res in store_results]
pressure = [res['press'] for res in store_results]
temp = [res['temp'] for res in store_results]
# Plot some energies:
fig1 = plt.figure()
gs = gridspec.GridSpec(2, 2)
ax1 = fig1.add_subplot(gs[:, 0])
ax1.plot(step, pot_e, label='Potential')
ax1.plot(step, kin_e, label='Kinetic')
ax1.plot(step, tot_e, label='Total')
ax1.set_xlabel('Step no.')
ax1.set_ylabel('Energy per particle')
ax1.legend(loc='center left', prop={'size': 'small'})
ax2 = fig1.add_subplot(gs[0, 1])
ax2.plot(step, temp)
ax2.set_ylabel('Temperature')
ax3 = fig1.add_subplot(gs[1, 1])
ax3.plot(step, pressure)
ax3.set_xlabel('Step no.')
ax3.set_ylabel('Pressure')
fig1.subplots_adjust(bottom=0.12, right=0.95, top=0.95, left=0.12, wspace=0.3)
if 'noplot' not in sys.argv[1:]:
    plt.show()
