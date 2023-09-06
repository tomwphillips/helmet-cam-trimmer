from trim import get_trim_timestamps, seconds_to_timestamp, timestamp_to_seconds


def test_hms_timestamp_to_seconds():
    assert timestamp_to_seconds("00:00:00") == 0
    assert timestamp_to_seconds("01:01:01") == 60 * 60 + 60 + 1
    assert timestamp_to_seconds("-01:01:01") == -1 * (60 * 60 + 60 + 1)


def test_ms_timestamp_to_seconds():
    assert timestamp_to_seconds("00:00") == 0
    assert timestamp_to_seconds("01:01") == 60 + 1
    assert timestamp_to_seconds("-01:01") == -1 * (60 + 1)


def test_seconds_to_timestamp():
    assert seconds_to_timestamp(60 * 60 + 60 + 1) == "01:01:01"
    assert seconds_to_timestamp(-1 * (60 * 60 + 60 + 1)) == "-01:01:01"


def test_get_trim_timestamps():
    assert get_trim_timestamps(180) == (120, 240)
    assert get_trim_timestamps(30) == (0, 90)
    assert get_trim_timestamps(180, padding_after=30) == (120, 210)
    assert get_trim_timestamps(180, padding_before=30) == (150, 240)
