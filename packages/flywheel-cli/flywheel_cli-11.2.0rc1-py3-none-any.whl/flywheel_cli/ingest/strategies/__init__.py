"""Provides various ingest strategies to import different type of files."""
import typing

from .dicom import DicomConfig
from .folder import FolderConfig
from .template import TemplateConfig

StrategyConfig = typing.Union[DicomConfig, FolderConfig, TemplateConfig]
