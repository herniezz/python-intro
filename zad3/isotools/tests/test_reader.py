import os
import pytest

from isotools.reader import get_file_size, read_sector

def test_get_file_size(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("test content")
    assert get_file_size(str(test_file)) == len("test content")

def test_read_sector(tmp_path):
    test_file = tmp_path / "test.bin"
    with open(test_file, 'wb') as f:
        f.write(b'0' * 2048 + b'1' * 2048)
    
    assert len(read_sector(str(test_file), 0)) == 2048
    assert read_sector(str(test_file), 0) == b'0' * 2048
    assert read_sector(str(test_file), 1) == b'1' * 2048

def test_read_sector_invalid():
    with pytest.raises(ValueError):
        read_sector("test.bin", -1)
    
    with pytest.raises(ValueError):
        read_sector("test.bin", 0, 0) 