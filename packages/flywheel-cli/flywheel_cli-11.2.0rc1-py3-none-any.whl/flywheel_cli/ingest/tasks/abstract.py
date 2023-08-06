"""Provides the abstract Task class."""
import logging
from abc import ABC, abstractmethod

from ..client import DBClient
from .. import schemas as T
from .. import utils
from .. import config

log = logging.getLogger(__name__)


class Task(ABC):
    """Abstract ingest task interface"""
    can_retry = False

    def __init__(self, db: DBClient, task: T.TaskOut, worker_config: config.WorkerConfig):
        self.db = db  # pylint: disable=C0103
        self.task = task
        self.worker_config = worker_config
        ingest = self.db.ingest
        self.ingest_config = ingest.config
        self.strategy_config = ingest.strategy_config

    @abstractmethod
    def _run(self):
        """Task specific implementation."""

    def _initialize(self):
        """Initialize the task before execution."""

    def _on_success(self):
        """Called when the task completed successfully"""

    def _on_error(self):
        """Called when the task ultimately failed"""

    def run(self):
        """Execute the task."""
        try:
            self._initialize()
            self._run()
            self.db.update_task(self.task.id, status=T.TaskStatus.completed)
            self._on_success()
        except Exception as exc:  # pylint: disable=broad-except
            if self.can_retry and self.task.retries < self.ingest_config.max_retries:
                self.db.update_task(
                    self.task.id,
                    status=T.TaskStatus.pending,
                    retries=self.task.retries + 1
                )
                exc_type = exc.__class__.__name__
                log.warning(f"Task failed with {exc_type}, retrying later ({self.task.retries + 1})")
            else:
                log.exception("Task failed")
                self.db.update_task(self.task.id, status=T.TaskStatus.failed, error=str(exc))
                self._on_error()

    @property
    def fw(self):
        """Get flywheel SDK client"""
        return utils.get_sdk_client(self.db.api_key)
