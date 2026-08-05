from __future__ import annotations

import subprocess
import sys

import test_template


def test_run_trims_surrounding_whitespace() -> None:
    assert test_template.run('  hello  ') == 'hello'


def test_run_is_idempotent() -> None:
    once = test_template.run('hello world\n')
    assert test_template.run(once) == once


def test_run_accepts_empty_input() -> None:
    assert not test_template.run('')


def test_run_round_trips_unicode() -> None:
    assert test_template.run('héllo wörld') == 'héllo wörld'


def test_go_version_is_stamped() -> None:
    assert len(test_template.go_version().split()) == 3


def test_cli_reads_stdin() -> None:
    result = subprocess.run(
        [sys.executable, '-m', 'test_template._cli'],
        input='  hello  ',
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout == 'hello'
