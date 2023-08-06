from unittest import mock

import pytest

from flywheel_cli.ingest import deid, schemas


def test_deid_logger_write_entry():
    write_func = mock.Mock()
    logger = deid.DeidLogger(write_func)
    logger.write_entry({
        "path": "path/to/1.dcm",
        "type": "before",
        "PatientName": "Name",
    })
    assert list(logger.temp_logs["path/to/1.dcm"].keys()) == ["PatientName"]
    write_func.assert_not_called()
    logger.write_entry({
        "path": "path/to/1.dcm",
        "type": "after",
        "PatientName": "-",
    })
    assert not logger.temp_logs.get("path/to/1.dcm")
    write_func.assert_called_once()
    args, _ = write_func.call_args
    assert len(args) == 1
    assert isinstance(args[0], schemas.DeidLogIn)
    assert args[0].src_path == "path/to/1.dcm"
    assert args[0].tags_before["PatientName"] == "Name"
    assert args[0].tags_after["PatientName"] == "-"
