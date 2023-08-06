# -*- coding: utf-8 -*-
# Copyright (c) 2019, PyRETIS Development Team.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""Animation of umbrella sampling."""
from matplotlib import pyplot as plt
from matplotlib import gridspec
import numpy as np
import colorama
from tqdm import tqdm, trange
from pyretis.inout import print_to_screen
from pyretis.core import System, RandomGenerator, create_box, Particles
from pyretis.simulation import UmbrellaWindowSimulation
from pyretis.forcefield import ForceField
from pyretis.forcefield.potentials import DoubleWell, RectangularWell
from pyretis.analysis.histogram import histogram, match_all_histograms


UMBRELLA_WINDOWS = [
    [-1.0, -0.4],
    [-0.5, -0.2],
    [-0.3, 0.0],
    [-0.1, 0.2],
    [0.1, 0.4],
    [0.3, 0.6],
    [0.5, 1.0]
]
RANDSEED = 1  # Seed for random number generator.
MINCYCLES = 10000  # Minimum number of cycles in each window.
MAXDX = 0.1  # Maximum allowed displacement in the MC step(s).
BINS = 100
HISTLIM = (-1.2, 1.2)
FIG_FREQ = 100  # How often we should store figures.
XLIM = (-1.2, 1.2)
SCALE_STEPS = 12  # Steps for animating the scaling.
XLIM_POT = (-1.2, 1.2)
YLIM_POT = (-0.3, 0.05)
BAR_FMT = {
    'window': ('Plotting window {n_fmt} of '
               '{total_fmt}|{bar}| [{elapsed}<{remaining}, {rate_fmt}]'),
    'scale': ('Scale step {n_fmt}/{total_fmt}|{bar}| '
              '[{elapsed}<{remaining}, {rate_fmt}]'),
    'pos': ('Step no. {n_fmt}/{total_fmt}|{bar}| '
            '[{elapsed}<{remaining}, {rate_fmt}]'),
    'window-scale': ('Re-scaling window {n_fmt} of {total_fmt}|{bar}| '
                     '[{elapsed}<{remaining}, {rate_fmt}]'),
}


def create_system():
    """Set up the system."""
    # Define system with a temperature in K:
    system = System(temperature=500, units='eV/K',
                    box=create_box(periodic=[False]))
    system.particles = Particles(dim=system.get_dim())
    # We will only have one particle in the system:
    system.add_particle(name='X', pos=np.array([-0.7]))
    # In this particular example, we are going to use
    # a simple double well potential:
    potential_dw = DoubleWell(a=1, b=1, c=0.02)
    # And a rectangular well potential:
    potential_rw = RectangularWell()
    # Set up the unbiased force field:
    forcefield = ForceField(
        'Double well',
        potential=[potential_dw],
        params=[{'a': 1.0, 'b': 1.0, 'c': 0.02}],
    )
    # Set up the biased potential:
    forcefield_bias = ForceField(
        'Double well with rectangular bias',
        potential=[potential_dw, potential_rw],
        params=[{'a': 1.0, 'b': 1.0, 'c': 0.02}, None]
    )
    # Attach biased force field to the system:
    system.forcefield = forcefield_bias
    return system, forcefield, forcefield_bias


def run_umbrella_simulation(system, settings, rgen):
    """Run a single umbrella simulation.

    Paramters
    ---------
    system : object like :class:`.System`
        The system we are running the simulation for.
    simulation_settings : dict
        A dictionary with settings for the simulation.
    rgen : object like :class:`.RandomGenerator`
        A random number generator we make use of in the simulation.

    Returns
    -------
    pos : numpy.array
        The accepted positions of the particle.
    trial : numpy.array
        The positions of all trial moves.
    success : list of boolean
        True if a move was accepted.
    ener : numpy.array
        The potential energy of the system.

    """
    # Move the bias according to the umbrella:
    params = {
        'left': settings['umbrella'][0],
        'right': settings['umbrella'][1]
    }
    system.forcefield.update_potential_parameters(
        system.forcefield.potential[1],  # This is the rectangular well.
        params
    )
    system.potential()  # Recalculate potential energy.
    simulation = UmbrellaWindowSimulation(
        system,
        settings['umbrella'],
        settings['over'],
        settings['maxdx'],
        rgen=rgen,
        mincycle=settings['mincycle'],
    )
    pos, trial, ener = [], [], []
    success = []
    for result in tqdm(simulation.run()):
        pos.append(system.particles.pos)
        trial.append(result['displace_step'][2])
        success.append(result['displace_step'][3])
        ener.append(system.particles.vpot)
    nstep = simulation.cycle['step'] - simulation.cycle['start']
    print_to_screen('Done. Cycles: {}'.format(nstep), level='success')
    return np.array(pos), np.array(trial), success, np.array(ener)


def run_simulation(system):
    """Run the simulation (all umbrellas)."""
    numb = len(UMBRELLA_WINDOWS)
    rgen = RandomGenerator(seed=RANDSEED)
    trajectory, energy = [], []  # To store all trajectories & energies.
    msg = '\nRunning umbrella no: {} of {}. Location: {}'
    # we run all the umbrella simulations by looping over
    # the different umbrellas we defined:
    print_to_screen('Starting simulations:', level='info')
    for i, window in enumerate(UMBRELLA_WINDOWS):
        print_to_screen(msg.format(i + 1, numb, window))
        # Get position that must be crossed:
        over = UMBRELLA_WINDOWS[min(i + 1, numb - 1)][0]
        # Collect settings:
        settings = {
            'umbrella': window,
            'over': over,
            'maxdx': MAXDX,
            'mincycle': MINCYCLES,
        }
        pos, trial, success, ener = run_umbrella_simulation(
            system,
            settings,
            rgen
        )
        trajectory.append([pos, trial, success])
        energy.append(ener)
    print_to_screen('Data collection done!', level='info')
    return trajectory, energy


def evaluate_potential(system, forcefield, positions):
    """Evaluate the potential energy.

    Parameters
    ----------
    system : object like :class:`.System`
        The system containing the particle position.
    forcefield : object like :class:`.ForceField`
        The force field with potential functions.
    positions : numpy.array
        The positions for which we will evaluate the potential.

    Returns
    -------
    out : numpy.array
        The potential energy

    """
    vpot = []
    for pos in positions:
        system.particles.pos = pos
        vpot.append(forcefield.evaluate_potential(system))
    return np.array(vpot)


def add_potential_plot(axes, system, forcefield):
    """Add the potential plot to the axes."""
    pos = np.linspace(-2, 2, 250)
    vpot = evaluate_potential(system, forcefield, pos)
    line_pot, = axes.plot(pos, vpot, lw=3)
    axv = axes.axvspan(xmin=-10, xmax=-10, alpha=0.1, color='#262626')
    scatter = axes.scatter(None, None, s=150, alpha=0.6, marker='o')
    scatter_trial = axes.scatter(None, None, s=150, c='black', alpha=0.6,
                                 marker='x')
    plot_obj = {
        'potential': line_pot,
        'window': axv,
        'scatter': scatter,
        'scatter_trial': scatter_trial,
    }
    return plot_obj


def add_histogram_plots(axes_hist, axes_all_hist, axes_hist_log):
    """Add histogram plot to the given axes."""
    counts = []
    probs = []
    histlog = []
    # Create empty histogram to get bins etc:
    for _ in range(len(UMBRELLA_WINDOWS)):
        hist, _, bin_mid = histogram([0], bins=BINS, limits=HISTLIM)
        delta_bin = bin_mid[1] - bin_mid[0]
        for axi, store in zip((axes_hist, axes_all_hist, axes_hist_log),
                              (counts, probs, histlog)):
            rects = axi.bar(bin_mid - 0.5 * delta_bin, hist, delta_bin,
                            alpha=0.5)
            store.append(rects)
            for rec in rects:
                rec.set_visible(False)
    plot_obj = {
        'counts': counts,
        'prob': probs,
        'histlog': histlog,
    }
    return plot_obj


def create_plots(system, forcefield):
    """Set up for plotting."""
    fig = plt.figure()
    grid = gridspec.GridSpec(2, 2)

    ax_pot = fig.add_subplot(grid[0, 0])
    ax_pot.set_ylabel('$V(x)$')
    ax_pot.set_xlabel('$x$')
    ax_pot.set_xlim(XLIM_POT)
    ax_pot.set_ylim(YLIM_POT)

    ax_hist = fig.add_subplot(grid[0, 1])
    ax_hist.set_xlabel('$x$')
    ax_hist.set_ylabel('No. of counts')
    ax_hist.set_xlim(XLIM)
    ax_hist.set_ylim(0.0, 1.0)

    ax_all_hist = fig.add_subplot(grid[1, 0])
    ax_all_hist.set_ylabel('Probability density')
    ax_all_hist.set_xlabel('$x$')
    ax_all_hist.set_xlim(XLIM)

    ax_hist_log = fig.add_subplot(grid[1, 1])
    ax_hist_log.set_visible(False)

    axes = {
        'pot': ax_pot,
        'hist': ax_hist,
        'hist-scaled': ax_all_hist,
        'hist-log': ax_hist_log
    }

    fig.subplots_adjust(left=0.1, bottom=0.2, right=0.90, top=0.90,
                        wspace=0.3, hspace=0.2)
    # Add some plot objects:

    plot_objects = {'figtxt': plt.figtext(0.05, 0.05, '')}
    pot_obj = add_potential_plot(ax_pot, system, forcefield)
    plot_objects.update(pot_obj)
    hist_obj = add_histogram_plots(ax_hist, ax_all_hist, ax_hist_log)
    plot_objects.update(hist_obj)
    fig.canvas.draw()
    return fig, axes, plot_objects


def update_window_plot(axes, axv, window):
    """Plot region for the given umbrella window."""
    region = np.array([[window[0], 0.0], [window[0], 1.0],
                       [window[1], 1.0], [window[1], 0.0],
                       [window[0], 0.0]])
    axv.set_xy(region)
    axes.draw_artist(axv)


def update_histogram(positions, axes, rects, store=None, density=False):
    """Update histograms according to the new data."""
    hist, bins, bin_mid = histogram(positions, bins=BINS, limits=HISTLIM,
                                    density=density)
    if density:
        ymax = max([histi[0].max() for histi in store] + [hist.max()])
        axes.set_ylim(0.0, ymax * 1.05)
    else:
        axes.set_ylim(0.0, hist.max() * 1.05)
    for rect, histi in zip(rects, hist):
        rect.set_height(histi)
        rect.set_visible(True)
    return hist, bins, bin_mid


def make_plots(system, forcefield, trajectory, energy):
    """Manage the creation of the plots."""
    fig, axes, plot_obj = create_plots(system, forcefield)
    all_histograms = plot_trials(fig, axes, plot_obj, system, forcefield,
                                 trajectory, energy)
    plot_scalings(fig, axes, plot_obj, system, forcefield, all_histograms)


def update_figure(fig, axes, artist):
    """Use blit to update the trial/accetpted position."""
    background = fig.canvas.copy_from_bbox(axes.bbox)
    fig.canvas.restore_region(background)
    axes.draw_artist(artist)
    fig.canvas.blit(axes.bbox)


def plot_trials(fig, axes, plot_obj, system, forcefield, trajectory, energy):
    """Plot the trial moves and corresponding histograms."""
    tot_step = 0  # Total number of steps done.
    all_histograms = []  # For storing all histograms.
    all_normed_histograms = []  # For storing all normed histograms.
    print_to_screen('Making plots for windows', level='success')
    for i in trange(len(UMBRELLA_WINDOWS), bar_format=BAR_FMT['window']):
        pos, trial, success = (trajectory[i][0], trajectory[i][1],
                               trajectory[i][2])
        ener = energy[i]
        update_window_plot(axes['pot'], plot_obj['window'],
                           UMBRELLA_WINDOWS[i])
        pos_so_far = []
        for j in trange(len(pos), bar_format=BAR_FMT['pos']):
            tot_step += 1
            pos_so_far.append(pos[j])

            if not success[j]:  # Add trial point:
                system.particles.pos = trial[j]
                vpot = forcefield.evaluate_potential(system)
                plot_obj['scatter_trial'].set_offsets([trial[j], vpot])
                plot_obj['scatter_trial'].set_visible(True)
            else:
                plot_obj['scatter_trial'].set_visible(False)
            if j % FIG_FREQ == 0:
                plot_obj['figtxt'].set_text(
                    'Total number of MC cycles: {}'.format(tot_step)
                )
                plot_obj['scatter'].set_offsets([pos[j], ener[j]])
                update_histogram(pos_so_far, axes['hist'],
                                 plot_obj['counts'][i])
                update_histogram(pos_so_far, axes['hist-scaled'],
                                 plot_obj['prob'][i],
                                 store=all_normed_histograms, density=True)
                update_figure(fig, axes['pot'], plot_obj['scatter'])
                fig.savefig('frame-{0:03d}-{1:05d}.png'.format(i, j))
        # Add final histograms:
        hist1 = update_histogram(pos_so_far, axes['hist'],
                                 plot_obj['counts'][i])
        all_histograms.append(hist1)
    return all_histograms


def plot_scalings(fig, axes, plot_obj, system, forcefield, all_histograms):
    """Plot the scaling for matched histograms."""
    _, scale_factors, hist_avg = match_all_histograms(
        all_histograms,
        UMBRELLA_WINDOWS,
    )
    axes['hist'].set_xlabel('$x$')
    axes['hist'].set_ylabel('Matching histograms')
    axes['hist-log'].set_xlim(XLIM)
    axes['hist-log'].set_yscale('log')
    axes['hist-log'].set_xlabel('$x$')
    axes['hist-log'].set_ylabel('Matching - logscale')
    axes['hist-log'].set_visible(True)
    plot_obj['figtxt'].set_text('Re-scaling histograms!')

    logmin = min(hist_avg[np.where(hist_avg > 0.0)[0]])

    for rects in plot_obj['counts']:
        for rec in rects:
            rec.visible = False

    for i in trange(len(UMBRELLA_WINDOWS), bar_format=BAR_FMT['window-scale']):
        hist, _, bin_mid = all_histograms[i]
        rects = plot_obj['counts'][i]
        rects_log = plot_obj['histlog'][i]
        if i == 0:
            axes['hist'].set_ylim(0.0, hist.max() * 1.05)
            axes['hist-log'].set_ylim(logmin / 10, hist.max() * 10)
            scales = np.ones(SCALE_STEPS)
        else:
            scales = np.linspace(1, scale_factors[i], SCALE_STEPS)
            plot_obj['figtxt'].set_text('Re-scaling histogram {}'.format(i))

        for j in trange(len(scales), bar_format=BAR_FMT['scale']):
            for rec, rec_log, histi in zip(rects, rects_log, hist):
                rec.set_height(histi * scales[j])
                rec_log.set_height(histi * scales[j])
                rec.set_visible(True)
                rec_log.set_visible(True)
            if j % 1 == 0:
                fig.savefig('scale-{0:03d}-{1:05d}.png'.format(i, j))
    plot_obj['figtxt'].set_text('Done with scaling: Calculating free energy')
    axes['hist'].plot(bin_mid, hist_avg, lw=6, color='orangered', alpha=0.65)
    axes['hist-log'].plot(bin_mid, hist_avg, lw=6, color='orangered',
                          alpha=0.65)

    free = -np.log(hist_avg) / system.temperature['beta']  # free energy
    free -= free.min()
    # Replot potential:
    pos = np.linspace(-2, 2, 250)
    vpot = evaluate_potential(system, forcefield, pos)
    vpot -= vpot.min()
    axes['pot'].plot(bin_mid, free, lw=6, color='orangered', alpha=0.65)

    where = np.where(np.logical_and(pos >= XLIM_POT[0], pos <= XLIM_POT[1]))[0]

    axes['pot'].set_ylim(-0.05, vpot[where].max())
    for obj in ('scatter', 'scatter_trial', 'window'):
        plot_obj[obj].set_visible(False)
    plot_obj['potential'].set_xdata(pos)
    plot_obj['potential'].set_ydata(vpot)
    fig.savefig('final.png')


def main():
    """Run the simulation and do the plotting'."""
    system, forcefield, _ = create_system()
    trajectory, energy = run_simulation(system)
    make_plots(system, forcefield, trajectory, energy)


if __name__ == '__main__':
    colorama.init(autoreset=True)
    main()
