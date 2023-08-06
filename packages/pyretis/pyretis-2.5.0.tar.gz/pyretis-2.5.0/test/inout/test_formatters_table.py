# -*- coding: utf-8 -*-
# Copyright (c) 2019, PyRETIS Development Team.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""A test module for the table formatters."""
import logging
import os
import tempfile
import unittest
import numpy as np
from pyretis.core.pathensemble import PathEnsemble
from pyretis.inout.formats.txt_table import (
    TxtTableFormatter,
    PathTableFormatter,
    ThermoTableFormatter,
    RETISResultFormatter,
    txt_save_columns,
)
from .help import turn_on_logging


logging.disable(logging.CRITICAL)
HERE = os.path.abspath(os.path.dirname(__file__))


class TestTxtTableFormatter(unittest.TestCase):
    """Test that the table formatter works as intended."""

    def test_table_formatter(self):
        """Test the table formatter."""
        table = {
            'title': 'Test table formatter.',
            'var': ['step', 'temp', 'pot', 'ekin'],
            'format': {
                'labels': ['Step', 'Temperature', 'Potential energy',
                           'Kinetic energy'],
                'width': (10, 12),
                'spacing': 2,
                'row_fmt': ['{:> 10d}', '{:> 12.6g}'],
                }
        }
        formatter = TxtTableFormatter(table['var'], table['title'],
                                      **table['format'])
        rows = [
            {'temp': 300, 'pot': 1.0, 'ekin': 2.0},
            {'temp': 300.1, 'pot': 2.1, 'ekin': 3.1},
        ]
        self.assertEqual(
            formatter.header,
            '#     Step   Temperature  Potential energy  Kinetic energy',
        )
        correct = [
            '         1           300             1             2',
            '         2         300.1           2.1           3.1',
        ]
        for i, row in enumerate(rows):
            for line in formatter.format(i+1, row):
                self.assertEqual(line, correct[i])

    def test_table_formatter_missing(self):
        """Test the table formatter when some input is missing."""
        table = {
            'title': 'Test table formatter.',
            'var': ['step', 'temp', 'pot', 'ekin'],
            'format': {
                'labels': ['Step', 'Temperature', 'Potential energy',
                           'Kinetic energy'],
                }
        }
        formatter = TxtTableFormatter(table['var'], table['title'],
                                      **table['format'])
        rows = [
            {'temp': 500, 'pot': 5.0, 'ekin': 20.0},
            {'temp': 500.1, 'pot': 5.1, 'ekin': 30.1},
        ]
        self.assertEqual(
            formatter.header,
            '#       Step  Temperature Potential energy Kinetic energy'
        )
        correct = [
            '           1          500                5             20',
            '           2        500.1              5.1           30.1',
        ]
        for i, row in enumerate(rows):
            for line in formatter.format(i+1, row):
                self.assertEqual(line, correct[i])

    def test_table_formatter_short(self):
        """Test the table formatter when some labels are short."""
        table = {
            'title': 'Test table formatter.',
            'var': ['step', 'x', 'y', 'z'],
            'format': {
                'labels': ['Step', 'x', 'y', 'z'],
                'width': (10, 6),
                }
        }
        formatter = TxtTableFormatter(table['var'], table['title'],
                                      **table['format'])
        rows = [
            {'x': 1, 'y': 2, 'z': -1},
            {'x': 3.14, 'y': -2.71, 'z': -100.1},
        ]
        self.assertEqual(
            formatter.header,
            '#     Step      x      y      z',
        )
        correct = [
            '         1      1      2     -1',
            '         2   3.14  -2.71 -100.1',
        ]
        for i, row in enumerate(rows):
            for line in formatter.format(i+1, row):
                self.assertEqual(line, correct[i])


class TableFMTTest(unittest.TestCase):
    """Test that table writers work as intended."""

    def test_thermo_table(self):
        """Test the thermo table."""
        table = ThermoTableFormatter()
        data = dict(step=100, temp=1.2345, vpot=5.4321e3, ekin=2.222,
                    etot=3.456, press=1.011e9)
        line = ('       100        1.2345        5432.1         '
                '2.222         3.456     1.011e+09')
        for lines in table.format(100, data):
            self.assertMultiLineEqual(lines, line)
            break
        data = dict(step=100, temp=1.2345, vpot=5.4321e3, ekin=2.222,
                    etot=3.456, press=101.11111111)
        line = ('       100        1.2345        5432.1         '
                '2.222         3.456       101.111')
        for lines in table.format(100, data):
            self.assertMultiLineEqual(lines, line)
            break

    def test_path_table(self):
        """Test the path data table."""
        table = PathTableFormatter()
        ens = PathEnsemble(1, [-0.9, -0.9, 1.0])
        ens.nstats['npath'] = 10
        ens.nstats['nshoot'] = 8
        ens.nstats['ACC'] = 4
        ens.nstats['BWI'] = 3
        ens.nstats['FTL'] = 2
        ens.nstats['FTX'] = 1
        correct = ('       101             4             3             0'
                   '             2             0             1')
        for line in table.format(101, ens):
            self.assertEqual(line, correct)
            break

    def test_column_writer(self):
        """Test the column writer method."""
        with tempfile.NamedTemporaryFile() as temp:
            columns = [np.random.rand(10) for i in range(5)]
            txt_save_columns(temp.name, 'Test data', columns, backup=True)
            temp.flush()
        with tempfile.NamedTemporaryFile() as temp:
            columns = [np.random.rand(10-i) for i in range(5)]
            with turn_on_logging():
                with self.assertLogs('pyretis.inout.formats.txt_table',
                                     level='WARNING'):
                    txt_save_columns(temp.name, 'Test data', columns,
                                     backup=True)
            temp.flush()

    def test_retis_formatter(self):
        """Test the formatter for RETIS results."""

        formatter = RETISResultFormatter()
        ens = PathEnsemble(1, [-0.9, -0.9, 1.0])
        ens.nstats['npath'] = 10
        ens.nstats['nshoot'] = 8
        ens.nstats['ACC'] = 4
        ens.nstats['BWI'] = 3
        ens.nstats['FTL'] = 2
        ens.nstats['FTX'] = 1
        ens.paths = [
            {
                'generated': ('s-', 0, 0, 0), 'status': 'NCR', 'length': 69,
                'ordermax': (-0.8977260384533993, 32),
                'ordermin': (-0.9001050210610345, 0),
                'interface': ('L', '*', 'L'), 'cycle': 101}
        ]
        correct = [
            '# Results for path ensemble [0^+] at cycle 101:',
            ('# Generated path with status "NCR", move "swap from -" '
             'and length 69.'),
            '# Order parameter max was: -0.8977260384533993 at index 32.',
            '# Order parameter min was: -0.9001050210610345 at index 0.',
            '# Path ensemble statistics:',
            ('# Ensemble     Cycle    Accepted         BWI         BTL'
             '         FTL         BTX         FTX'),
            ('     [0^+]       101           4           3           0'
             '           2           0           1'),
            '\n',
        ]
        for linei, linej in zip(formatter.format(101, ens), correct):
            self.assertEqual(linei, linej)


if __name__ == '__main__':
    unittest.main()
