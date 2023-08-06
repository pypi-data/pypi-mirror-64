"""Provides the DicomImporter class."""
# pylint: disable=R0903
from typing import Optional

from pydantic import validator

from ... import util
from ..template import create_scanner_node
from .abstract import Strategy, Config


class DicomStrategy(Strategy):
    """Strategy to ingest dicom files"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.config.subject:
            util.set_nested_attr(self.context, "subject.label", self.config.subject)
        if self.config.session:
            util.set_nested_attr(self.context, "session.label", self.config.session)

    def initialize(self):
        """Initialize the importer."""
        self.add_template_node(create_scanner_node("dicom"))


class DicomConfig(Config):
    """Config class for dicom ingest strategy"""
    group: str
    project: str
    subject: Optional[str]
    session: Optional[str]

    @validator("group")
    def validate_group_id(cls, val):  # pylint: disable=no-self-argument, no-self-use
        """Validate group id"""
        return util.group_id(val)

    class ArgparserConfig:
        """Argparser config"""
        group = {
            "positional": True,
            "nargs": "?",
            "metavar": "GROUP_ID",
            "help": "The id of the group",
        }
        project = {
            "positional": True,
            "nargs": "?",
            "metavar": "PROJECT_LABEL",
            "help": "The label of the project",
        }
        subject = {
            "metavar": "LABEL",
            "help": "Override value for the subject label",
        }
        session = {
            "metavar": "LABEL",
            "help": "Override value for the session label",
        }

    def create_strategy(self):
        return DicomStrategy(self)
