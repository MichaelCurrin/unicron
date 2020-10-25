"""
History module tests.
"""
# pylint: disable=missing-function-docstring
import datetime

from unicron import history


def test_get_last_run_date():
    assert history.get_last_run_date("never_run_before.sh") is None
    assert history.get_last_run_date("fail.sh") is None

    assert history.get_last_run_date("old.sh") == datetime.date(
        year=2020, month=1, day=1
    )
    assert history.get_last_run_date("today.sh") == datetime.date.today()


def test_check_need_to_run():
    # Expect to run.
    assert history.check_need_to_run("never_run_before.sh") is True
    assert history.check_need_to_run("fail.sh") is True
    assert history.check_need_to_run("old.sh") is True

    # Expect not to run.
    assert history.check_need_to_run("today.sh") is False
