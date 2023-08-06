# -*- coding: utf-8 -*-
# Copyright (c) 2019, PyRETIS Development Team.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""Module for formatting path-trajectory data from PyRETIS.

Important classes defined here
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PathExtFormatter (:py:class:`.PathExtFormatter`)
    A class for formatting external trajectories. Since this format
    is intended for paths created by an external software it will
    simply contain locations for the files where the snapshots are
    stored.

PathIntFormatter (:py:class:`.PathIntFormatter`)
    A class for formatting internal trajectories. The format used is
    relatively simple and does not contain information about atoms,
    just the coordinates. The output for n-dimensional system contains
    2n columns (positions and velocities). This formatter is intended
    for use with objects like :py:class:`.Path`.

PathExtFile (:py:class:`.PathExtFile`)
    A class for writing path data for external paths.

PathIntFile (:py:class:`.PathIntFile`)
    A class for writing path data for internal paths.

"""
import logging
import os
import numpy as np
from pyretis.inout.formats.formatter import OutputFormatter
from pyretis.inout.fileio import FileIO, read_some_lines
logger = logging.getLogger(__name__)  # pylint: disable=invalid-name
logger.addHandler(logging.NullHandler())


__all__ = [
    'PathExtFormatter',
    'PathIntFormatter',
    'PathExtFile',
    'PathIntFile',
]


class PathIntFormatter(OutputFormatter):
    """A class for formatting internal trajectories."""

    _FMT = '{:15.9f}'

    def __init__(self):
        """Initialise the PathIntFormatter formatter."""
        super().__init__('PathIntFormatter', header=None)
        self.print_header = False
        self.fmt = None

    def format(self, step, data):
        """Format path data for internal paths.

        Parameters
        ----------
        step : integer
            The current simulation step.
        data : list
            Here, ``data[0]`` is assumed to be an object like
            :py:class:`.Path` and ``data[1]`` a string containing the
            status of this path.

        Yields
        ------
        out : string
            The trajectory (positions & velocities).

        """
        path, status = data[0], data[1]
        if not path:  # E.g. when null-moves are False.
            return
        yield '# Cycle: {}, status: {}'.format(step, status)
        for i, phasepoint in enumerate(path.phasepoints):
            yield 'Snapshot: {}'.format(i)
            pos = phasepoint.particles.get_pos()
            vel = phasepoint.particles.get_vel()
            for posj, velj in zip(pos, vel):
                if self.fmt is None:
                    self.fmt = ' '.join([self._FMT] * len(posj))
                yield ' '.join([self.fmt.format(*posj),
                                self.fmt.format(*velj)])

    @staticmethod
    def parse(line):
        """Parse positions and velocities from a single line.

        Parameters
        ----------
        line : string
            The line to parse.

        Returns
        -------
        pos : list of floats
            The positions read from the file.
        vel : list of floats
            The velocities read from the file.

        """
        raw = [float(i) for i in line.split()]
        dim = len(raw) // 2
        if not 1 <= dim <= 3:
            raise ValueError(
                'Malformed trajectory data: dim = {}?'.format(dim)
            )
        pos = raw[:dim]
        vel = raw[dim:2*dim]
        return pos, vel

    def read_snapshots(self, data):
        """Read snapshots from data.

        Parameters
        ----------
        data : list of strings
            The data we are reading into snapshots.

        Yields
        ------
        out : dict
            A dict representing the snapshot with positions and
            velocities.

        """
        pos, vel = [], []
        for line in data:
            if line.startswith('Snapshot'):
                # A new snapshot, store the old one:
                if pos:
                    yield {'pos': np.array(pos), 'vel': np.array(vel)}
                pos, vel = [], []
            else:
                new_pos, new_vel = self.parse(line)
                pos.append(new_pos)
                vel.append(new_vel)
        if pos:
            yield {'pos': np.array(pos), 'vel': np.array(vel)}

    def load(self, filename):
        """Load trajectories from a path file.

        Parameters
        ----------
        filename : string
            The path/file name of the file we want to open.

        Yields
        ------
        data : dict
            The trajectory & comment read from the path file.

        """
        for trajectory in read_some_lines(filename, line_parser=None):
            # These trajectories are just raw text,
            # convert to snapshots:
            traj = [i for i in self.read_snapshots(trajectory['data'])]
            data = {'comment': trajectory['comment'],
                    'data': traj}
            yield data


class PathExtFormatter(OutputFormatter):
    """A class for formatting external trajectories.

    The external trajectories as stored as files and this path
    formatter includes the location of these files.

    Attributes
    ----------
    FMT : string
        The string to use for the formatting.

    """

    FMT = '{:>10}  {:>20s}  {:>10}  {:>5}'

    def __init__(self):
        """Initialise the PathExtFormatter formatter."""
        header = {'labels': ['Step', 'Filename', 'index', 'vel'],
                  'width': [10, 20, 10, 5], 'spacing': 2}

        super().__init__('PathExtFormatter', header=header)
        self.print_header = False

    def format(self, step, data):
        """Format path data for external paths.

        Parameters
        ----------
        step : integer
            The current simulation step.
        data : list
            Here, ``data[0]`` is assumed to be an object like
            :py:class:`.Path`` and ``data[1]`` a string containing the
            status of this path.

        Yields
        ------
        out : string
            The trajectory as references to files.

        """
        path, status = data[0], data[1]
        if not path:  # E.g. when null-moves are False.
            return
        yield '# Cycle: {}, status: {}'.format(step, status)
        yield self.header
        for i, phasepoint in enumerate(path.phasepoints):
            filename, idx = phasepoint.particles.get_pos()
            filename_short = os.path.basename(filename)
            if idx is None:
                idx = 0
            vel = -1 if phasepoint.particles.get_vel() else 1
            yield self.FMT.format(i, filename_short, idx, vel)

    @staticmethod
    def parse(line):
        """Parse the line data by splitting text on spaces.

        Parameters
        ----------
        line : string
            The line to parse.

        Returns
        -------
        out : list
            The columns of data.

        """
        return [i for i in line.split()]


class PathExtFile(FileIO):
    """A class for writing path data."""

    def __init__(self, filename, file_mode, backup=True):
        """Create the path writer with correct format for external paths."""
        super().__init__(filename, file_mode, PathExtFormatter(),
                         backup=backup)


class PathIntFile(FileIO):
    """A class for writing path data."""

    def __init__(self, filename, file_mode, backup=True):
        """Create the path writer with correct format for internal paths."""
        super().__init__(filename, file_mode, PathIntFormatter(),
                         backup=backup)
