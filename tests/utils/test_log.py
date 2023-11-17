#!/usr/bin/env python3

"""
test_log.py: TODO: Headline...

TODO: Description...
"""

# Header.
__author__ = "Lennart Haack"
__email__ = "lennart-haack@mail.de"
__license__ = "GNU GPLv3"
__version__ = "0.0.1"
__build__ = "2023.1"
__date__ = "2023-11-07"
__status__ = "Prototype"

# Imports.
import logging
from unittest.mock import MagicMock, patch

import pytest

from oneguardai.utils import log


def test_log_count_increments_warning():
    log_count = log.LogCount()
    log_count.emit(logging.makeLogRecord({"levelname": "WARNING"}))
    assert log_count.warnings == 1


def test_log_count_increments_error():
    log_count = log.LogCount()
    log_count.emit(logging.makeLogRecord({"levelname": "ERROR"}))
    assert log_count.errors == 1


def test_log_count_increments_critical():
    log_count = log.LogCount()
    log_count.emit(logging.makeLogRecord({"levelname": "CRITICAL"}))
    assert log_count.criticals == 1


@patch('os.makedirs')
@patch('logging.getLogger')
def test_create_logger(mock_get_logger, mock_makedirs):
    mock_logger = MagicMock()
    mock_get_logger.return_value = mock_logger
    log.create(log.LogCount())
    mock_makedirs.assert_called_once()
    assert mock_logger.addHandler.call_count == 3
    assert mock_logger.setLevel.call_count == 1


@patch('os.makedirs')
@patch('logging.getLogger')
def test_create_logger_with_nonexistent_log_directory(mock_get_logger,
                                                      mock_makedirs
                                                      ):
    mock_logger = MagicMock()
    mock_get_logger.return_value = mock_logger
    mock_makedirs.side_effect = FileNotFoundError
    with pytest.raises(FileNotFoundError):
        log.create(log.LogCount())
