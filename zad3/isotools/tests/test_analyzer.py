import pytest
from isotools.analyzer import analyze_media, find_pattern, find_all_patterns, needs_overburn
from isotools.formats import MEDIA_CAPACITY, SECTOR_SIZE

def test_analyze_media(tmp_path):
    test_file = tmp_path / "test.iso"
    with open(test_file, 'wb') as f:
        f.write(b'0' * 2048 * 2)
    
    result = analyze_media(str(test_file))
    assert result['size'] == 4096
    assert result['sectors'] == 2
    assert result['capacity'] == 737280000

def test_find_pattern(tmp_path):
    test_file = tmp_path / "test.bin"
    with open(test_file, 'wb') as f:
        f.write(b'0' * 2048 + b'1' * 2048)
    
    assert find_pattern(str(test_file), b'1') == 1
    assert find_pattern(str(test_file), b'2') is None

def test_find_all_patterns(tmp_path):
    test_file = tmp_path / "test.bin"
    with open(test_file, 'wb') as f:
        f.write(b'0' * 2048 + b'1' * 2048 + b'0' * 2048 + b'1' * 2048)
    
    assert find_all_patterns(str(test_file), b'1') == [1, 3]
    assert find_all_patterns(str(test_file), b'2') == []

def test_needs_overburn(tmp_path):
    path = tmp_path / "big.iso"
    path.write_bytes(b"0" * (MEDIA_CAPACITY['iso'] + 1))
    assert needs_overburn(str(path)) 