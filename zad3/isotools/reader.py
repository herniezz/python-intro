import os
from typing import Optional

from isotools.formats import SECTOR_SIZE

def get_file_size(path: str) -> int:
    return os.path.getsize(path)

def read_sector(path: str, sector: int = 0, size: Optional[int] = None) -> bytes:
    if sector < 0:
        raise ValueError("sector number must be non-negative")
    if size is None:
        size = SECTOR_SIZE
    elif size <= 0:
        raise ValueError("size must be positive")
    with open(path, 'rb') as f:
        f.seek(sector * SECTOR_SIZE)
        return f.read(size) 