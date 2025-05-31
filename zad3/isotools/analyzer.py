from typing import Dict, List, Optional

from isotools.formats import MEDIA_CAPACITY, SECTOR_SIZE
from isotools.reader import get_file_size, read_sector

def analyze_media(path: str) -> Dict[str, int]:
    size = get_file_size(path)
    return {
        'size': size,
        'sectors': size // SECTOR_SIZE,
        'capacity': MEDIA_CAPACITY.get(path.split('.')[-1].lower(), 0)
    }

def find_pattern(path: str, pattern: bytes, start_sector: int = 0) -> Optional[int]:
    if start_sector < 0:
        raise ValueError("start_sector must be non-negative")
    if not pattern:
        raise ValueError("pattern cannot be empty")
    
    sector = start_sector
    while True:
        data = read_sector(path, sector)
        if not data:
            break
        if pattern in data:
            return sector
        sector += 1
    return None

def find_all_patterns(path: str, pattern: bytes) -> List[int]:
    if not pattern:
        raise ValueError("pattern cannot be empty")
    
    sectors = []
    sector = 0
    while True:
        data = read_sector(path, sector)
        if not data:
            break
        if pattern in data:
            sectors.append(sector)
        sector += 1
    return sectors

def needs_overburn(path: str) -> bool:
    size = get_file_size(path)
    return size > 737280000 