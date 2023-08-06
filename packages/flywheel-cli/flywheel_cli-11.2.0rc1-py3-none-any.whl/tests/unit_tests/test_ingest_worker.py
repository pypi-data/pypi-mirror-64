from unittest import mock

import pytest

from flywheel_cli.ingest.worker import Worker


def test_ingest_worker_name_from_config():
    config = MockConfig()
    worker = Worker(config)
    assert worker.name == config.worker_name


def test_ingest_worker_name_explicit():
    config = MockConfig()
    worker = Worker(config, name="explicit-name")
    assert worker.name == "explicit-name"


class MockConfig:
    db_url = "sqlite:///:memory:"
    worker_name = "mock-worker-name"
