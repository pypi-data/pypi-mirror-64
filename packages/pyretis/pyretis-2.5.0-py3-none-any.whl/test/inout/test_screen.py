# -*- coding: utf-8 -*-
# Copyright (c) 2019, PyRETIS Development Team.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""Test pyretis.inout.screen"""
import unittest
from unittest.mock import patch
from io import StringIO
from pyretis.inout.screen import ScreenOutput


class TestScreenOutput(unittest.TestCase):
    """Test the screen outputter."""

    def test_screen_output(self):
        """Test that the screen outputter works as intended."""
        screen = ScreenOutput(formatter=None)
        test = 'This is a test'
        with patch('sys.stdout', new=StringIO()) as txt:
            write = screen.write(test)
            self.assertTrue(write)
            self.assertEqual(test, txt.getvalue().strip())
        with patch('sys.stdout', new=StringIO()):
            write = screen.write(None)
            self.assertFalse(write)
        with patch('sys.stdout', new=StringIO()) as txt:
            write = screen.write(test, end='\n')
            self.assertTrue(write)
            self.assertEqual(test, txt.getvalue().split('\n')[0])


if __name__ == '__main__':
    unittest.main()
