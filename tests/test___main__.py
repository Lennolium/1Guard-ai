#!/usr/bin/env python3

"""
test___main__.py: TODO: Headline...

TODO: Description...
"""

# Header.
__author__ = "Lennart Haack"
__email__ = "lennart-haack@mail.de"
__license__ = "GNU GPLv3"
__version__ = "0.0.1"
__date__ = "2023-11-13"
__status__ = "Prototype/Development/Production"

# Imports.
from unittest.mock import patch

from oneguardai.__main__ import exception_handler, exit_handler, main


@patch('sys.exit')
def test_exit_handler_without_error(mock_exit):
    exit_handler()
    mock_exit.assert_called_once_with(0)


@patch('sys.exit')
def test_exit_handler_with_error(mock_exit):
    exit_handler(error=True)
    mock_exit.assert_called_once_with(1)


@patch('sys.exit')
def test_exception_handler_keyboard_interrupt(mock_exit):
    exception_handler(KeyboardInterrupt, None, None)
    mock_exit.assert_not_called()


@patch('sys.exit')
def test_exception_handler_uncaught_exception(mock_exit):
    exception_handler(Exception, None, None)
    mock_exit.assert_called_once_with(1)


@patch('signal.signal')
@patch('oneguardai.__main__.LOGGER')
def test_main(mock_logger, mock_signal):
    main()
    assert mock_logger.info.call_count == 5
    assert mock_signal.call_count == 3
