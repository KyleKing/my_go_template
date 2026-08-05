"""Python bindings for the test-template Go library."""

from ._core import TestTemplateError, __version__, go_version, run

__all__ = ['TestTemplateError', '__version__', 'go_version', 'run']
