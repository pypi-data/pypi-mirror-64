"""Provides FolderImporter class."""
# pylint: disable=R0903
import re
from typing import Optional

from ..template import StringMatchNode
from .abstract import Strategy, Config


class FolderStrategy(Strategy):
    """Strategy to ingest a folder"""

    def initialize(self):
        """Initialize the strategy."""
        for _ in range(self.config.root_dirs):
            self.add_template_node(StringMatchNode(re.compile(".*")))

        if not self.config.group:
            self.add_template_node(StringMatchNode("group"))

        if not self.config.project:
            self.add_template_node(StringMatchNode("project"))

        if not self.config.no_subjects:
            self.add_template_node(StringMatchNode("subject"))

        if not self.config.no_sessions:
            self.add_template_node(StringMatchNode("session"))

        if self.config.pack_acquisitions:
            self.add_template_node(StringMatchNode('acquisition', packfile_type=self.config.pack_acquisitions))
        else:
            self.add_template_node(StringMatchNode('acquisition'))
            self.add_template_node(StringMatchNode(re.compile(self.config.dicom), packfile_type='dicom'))


class FolderConfig(Config):
    """Config class for folder import strategy"""
    strategy_name = "folder"
    group: Optional[str]
    project: Optional[str]
    dicom: str = "dicom"
    pack_acquisitions: Optional[str]
    root_dirs: int = 0
    no_subjects: bool = False
    no_sessions: bool = False

    class ArgparserConfig:
        """Argparser config"""
        _groups = {
            "acq": {"type": "mutually_exclusive"},
            "no_level": {"type": "mutually_exclusive"},
        }
        group = {
            "flags": ["-g", "--group"],
            "metavar": "ID",
            "help": "The id of the group, if not in folder structure",
        }
        project = {
            "flags": ["-p", "--project"],
            "metavar": "LABEL",
            "help": "The label of the project, if not in folder structure",
        }
        dicom = {
            "group": "acq",
            "metavar": "NAME",
            "help": "The name of dicom subfolders to be zipped prior to upload",
        }
        pack_acquisitions = {
            "group": "acq",
            "metavar": "TYPE",
            "help": "Acquisition folders only contain acquisitions of TYPE and are zipped prior to upload",
        }
        root_dirs = {"help": "The number of directories to discard before matching"}
        no_subjects = {
            "group": "no_level",
            "help": "no subject level (create a subject for every session)",
        }
        no_sessions = {
            "group": "no_level",
            "help": "no session level (create a session for every subject)",
        }

    def create_strategy(self):
        return FolderStrategy(self)
