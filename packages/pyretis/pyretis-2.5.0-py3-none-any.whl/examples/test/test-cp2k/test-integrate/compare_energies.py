# -*- coding: utf-8 -*-
# Copyright (c) 2019, PyRETIS Development Team.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""Compare energy output for CP2K and PyRETIS."""
import sys
import colorama
from matplotlib import pyplot as plt
import numpy as np
from pyretis.inout import print_to_screen
from pyretis.inout.settings import parse_settings_file
from pyretis.inout.formats.cp2k import (
    read_cp2k_energy,
)


plt.style.use('seaborn-poster')


def main(energy_file, cp2k_file, plot=False):
    """Perform the test."""
    settings = parse_settings_file('cp2k.rst')
    timestep = settings['engine']['timestep']
    subcycles = settings['engine']['subcycles']

    print_to_screen('Reading energy file: {}'.format(energy_file),
                    level='info')
    energy = np.loadtxt(energy_file)
    print_to_screen('Reading CP2K energies from file: {}'.format(cp2k_file),
                    level='info')
    energy_cp2k = read_cp2k_energy(cp2k_file)

    energy_cp2k_mse = {key: val[::subcycles] for
                       key, val in energy_cp2k.items()}

    mse_ok = obtain_mses(energy, energy_cp2k_mse)

    if plot:
        print_to_screen('\nPlotting for comparison', level='message')
        plot_comparison(energy, energy_cp2k, energy_file, cp2k_file,
                        timestep*subcycles)

    if not mse_ok:
        print_to_screen('\nComparison failed!', level='error')
        sys.exit(1)


def obtain_mses(energy, energy_cp2k, tol=1.0e-5):
    """Obtain some mean squared errors."""
    pairs = ((1, 'vpot'), (2, 'ekin'), (3, 'etot'),
             (4, 'temp'))
    for pair in pairs:
        if not len(energy[:, pair[0]]) == len(energy_cp2k[pair[1]]):
            return False
        mse = ((energy[:, pair[0]] - energy_cp2k[pair[1]])**2).mean(axis=0)
        level = 'info'
        tol_ok = True
        if tol:
            tol_ok = abs(mse) < tol
            if not tol_ok:
                level = 'error'
        print_to_screen('MSE {}: {}'.format(pair[1], mse), level=level)
        if not tol_ok:
            return False
    return True


def plot_comparison(energy, energy_cp2k, energy_file, cp2k_file, delta_t):
    """Just plot some properties for the paths."""
    fig1 = plt.figure()
    ax11 = fig1.add_subplot(221)
    ax12 = fig1.add_subplot(222)
    ax21 = fig1.add_subplot(223)
    ax22 = fig1.add_subplot(224)
    plabel = 'PyRETIS ({})'.format(energy_file)
    glabel = 'CP2K ({})'.format(cp2k_file)
    time = np.arange(len(energy[:, 1])) * delta_t
    ax11.plot(time, energy[:, 1], lw=4, ls='-', marker='o', label=plabel)
    ax11.plot(energy_cp2k['time'], energy_cp2k['vpot'],
              lw=2, ls='--', marker='^', label=glabel)
    ax11.legend()
    ax11.set_ylabel('Potential')

    ax12.plot(time, energy[:, 2], lw=4, ls='-', marker='o')
    ax12.plot(energy_cp2k['time'], energy_cp2k['ekin'],
              lw=2, ls='--', marker='^')
    ax12.set_ylabel('Kinetic')

    ax21.plot(time, energy[:, 3], lw=4, ls='-', marker='o')
    ax21.plot(energy_cp2k['time'], energy_cp2k['etot'],
              lw=2, ls='--', marker='^')
    ax21.set_ylabel('Total')

    ax22.plot(time, energy[:, 4], lw=4, ls='-', marker='o')
    ax22.plot(energy_cp2k['time'], energy_cp2k['temp'],
              lw=2, ls='--', marker='^')
    ax22.set_ylabel('Temperature')

    fig1.tight_layout()
    plt.show()


if __name__ == '__main__':
    colorama.init(autoreset=True)
    PLOT = len(sys.argv) > 3
    main(sys.argv[1], sys.argv[2], plot=PLOT)
