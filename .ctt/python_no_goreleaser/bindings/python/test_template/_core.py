"""Python bindings for the test-template Go library."""

from __future__ import annotations

import ctypes
import sys
from pathlib import Path
from threading import Lock

__version__ = '0.0.0'

_LIB_STEM = '_libtesttemplate'
_LIB_SUFFIXES = {'darwin': '.dylib', 'win32': '.dll'}

_lib: ctypes.CDLL | None = None
_lib_lock = Lock()


class TestTemplateError(Exception):
    """Raised when the Go library rejects its input."""


def _library_path() -> Path:
    suffix = _LIB_SUFFIXES.get(sys.platform, '.so')
    return Path(__file__).parent / f'{_LIB_STEM}{suffix}'


def _load() -> ctypes.CDLL:
    """Open the shared library, binding argument and return types once.

    Loading is deferred to the first call because the Go runtime does not survive
    fork() without exec(). Importing this module stays safe for a process that
    forks; calling into it before forking is not.
    """
    global _lib  # ruff: ignore[global-statement]
    with _lib_lock:
        if _lib is not None:
            return _lib

        lib = ctypes.CDLL(str(_library_path()))
        lib.TestTemplateRun.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p)]
        lib.TestTemplateRun.restype = ctypes.c_void_p
        lib.TestTemplateVersion.argtypes = []
        lib.TestTemplateVersion.restype = ctypes.c_void_p
        lib.TestTemplateFree.argtypes = [ctypes.c_void_p]
        lib.TestTemplateFree.restype = None
        _lib = lib
        return lib


def _take(lib: ctypes.CDLL, pointer: int | None) -> str | None:
    """Copy a Go-allocated C string into Python and free the original."""
    if not pointer:
        return None
    try:
        raw = ctypes.cast(pointer, ctypes.c_char_p).value
        return raw.decode() if raw is not None else None
    finally:
        lib.TestTemplateFree(pointer)


def run(text: str) -> str:
    """Pass text through the Go library and return its output."""
    lib = _load()
    error = ctypes.c_char_p()
    pointer = lib.TestTemplateRun(text.encode(), ctypes.byref(error))
    message = _take(lib, ctypes.cast(error, ctypes.c_void_p).value)
    if message is not None:
        raise TestTemplateError(message)
    if pointer is None:
        raise TestTemplateError('test-template returned no output')
    return _take(lib, pointer) or ''


def go_version() -> str:
    """Return the version, commit, and build date stamped into the Go library."""
    lib = _load()
    return _take(lib, lib.TestTemplateVersion()) or ''
