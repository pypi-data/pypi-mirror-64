from miio import Vacuum
from miio.vacuumcontainers import CleaningSummary, CleaningDetails, VacuumStatus
from unittest.mock import Mock, create_autospec, patch, PropertyMock
from pytest import fixture
from datetime import timedelta, datetime
EMPTY_CLEANING_SUMMARY = CleaningSummary([0, 0, 0, []])

@fixture()
def dev():
    return Vacuum("123.123.123.123")

def test_vacuum_state_v4():
    data = {'state': 8, 'dnd_enabled': 1, 'clean_time': 0,
            'msg_ver': 4, 'map_present': 1, 'error_code': 0, 'in_cleaning': 0,
            'clean_area': 0, 'battery': 100, 'fan_power': 20, 'msg_seq': 320}

    x = VacuumStatus(data)

    assert x.state == "Charging"
    assert x.state_code == 8

    assert not x.got_error
    assert x.error_code == 0
    assert x.error == "No error"

    assert x.fanspeed == 20
    assert x.clean_area == 0
    assert x.clean_time == timedelta(0)

    with patch.object(x, 'state_code', new_callable=PropertyMock) as invalid:
        invalid.return_value = -1
        assert x.state == "Charging"


def test_cleaning_summary():
    x = CleaningSummary([1, 57260000, 2, [1548855493, 1543350408]])
    assert x.count == 2
    assert len(x.ids) == 2
    assert x.total_duration == timedelta(seconds=1)
    assert x.total_area == 57.26


def test_clean_details(dev: Vacuum):
    start = datetime(year=2000, day=1, month=1, hour=1)
    end = datetime(year=2000, day=1, month=1, hour=2)
    duration = timedelta(hours=1)
    details = CleaningDetails([ start.timestamp(), end.timestamp(), duration.total_seconds(), 57260000, 0, 0 ])

    assert details.start == start
    assert details.end == end
    assert details.duration == duration
    assert details.area == 57.26
    assert details.error_code == 0
    assert details.error == "No error"

def test_empty_last_clean_details(dev: Vacuum):
    with patch.object(dev, 'clean_history') as mock_clean:
        mock_clean.return_value = EMPTY_CLEANING_SUMMARY
        history = dev.clean_history()
        assert history.count == 0
        assert history.total_area == 0
        assert history.total_duration == timedelta(0)
        assert not history.ids

        assert not dev.last_clean_details()



