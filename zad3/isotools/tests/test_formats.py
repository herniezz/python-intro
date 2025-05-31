import pytest

from isotools.formats import SECTOR_SIZE, MEDIA_CAPACITY

def test_sector_size():
    assert SECTOR_SIZE == 2048

def test_media_capacity():
    expected = {
        'iso': 737280000,
        'img': 737280000,
        'bin': 737280000,
        'dvd': 4700000000,
        'dvd_dl': 8500000000,
        'bd': 25000000000,
        'bd_dl': 50000000000,
        'usb_1gb': 1000000000,
        'usb_4gb': 4000000000,
        'usb_8gb': 8000000000,
        'usb_16gb': 16000000000,
        'usb_32gb': 32000000000,
        'hdd_500gb': 500000000000,
        'hdd_1tb': 1000000000000,
    }
    for key, value in expected.items():
        assert key in MEDIA_CAPACITY
        assert MEDIA_CAPACITY[key] == value

def test_media_capacity_keys():
    expected_keys = {
        'iso', 'img', 'bin', 'dvd', 'dvd_dl', 'bd', 'bd_dl',
        'usb_1gb', 'usb_4gb', 'usb_8gb', 'usb_16gb', 'usb_32gb',
        'hdd_500gb', 'hdd_1tb'
    }
    assert set(MEDIA_CAPACITY.keys()) == expected_keys 