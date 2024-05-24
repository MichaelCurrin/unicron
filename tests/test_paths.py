"""
Paths module tests.
"""

# pylint: disable=missing-function-docstring
from unicron import paths


def test_mk_last_run_path():
    path = paths.mk_last_run_path("foo")

    assert str(path).endswith("_test_var/last_run/foo.txt")


def test_mk_output_path():
    path = paths.mk_output_path("foo")

    assert str(path).endswith("_test_var/output/foo.log")
