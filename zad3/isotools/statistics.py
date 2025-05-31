from typing import Dict, List

from isotools.analyzer import analyze_media, find_all_patterns

def get_media_stats(path: str) -> Dict[str, int]:
    return analyze_media(path)

def get_pattern_stats(path: str, pattern: bytes) -> Dict[str, int]:
    sectors = find_all_patterns(path, pattern)
    return {
        'count': len(sectors),
        'first_sector': sectors[0] if sectors else -1,
        'last_sector': sectors[-1] if sectors else -1
    }

def get_media_usage(path: str) -> Dict[str, float]:
    stats = analyze_media(path)
    if stats['capacity'] == 0:
        return {'usage': 0.0}
    return {
        'usage': (stats['size'] / stats['capacity']) * 100
    } 