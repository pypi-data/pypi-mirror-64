# -*- coding: utf-8 -*-
# Copyright (c) 2019, PyRETIS Development Team.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""Methods that will output results from the analysis functions.

The Methods defined here will also run the analysis and output
according to given settings.

Important methods defined here
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

analyse_file (:py:func:`.analyse_file`)
    Method to analyse a file. For example, it can be used as

    >>> from pyretis.inout.analysisio import analyse_file
    >>> result, raw_data = analyse_file('cross', 'cross.txt', settings)

    To output the results, for instance by plotting, one can do:

    >>> figures = output_results(file_type, plotter, result, raw_data)
    >>> txt_file = output_results(file_type, txt_plotter, result, raw_data)


run_analysis_files (:py:func:`.run_analysis_files`)
    Methods to the analysis on a set of files. It will create output
    that can be used for reporting.
"""
import logging
import os
from pyretis.core.units import create_conversion_factors
from pyretis.core.pathensemble import generate_ensemble_name
from pyretis.analysis import (analyse_flux, analyse_energies, analyse_orderp,
                              analyse_path_ensemble, match_probabilities,
                              retis_flux, retis_rate)
from pyretis.inout import print_to_screen
from pyretis.inout.formats.formatter import format_number
from pyretis.inout.plotting import create_plotter
from pyretis.inout.plotting import TxtPlotter
from pyretis.inout.report import generate_report
from pyretis.inout.settings import (SECTIONS, copy_settings)
from pyretis.inout.formats.pathensemble import PathEnsembleFile
from pyretis.inout.formats.energy import EnergyFile
from pyretis.inout.formats.order import OrderFile
from pyretis.inout.formats.cross import CrossFile
from pyretis.inout.simulationio import OUTPUT_TASKS
logger = logging.getLogger(__name__)  # pylint: disable=invalid-name
logger.addHandler(logging.NullHandler())


__all__ = ['analyse_file', 'run_analysis_files']


_ANALYSIS_FUNCTIONS = {'cross': analyse_flux,
                       'order': analyse_orderp,
                       'energy': analyse_energies,
                       'pathensemble': analyse_path_ensemble}


# Input files for analysis
_FILES = {'md-flux': {},
          'md-nve': {},
          'md': {},
          'tis': {},
          'tis-multiple': {},
          'retis': {}}
# Add files
for key in ('cross', 'energy', 'order'):
    _FILES['md-flux'][key] = OUTPUT_TASKS[key]['filename']
for key in ('energy',):
    _FILES['md-nve'][key] = OUTPUT_TASKS[key]['filename']
    _FILES['md'][key] = OUTPUT_TASKS[key]['filename']
for key in ('pathensemble',):
    for key2 in ('tis-multiple', 'tis', 'retis'):
        _FILES[key2][key] = OUTPUT_TASKS[key]['filename']


def run_analysis(settings):
    """Run a predefined analysis task.

    Parameters
    ----------
    settings : dict
        Simulation settings and settings for the analysis.

    Returns
    -------
    out : dict
        A dictionary with the results from the analysis. This dict
        can be used to generate a report.

    """
    runners = {'retis': run_retis_analysis,
               'tis': run_tis_analysis,
               'tis-multiple': run_tis_analysis,
               'md-flux': run_mdflux_analysis}
    sim = settings['simulation']
    sim_task = sim['task'].lower()
    report_dir = settings['analysis'].get('report-dir', None)
    plotter = create_plotter(settings['analysis']['plot'],
                             out_dir=report_dir)
    backup = settings['output'].get('backup', SECTIONS['output']['backup'])
    txt_plotter = TxtPlotter(settings['analysis']['txt-output'],
                             backup=backup,
                             out_dir=report_dir)
    if sim_task in runners.keys():
        runner = runners[sim_task]
        return runner(settings, plotter, txt_plotter)
    msgtxt = 'Unknown analysis task "{}" requested!'.format(sim_task)
    logger.error(msgtxt)
    raise ValueError(msgtxt)


def get_path_ensemble_files(ensemble, settings, detect,
                            interfaces):
    """Return files for a single path ensemble.

    Here, we will return the files needed to analyse a single path
    ensemble and we will also return settings which can be used for
    the analysis.

    Parameters
    ----------
    ensemble : int
        This is the integer representing the ensemble.
    settings : dict
        The settings to use for an analysis/simulation
    detect : float or None
        The interface use for detecting if a path is successful for not.
    interfaces : list of floats
        The interfaces used for this particular path simulation.

    Returns
    -------
    local_settings : dict
        This dict contains settings which can be used for a initial
        flux analysis.
    files : list of tuples
        The tuples in this list are the files which can be analysed
        further, using the settings in `out[0]`.

    """
    sim_task = settings['simulation']['task'].lower()
    lsetting = copy_settings(settings)
    lsetting['simulation']['interfaces'] = interfaces
    lsetting['tis']['detect'] = detect
    lsetting['tis']['ensemble_number'] = ensemble
    files = []
    for file_type in _FILES[sim_task]:
        filename = os.path.join(generate_ensemble_name(ensemble),
                                _FILES[sim_task][file_type])
        if os.path.isfile(filename):
            files.append((file_type, filename))
            logger.debug('Adding file "%s" for analysis', filename)
        else:
            logger.debug('Could not find file %s', filename)
    return lsetting, files


def get_path_simulation_files(sim_settings):
    """Set up for analysis of TIS and RETIS simulations.

    For these kinds of simulations, we expect to analyse several
    directories with raw-data. For TIS we expect to find a directory
    with raw-data for the initial flux (named ``flux``) and the
    directories for the path simulations (named ``001``, ``002`` etc.
    for ensembles [0^+], [1^+] and so on). For RETIS, we expect to
    find the same directories but with a ``000`` (for the ``[0^-]``
    ensemble) rather than the ``flux`` directory.

    Parameters
    ----------
    sim_settings : dict
        The settings used for the (RE)TIS simulation(s). These settings
        are used to get the interfaces used and the path ensembles
        defined by these interfaces.

    Returns
    -------
    all_settings : list of dict
        This dict in this list contains settings which can be used for
        the analysis.
    all_files : list of lists of tuples
        `all_files[i]` is a list of files from path ensemble
        simulation `i`. For TIS, `all_files[0]` should be the files
        obtained in the initial flux simulation. These files can be
        analysed using the settings in `all_settings[i]`.

    """
    # Check if we can do flux analysis:
    all_files, all_settings = [], []
    interfaces = sim_settings['simulation']['interfaces']
    reactant = interfaces[0]
    product = interfaces[-1]
    if sim_settings['simulation']['task'] == 'tis-multiple':
        all_files.append(None)
        all_settings.append(None)
    else:  # just add the 0 ensemble
        detect = None
        interface = [-float('inf'), reactant, reactant]
        setts, files = get_path_ensemble_files(0, sim_settings, detect,
                                               interface)
        all_files.append(files)
        all_settings.append(setts)
    for i, middle in enumerate(interfaces[:-1]):
        try:
            detect = interfaces[i + 1]
        except IndexError:
            detect = product
        interface = [reactant, middle, product]
        setts, files = get_path_ensemble_files(i + 1, sim_settings, detect,
                                               interface)
        all_files.append(files)
        all_settings.append(setts)
    return all_settings, all_files


def print_value_error(heading, value, rel_error, level=None):
    """Print out the matched probabilities."""
    val = format_number(value, 0.1, 100)
    msgtxt = '{}: {}'.format(heading, val)
    print_to_screen(msgtxt.strip(), level=level)
    fmt_scale = format_number(rel_error * 100, 0.1, 100)
    msgtxt = '(Relative error: {} %)'.format(fmt_scale.rstrip())
    print_to_screen(msgtxt, level=level)


def run_single_tis_analysis(settings, plotter, txt_plotter):
    """Run the analysis for a single TIS ensemble.

    Parameters
    ----------
    settings : dict
        The settings to use for an analysis/simulation.
    plotter : object like :py:class:`.Plotter`
        This is the object that handles the plotting.
    txt_plotter : object like :py:class:`.Plotter`
        This is the object that handles the text output.

    Returns
    -------
    out : list or dict or similar
        The output from the analysis.

    """
    sim = settings['simulation']
    tis = settings['tis']
    sett, files = get_path_ensemble_files(tis['ensemble_number'],
                                          settings,
                                          tis['detect'],
                                          sim['interfaces'])
    msgtxt = 'Analysing ensemble {}'.format(tis['ensemble_number'])
    print_to_screen(msgtxt, level='info')
    print_to_screen()
    result = run_analysis_files(sett, files, plotter, txt_plotter)
    report_txt = generate_report('tis', result, output='txt')[0]
    print_to_screen(''.join(report_txt))
    print_to_screen()
    return result


def run_tis_analysis(settings, plotter, txt_plotter):
    """Run the analysis for TIS.

    Parameters
    ----------
    settings : dict
        The settings to use for an analysis/simulation.
    plotter : object like :py:class:`.Plotter`
        This is the object that handles the plotting.
    txt_plotter : object like :py:class:`.Plotter`
        This is the object that handles the text output.

    Returns
    -------
    out : list or dict or similar
        The output from the analysis.

    """
    if settings['simulation']['task'] == 'tis':
        return run_single_tis_analysis(settings, plotter, txt_plotter)
    results = {'cross': None, 'pathensemble': [], 'matched': None}
    all_settings, all_files = get_path_simulation_files(settings)
    nens = len(all_settings) - 1
    for i, (sett, files) in enumerate(zip(all_settings, all_files)):
        if i == 0:
            msgtxt = ('Initial flux is not calculated here.\n'
                      'Remember to calculate this separately!')
            logger.info(msgtxt)
            print_to_screen(msgtxt, level='warning')
        else:
            msgtxt = 'Analysing ensemble {} of {}'.format(i, nens)
            print_to_screen(msgtxt, level='info')
            print_to_screen()
            result = run_analysis_files(sett, files, plotter, txt_plotter)
            results['pathensemble'].append(result['pathensemble'])
            report_txt = generate_report('tis', result,
                                         output='txt')[0]
            print_to_screen(''.join(report_txt))
            print_to_screen()
    # match probabilities:
    out, fig, txt = analyse_and_output_matched(results['pathensemble'],
                                               plotter, txt_plotter,
                                               settings)
    results['matched'] = {'out': out, 'figures': fig, 'txtfile': txt}
    print_to_screen('Overall results', level='success')
    print_to_screen('===============', level='success')
    print_to_screen()
    print_value_error('TIS Crossing probability',
                      out['prob'], out['relerror'], level='success')
    return results


def run_retis_analysis(settings, plotter, txt_plotter):
    """Run the analysis for RETIS.

    Parameters
    ----------
    settings : dict
        The settings to use for an analysis/simulation.
    plotter : object like :py:class:`.Plotter`
        This is the object that handles the plotting.
    txt_plotter : object like :py:class:`.Plotter`
        This is the object that handles the text output.

    """
    units = settings['system']['units']
    if 'unit-system' in settings:
        create_conversion_factors(units, **settings['unit-system'])
    else:
        create_conversion_factors(units)
    all_settings, all_files = get_path_simulation_files(settings)
    results = {'cross': None,
               'pathensemble': [],
               'matched': None}
    nens = len(all_settings) - 1
    print_to_screen()
    for i, (sett, files) in enumerate(zip(all_settings, all_files)):
        msgtxt = 'Analysing ensemble {} of {}'.format(i, nens)
        print_to_screen(msgtxt, level='info')
        print_to_screen()
        if i == 0:
            result = run_analysis_files(sett, files, plotter, txt_plotter)
            results['pathensemble0'] = result['pathensemble']
            report_txt = generate_report('retis0', result, output='txt')[0]
            print_to_screen(''.join(report_txt))
            print_to_screen()
        else:
            result = run_analysis_files(sett, files, plotter, txt_plotter)
            results['pathensemble'].append(result['pathensemble'])
            report_txt = generate_report('tis', result,
                                         output='txt')[0]
            print_to_screen(''.join(report_txt))
            print_to_screen()
    # flux first:
    time_subcycles = settings['engine'].get('subcycles', 1)
    timestep = settings['engine']['timestep'] * time_subcycles
    flux, flux_error = retis_flux(results['pathensemble0']['out'],
                                  results['pathensemble'][0]['out'],
                                  timestep)
    results['flux'] = {'value': flux, 'error': flux_error,
                       'unit': units}
    # match probabilities:
    out, fig, txt = analyse_and_output_matched(results['pathensemble'],
                                               plotter, txt_plotter,
                                               settings,
                                               flux=flux)
    results['matched'] = {'out': out, 'figures': fig, 'txtfile': txt}
    rate, rate_error = retis_rate(out['prob'], out['relerror'],
                                  flux, flux_error)
    results['rate'] = {'value': rate, 'error': rate_error,
                       'unit': units}
    print_to_screen('Overall results', level='success')
    print_to_screen('===============', level='success')
    print_to_screen()
    print_value_error('RETIS Crossing probability',
                      out['prob'], out['relerror'], level='success')
    print_to_screen()
    print_value_error('Initial flux (units 1/{})'.format(units), flux,
                      flux_error, level='success')
    print_to_screen()
    print_value_error('Rate constant (units 1/{})'.format(units), rate,
                      rate_error, level='success')
    return results


def run_mdflux_analysis(settings, plotter, txt_plotter):
    """Run the analysis for the md flux simulation.

    Parameters
    ----------
    settings : dict
        The settings to use for an analysis/simulation.
    plotter : object like :py:class:`.Plotter`
        This is the object that handles the plotting.
    txt_plotter : object like :py:class:`.Plotter`
        This is the object that handles the text output.

    Returns
    -------
    out : list or dict or similar
        The output from the analysis.

    """
    sim = settings['simulation']
    sim_task = sim['task']
    files = []
    for file_type in _FILES[sim_task]:
        filename = _FILES[sim_task][file_type]
        if os.path.isfile(filename):
            files.append((file_type, filename))
    msgtxt = 'Running analysis of a MD flux simulation...'
    print_to_screen(msgtxt, level='info')
    print_to_screen()
    result = run_analysis_files(settings, files, plotter, txt_plotter)
    report_txt = generate_report('md-flux', result, output='txt')[0]
    print_to_screen(''.join(report_txt))
    print_to_screen()
    return result


def run_analysis_files(settings, files, plotter, txt_plotter):
    """Run the analysis on a collection of files.

    Parameters
    ----------
    settings : dict
        This dict contains settings which dictate how the
        analysis should be performed and it should also contain
        information on how the simulation was performed.
    files : list of tuples
        This list contains the raw files to be analysed. The
        tuples are on format ('filetype', 'filename').
    plotter : object like :py:class:`.Plotter`
        This is the object that handles the plotting.
    txt_plotter : object like :py:class:`.Plotter`
        This is the object that handles the text output.

    Returns
    -------
    out: dict
        The results from the analysis.

    """
    results = {}
    for (file_type, file_name) in files:
        result, raw_data = analyse_file(file_type, file_name, settings)
        figures = output_results(file_type, plotter, result, raw_data)
        txt_file = output_results(file_type, txt_plotter, result, raw_data)
        results[file_type] = {'out': result,
                              'figures': figures,
                              'txtfile': txt_file}
    return results


def read_first_block(file_type, file_name):
    """Read the first block of data from a file.

    This method will read the first block of data from a file and
    immediately return.

    Parameters
    ----------
    file_type : string
        A string used for selecting the file object to use here.
    file_name : string
        The file to open.

    Returns
    -------
    out : numpy.array
        The raw data read from the file.

    """
    first_block = None
    class_map = {'energy': EnergyFile, 'order': OrderFile, 'cross': CrossFile}
    try:
        klass = class_map[file_type]
    except KeyError:
        logger.error(
            'Unknown file type "%s" requested for analysis.',
            file_type
        )
        raise ValueError('Unknown file type requested in analysis.')
    with klass(file_name, 'r') as fileobj:
        for block in fileobj.load():
            if first_block is None:
                first_block = block
            else:
                logger.warning(
                    (
                        'Noticed a second block in the input file "%s".\n'
                        'This will be ignored by the flux analysis.\n'
                        'Are you are running the analysis with '
                        'the correct input?'
                    ),
                    file_name
                )
                break
    if first_block is None:
        return None
    return first_block['data']


def output_results(file_type, plotter, result, rawdata):
    """Plot the results.

    Plotting might here refer to both figures and text.

    Parameters
    ----------
    file_type : string
        This determines what we are going to plot.
    plotter : object like :py:class:`.Plotter`
        This is the object that handles the plotting.
    result : list of lists or dicts
        This contains the results from a specific analysis.
    rawdata : list of floats, lists or objects
        The raw data with analysis results.

    Returns
    -------
    out : list of strings
        These are the files that the plotter created.

    """
    if file_type == 'cross':
        return plotter.output_flux(result)
    if file_type == 'order':
        return plotter.output_orderp(result, rawdata)
    if file_type == 'energy':
        return plotter.output_energy(result, rawdata)
    if file_type == 'pathensemble':
        return plotter.output_path(result, rawdata)
    return None


def analyse_file(file_type, file_name, settings):
    """Run analysis on the given file.

    This function is included for convenience so that we can call an
    analysis like ``analyse_file('cross', 'cross.txt')`` i.e. it should
    automatically open the file and apply the correct analysis
    according to a given file type. Here we return a function to do the
    analysis, so we are basically wrapping one of the analysis
    functions. This is done in case we wish to rerun the analysis but
    with different settings for instance.

    Parameters
    ----------
    file_type : string
        This is the type of file we are to analyse.
    file_name : string
        The file name to open.
    settings : dict
        This dict contains settings which dictate how the
        analysis should be performed and information on how the
        simulation was performed.

    Returns
    -------
    results : list or dict
        The output from the analysis
    raw_data : list, numpy.array or another type of object
        The raw data used in the analysis.

    """
    function = _ANALYSIS_FUNCTIONS.get(file_type, None)
    if function is None:
        msgtxt = 'Unknown file type "{}" requested!'.format(file_type)
        logger.error(msgtxt)
        raise ValueError(msgtxt)
    results, raw_data = None, None
    if file_type in ('energy', 'order', 'cross'):
        # Read the first block of raw data and analyse it:
        raw_data = read_first_block(file_type, file_name)
        results = function(raw_data, settings)
    elif file_type == 'pathensemble':
        # Create a PathEnsembleFile object to use for the analysis.
        ensemble_settings = {
            'ensemble_number': settings['tis']['ensemble_number'],
            'interfaces': settings['simulation']['interfaces'],
            'detect': settings['tis']['detect'],
        }
        raw_data = PathEnsembleFile(file_name, 'r', ensemble_settings)
        results = function(raw_data, settings)
    return results, raw_data


def analyse_and_output_matched(raw_data, plotter, txt_plotter,
                               settings=None, flux=None):
    """Analyse and output matched probability.

    This will calculate the over-all crossing probability by combining
    results from many path simulations.

    Parameters
    ----------
    raw_data : list, numpy.array or another type of object
        The raw data used in the analysis.
    plotter : object like :py:class:`.Plotter`
        This is the object that handles the plotting.
    txt_plotter : object like :py:class:`.Plotter`
        This is the object that handles the text output.
    settings : dict
        This dictionary contains settings for the analysis.
        Here we make use of the following keys from the
        analysis section:

        * `ngrid`: The number of grid points for calculating the
          crossing probability as a function of the order parameter.
        * `maxblock`: The max length of the blocks for the block error
          analysis. Note that this will maximum be equal the half of the
          length of the data, see `block_error` in `.analysis`.
        * `blockskip`: Can be used to skip certain block lengths.
          A `blockskip` equal to `n` will consider every n'th block up
          to `maxblock`, i.e. it will use block lengths equal to `1`,
          `1+n`, `1+2n`, etc.
        * `bins`: The number of bins to use for creating histograms.

    flux : float, optional
        The computed flux to be used only in RETIS if the running average
        of the computed rate is desired.

    Returns
    -------
    out[0] : dict
        This dict contains the results from the analysis
    out[1] : list of dicts
        A dictionary with the figure files created (if any).
    out[2] : list of strings
        A list with the text files created (if any).

    """
    path_results, ensemble_names, detect = [], [], []
    interface_left = None
    for ensemble in raw_data:
        path_results.append(ensemble['out'])
        ensemble_names.append(ensemble['out']['ensemble'])
        detect.append(ensemble['out']['detect'])
        if interface_left is None:
            interface_left = ensemble['out']['interfaces'][0]
    result = match_probabilities(path_results, detect, settings)
    if flux is not None:
        result['overall-rrun'] = flux*result['overall-prun']
    # for the figure, we add the A interface:
    detect_plot = [interface_left] + detect
    figures = plotter.output_matched_probability(ensemble_names,
                                                 detect_plot,
                                                 result)
    outtxt = txt_plotter.output_matched_probability(ensemble_names,
                                                    detect,
                                                    result)
    return result, figures, outtxt
