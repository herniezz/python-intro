import pytest

from isotools.statistics import get_media_stats, get_pattern_stats, get_media_usage

def test_get_media_stats(tmp_path):
    test_file = tmp_path / "test.iso"
    with open(test_file, 'wb') as f:
        f.write(b'0' * 2048 * 2)
    
    result = get_media_stats(str(test_file))
    assert result['size'] == 4096
    assert result['sectors'] == 2
    assert result['capacity'] == 737280000

def test_get_pattern_stats(tmp_path):
    test_file = tmp_path / "test.bin"
    with open(test_file, 'wb') as f:
        f.write(b'0' * 2048 + b'1' * 2048 + b'0' * 2048 + b'1' * 2048)
    
    result = get_pattern_stats(str(test_file), b'1')
    assert result['count'] == 2
    assert result['first_sector'] == 1
    assert result['last_sector'] == 3

def test_get_media_usage(tmp_path):
    test_file = tmp_path / "test.iso"
    with open(test_file, 'wb') as f:
        f.write(b'0' * 2048 * 2)
    
    result = get_media_usage(str(test_file))
    assert result['usage'] == pytest.approx(0.0005555555555555556, rel=1e-10) 