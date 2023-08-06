# -*- coding: utf-8 -*-
# Copyright (c) 2019, PyRETIS Development Team.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""Methods for analysing energy data from simulations.

Important methods defined here
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

analyse_energies (py:func:`.analyse_energies`)
    Run the analysis for energies (kinetic, potential etc.).
"""
import numpy as np
from scipy.stats import gamma
from pyretis.analysis.analysis import analyse_data


__all__ = ['analyse_energies']


def analyse_energies(energies, settings):
    """Run the energy analysis on several energy types.

    The function will run the energy analysis on several energy types
    and collect the energies into a structure which is convenient for
    plotting the results.

    Parameters
    ----------
    energies : dict
        This dict contains the energies to analyse.
    settings : dict
        This dictionary contains settings for the analysis.

    Returns
    -------
    results : dict
        For each energy key `results[key]` contains the result from the
        energy analysis.

    See Also
    --------
    :py:func:`.analyse_data` in :py:mod:`pyretis.analysis.analysis.py`.

    """
    results = {}
    for key in energies:
        results[key] = analyse_data(energies[key], settings)
    # For the energy analysis it is also useful to add some
    # theoretical distributions:
    alp = (0.5 * settings['particles']['npart'] *
           settings['system']['dimensions'])
    scale = {'ekin': 1.0 / settings['system']['beta'],
             'temp': settings['system']['temperature'] / alp}
    for key in scale:
        if key in results:
            dist = results[key]['distribution']
            pos = np.linspace(min(0.0, dist[1].min()), dist[1].max(), 1000)
            tdist = gamma.pdf(pos, alp, loc=0, scale=scale[key])
            results[key]['boltzmann-dist'] = [tdist, pos, (0.0, scale[key])]
    return results
