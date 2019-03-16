import platform
import unittest
import subprocess
import sys

from mock import patch
from pathlib import Path

import cv2

from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QMessageBox

from inselect.gui import copy_box
from inselect.gui.utils import (reveal_path, report_exception_to_user,
                                qimage_of_bgr)
from inselect.tests.utils import temp_directory_with_files

from .gui_test import GUITest


TESTDATA = Path(__file__).parent.parent / 'test_data'


class TestUtils(GUITest):
    """Test GUI utils
    """
    @unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
    @patch.object(subprocess, 'call', return_value=1)
    def test_reveal_path_windows(self, mock_subprocess):
        "User reveals a path"
        with temp_directory_with_files() as tempdir:
            path = tempdir / 'xyz'
            path.touch()
            reveal_path(path)
            expected = "explorer.exe /select,{0}".format(path.resolve())
            mock_subprocess.assert_called_once_with(expected)

    @unittest.skipUnless('Darwin' == platform.system(), "requires OS X")
    @patch.object(subprocess, 'check_call')
    def test_reveal_path_os_x(self, mock_subprocess):
        "User reveals a path"
        with temp_directory_with_files() as tempdir:
            path = tempdir / 'xyz'
            path.touch()
            reveal_path(path)
            expected = [
                '/usr/bin/osascript',
                '-e',
                'tell application "Finder" to reveal POSIX file "{0}"'.format(
                    str(path.resolve())
                )
            ]
            mock_subprocess.assert_any_call(expected)

    @patch.object(QMessageBox, 'exec_', return_value=QMessageBox.Ok)
    @patch.object(QMessageBox, 'setDetailedText')
    def test_exception_reported(self, mock_set_text, mock_exec_):
        "Exception is reported with details"
        try:
            raise ValueError('Something went wrong')
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            report_exception_to_user(exc_type, exc_value, exc_traceback)

        self.assertTrue(mock_exec_.called)
        expected = """in test_exception_reported
    raise ValueError('Something went wrong')
"""
        self.assertIn(expected, mock_set_text.call_args[0][0])

    @patch.object(
        copy_box, 'show_copy_details_box',
        side_effect=ValueError('Unable to show copy details box')
    )
    @patch.object(QMessageBox, 'critical', return_value=QMessageBox.Ok)
    def test_copy_box_raises(self, mock_critical, mock_show_copy_details_box):
        "Exception is reported using a plain message box"
        try:
            raise ValueError('Something went wrong')
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            report_exception_to_user(exc_type, exc_value, exc_traceback)

        self.assertIn(
            'An error occurred:\nSomething went wrong',
            mock_critical.call_args[0]
        )

    @patch.object(QImage, 'isNull', return_value=True)
    def test_qimage_of_bgr_null_qimage(self, mock_is_null):
        "QImage not created from BGR ndarray"
        self.assertRaises(
            ValueError,
            qimage_of_bgr,
            cv2.imread(str(TESTDATA.joinpath('shapes.png')))
        )
        mock_is_null.assert_called_once_with()

    def test_qimage_of_bgr(self):
        "QImage created from BGR ndarray"
        img = qimage_of_bgr(cv2.imread(str(TESTDATA.joinpath('shapes.png'))))
        self.assertEqual((459, 437), (img.width(), img.height()))

if __name__ == '__main__':
    unittest.main()
