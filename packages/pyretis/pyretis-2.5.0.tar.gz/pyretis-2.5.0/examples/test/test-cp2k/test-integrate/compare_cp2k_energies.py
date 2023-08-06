# -*- coding: utf-8 -*-
# Copyright (c) 2019, PyRETIS Development Team.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""Compare energy output for CP2K."""
import sys
import colorama
from matplotlib import pyplot as plt
import numpy as np
from pyretis.inout import print_to_screen


plt.style.use('seaborn-poster')


def main(cp2k_file1, cp2k_file2, plot=False):
    """Perform the test."""
    print_to_screen('Reading energy file: {}'.format(cp2k_file1),
                    level='info')
    energy_cp2k1 = np.loadtxt(cp2k_file1)
    print_to_screen('Reading energy file: {}'.format(cp2k_file2),
                    level='info')
    energy_cp2k2 = np.loadtxt(cp2k_file2)

    mse_ok = obtain_mses(energy_cp2k1, energy_cp2k2)

    if plot:
        print_to_screen('\nPlotting for comparison', level='message')
        plot_comparison(energy_cp2k1, energy_cp2k2, cp2k_file1, cp2k_file2)

    if not mse_ok:
        print_to_screen('\nComparison failed!', level='error')
        sys.exit(1)


def obtain_mses(energy_cp2k1, energy_cp2k2, tol=1.0e-5):
    """Obtain some mean squared errors."""
    if not energy_cp2k1.shape == energy_cp2k2.shape:
        return False
    _, ncol = energy_cp2k1.shape
    for key in range(1, ncol - 1):  # last column is used time, skip it!
        term1 = (energy_cp2k1[key] - energy_cp2k2[key])**2
        term2 = (np.average(energy_cp2k2[key]) - energy_cp2k2[key])**2
        rse = term1.sum() / term2.sum()
        level = 'info'
        tol_ok = True
        if tol:
            tol_ok = abs(rse) < tol
            if not tol_ok:
                level = 'error'
        print_to_screen('RES {}: {}'.format(key, rse), level=level)
        if not tol_ok:
            return False
    return True


def plot_comparison(energy_cp2k1, energy_cp2k2, cp2k_file1, cp2k_file2):
    """Just plot some properties for the paths."""
    fig1 = plt.figure()
    ax11 = fig1.add_subplot(221)
    ax12 = fig1.add_subplot(222)
    ax21 = fig1.add_subplot(223)
    ax22 = fig1.add_subplot(224)
    plabel = 'CP2K ({})'.format(cp2k_file1)
    glabel = 'cp2k ({})'.format(cp2k_file2)

    ax11.plot(energy_cp2k1[:, 1], energy_cp2k1[:, 4],
              lw=4, ls='-', marker='o', label=plabel)
    ax11.plot(energy_cp2k2[:, 1], energy_cp2k2[:, 4],
              lw=2, ls='--', marker='^', label=glabel)
    ax11.legend()
    ax11.set_ylabel('Potential')

    ax12.plot(energy_cp2k2[:, 1], energy_cp2k2[:, 2],
              lw=4, ls='-', marker='o')
    ax12.plot(energy_cp2k2[:, 1], energy_cp2k2[:, 2],
              lw=2, ls='--', marker='^')
    ax12.set_ylabel('Kinetic')

    ax21.plot(energy_cp2k1[:, 1], energy_cp2k1[:, 5],
              lw=4, ls='-', marker='o')
    ax21.plot(energy_cp2k2[:, 1], energy_cp2k2[:, 5],
              lw=2, ls='--', marker='^')
    ax21.set_ylabel('Cons Qty')

    ax22.plot(energy_cp2k1[:, 1], energy_cp2k1[:, 3],
              lw=4, ls='-', marker='o')
    ax22.plot(energy_cp2k2[:, 1], energy_cp2k2[:, 3],
              lw=2, ls='--', marker='^')
    ax22.set_ylabel('Temperature')

    fig1.tight_layout()
    plt.show()


if __name__ == '__main__':
    colorama.init(autoreset=True)
    PLOT = len(sys.argv) > 3
    main(sys.argv[1], sys.argv[2], plot=PLOT)
