**IsoTools** to biblioteka Pythona do analizy obrazów dyskowych i optycznych. Umożliwia odczyt metadanych, wyszukiwanie wzorców bajtowych, wykrywanie mozliwosci overburningu i generowanie statystyk.


### Instalacja ręczna
```bash
git clone https://github.com/herniezz/isotools.git
cd isotools
python setup.py install
```

## Przykłady użycia

### Analiza obrazu dysku
```python
from isotools import analyze_media, get_media_usage

# Sprawdź rozmiar i pojemność obrazu
info = analyze_media("my_disk.iso")
print(f"Rozmiar: {info['size']} bajtów")
print(f"Liczba sektorów: {info['sectors']}")
print(f"Pojemność nośnika: {info['capacity']} bajtów")

# Sprawdź wykorzystanie nośnika
usage = get_media_usage("my_disk.iso")
print(f"Wykorzystanie: {usage['usage']:.2f}%")
```

### Wyszukiwanie wzorców
```python
from isotools import find_pattern, find_all_patterns

# Znajdź pierwsze wystąpienie wzorca
sector = find_pattern("my_disk.iso", b"PATTERN")
if sector is not None:
    print(f"Znaleziono wzorzec w sektorze {sector}")

# Znajdź wszystkie wystąpienia
sectors = find_all_patterns("my_disk.iso", b"PATTERN")
print(f"Znaleziono {len(sectors)} wystąpień wzorca")
```

### Sprawdzanie overburningu
```python
from isotools import needs_overburn

if needs_overburn("my_disk.iso"):
    print("Ostrzeżenie: Obraz przekracza standardową pojemność CD!")
```

## Informacje o projekcie

- **Autor:** herniezz
- **Wersja:** 0.1.0
- **Licencja:** MIT

## Struktura projektu

```
isotools/
  formats.py
  reader.py
  analyzer.py
  statistics.py
tests/
  test_formats.py
  test_reader.py
  test_analyzer.py
  test_statistics.py
README.md
setup.py
__init__.py
```

### Implementacja modułów

### **`formats.py`**

```python
SECTOR_SIZE = 2048

MEDIA_CAPACITY = {
    'iso': 737280000,      # 700 MB CD
    'img': 737280000,      # 700 MB CD
    'bin': 737280000,      # 700 MB CD
    'dvd': 4700000000,     # 4.7 GB single-layer dvd
    'dvd_dl': 8500000000,  # 8.5 GB dual-layer dvd
    'bd': 25000000000,     # 25 GB single-layer blu-ray
    'bd_dl': 50000000000,  # 50 GB dual-layer blu-ray
    'usb_1gb': 1000000000, # 1 GB USB stick
    'usb_4gb': 4000000000, # 4 GB USB stick
    'usb_8gb': 8000000000, # 8 GB USB stick
    'usb_16gb': 16000000000, # 16 GB USB stick
    'usb_32gb': 32000000000, # 32 GB USB stick
    'hdd_500gb': 500000000000, # 500 GB HDD
    'hdd_1tb': 1000000000000,  # 1 TB HDD
} 
```

Moduł definiuje stałe używane w całej bibliotece. `SECTOR_SIZE` określa rozmiar sektora (2048 B), kluczowy przy obliczeniach przesunięć w plikach obrazów optycznych. `MEDIA_CAPACITY` mapuje formaty plików na ich standardowe pojemności w bajtach (np. CD 700 MB, DVD 4.7 GB). 

> uwzględniono tu zarówno obrazy optyczne (ISO/CUE-BIN, DVD, Blu-ray), jak i masowe (IMG/DD z USB/HDD/SSD), ponieważ różne nośniki mają odmienną strukturę i rozmiar sektorów – w optyce standardem jest 2048 B, a w dyskach twardych i pamięciach flash 512 B lub 4096 B – co bez wyraźnego rozgraniczenia prowadziłoby do błędnych obliczeń przesunięć i wyszukiwania wzorców. Taki podział ułatwia również przyszłą rozbudowę - w istocie, moznaby wystarczy dodać nowe stałe w `formats.py` , by automatycznie dostosować analizę do niestandardowych formatów bez modyfikowania całej logiki narzędzi.
> 

### **`reader.py`**

```python
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
```

Moduł `reader.py` jest odpowiedzialny za bezpośrednią interakcję z plikiem obrazu na poziomie binarnym. Funkcja `get_file_size` bierze ścieżkę do pliku z obrazem i zwraca jego rozmiar w bajtach. Jeśli nie ma dostępu, przerywa działanie. `read_sector` pozwala wyciągnąć fragment danych: najpierw sprawdzanie, czy numer sektora jest nieujemny, a jeśli `size` nie jest podany, odczytuje dokładnie 2048 bajtów (rozmiar sektora). W przeciwnym razie używa wskazanej liczby bajtów – ale tylko wtedy, gdy jest dodatnia. Dane odczytywane są bezpośrednio w formie binarnej. Jeśli odczyta poza końcem pliku, funkcja zwróci mniej bajtów niż poproszono, zamiast zgłaszać błąd.

### **`analyzer.py`**

```python
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
```

Moduł `analyzer.py` to najwazniejsza część biblioteki. `analyze_media` podaje ile bajtów ma plik, ile pełnych sektorów (dzieląc przez 2048 B) i jaka jest nominalna pojemność nośnika na podstawie rozszerzenia (np. .iso to 700 MB). Dzięki temu wiadomo, czy obraz zmieści się na standardowych nośnikach.`find_pattern` skanuje obraz sektor po sektorze od podanego miejsca, szukając sekwencji bajtów `pattern`. Jeśli wzorzec się nie pojawi lub plik się skończy, funkcja zwraca `None`; w przeciwnym razie numer pierwszego pasującego sektora. `find_all_patterns` robi to samo, ale zbiera wszystkie sektory zawierające wzorzec i zwraca ich listę. `needs_overburn` sprawdza, czy plik jest większy niż 700 MB. Zwraca `True`, gdy obraz przekracza pojemność standardowej płyty CD, co może wymagać overburningu lub nośnika o większej pojemności.

### **`statistics.py`**

```python
from typing import Dict
from .analyzer import analyze_media, find_all_patterns

def get_media_stats(path: str) -> Dict[str, int]:
    return analyze_media(path)

def get_pattern_stats(path: str, pattern: bytes) -> Dict[str, int]:
    sectors = find_all_patterns(path, pattern)
    count = len(sectors)
    return {'count': count, 'first_sector': sectors[0] if count else -1, 'last_sector': sectors[-1] if count else -1}

def get_media_usage(path: str) -> Dict[str, float]:
    info = analyze_media(path)
    cap = info['capacity']
    return {'usage': (info['size'] / cap * 100) if cap else 0.0}
```

- `get_media_stats` to przekazanie wyników z `analyze_media` dalej.
- `get_pattern_stats` zlicza, ile razy i gdzie wewnątrz obrazu występuje podany wzorzec bajtowy (pierwszy i ostatni sektor, liczba wystąpień).
- `get_media_usage` oblicza, jaki procent pojemności nośnika zajmuje obraz; gdy pojemność jest nieznana (0), zwraca 0.0.

### Testy jednostkowe i walidacja

W projekcie zastosowano **pytest** do weryfikacji poprawności działania funkcji w czterech modułach.

### **`test_formats.py`**

```python
from isotools.formats import SECTOR_SIZE, MEDIA_CAPACITY

def test_sector_size():
    assert isinstance(SECTOR_SIZE, int)
    assert SECTOR_SIZE > 0

def test_media_capacity_keys():
    # Sprawdź, czy klucze dla nośników optycznych istnieją
    for key in ['iso', 'bin', 'img', 'dvd', 'bd_dl']:
        assert key in MEDIA_CAPACITY
```

- Weryfikacja, że `SECTOR_SIZE` jest poprawnym dodatnim integerem.
- Sprawdzenie obecności kluczy odpowiadających formatom optycznym i masowym.

### **`test_reader.py`**

```python
import pytest
from isotools.reader import get_file_size, read_sector

def test_get_file_size(tmp_path):
    p = tmp_path / "file"
    p.write_bytes(b"1234")
    assert get_file_size(str(p)) == 4

def test_read_sector_negative():
    with pytest.raises(ValueError):
        read_sector("dummy", sector=-1)

def test_read_sector_eof(tmp_path):
    p = tmp_path / "file"
    p.write_bytes(b"AB")
    data = read_sector(str(p), sector=0, size=10)
    assert data == b"AB"
```

- `test_get_file_size` weryfikuje poprawność odczytu rozmiaru pliku.
- `test_read_sector_negative` sprawdza, czy podsunięcie negatywnego sektora zgłasza `ValueError`.
- `test_read_sector_eof` symuluje odczyt poza końcem pliku i oczekuje, że zwrócone zostaną tylko dostępne bajty.

### **`test_analyzer.py`**

```python
import pytest
from isotools.analyzer import analyze_media, can_overburn, find_pattern, find_all_patterns
from isotools.formats import MEDIA_CAPACITY, SECTOR_SIZE

def test_analyze_media(tmp_path):
    path = tmp_path / "test.iso"
    data = b"X" * (SECTOR_SIZE * 5)
    path.write_bytes(data)
    stats = analyze_media(str(path))
    assert stats['sectors'] == 5
    assert stats['capacity'] == MEDIA_CAPACITY['iso']

def test_can_overburn(tmp_path):
    path = tmp_path / "big.iso"
    path.write_bytes(b"0" * (MEDIA_CAPACITY['iso'] + 1))
    assert can_overburn(str(path))

def test_find_pattern_and_all(tmp_path):
    path = tmp_path / "pattern.bin"
    content = b"A"*(SECTOR_SIZE*2) + b"PATTERN" + b"A"*(SECTOR_SIZE-7)
    path.write_bytes(content)
    assert find_pattern(str(path), b"PATTERN") == 2
    assert find_all_patterns(str(path), b"PATTERN") == [2]
```

- Weryfikacja poprawności `analyze_media` (sektory, pojemność).
- Testy funkcji `can_overburn` na obrazie poniżej pojemności i przekraczającym pojemność.
- Sprawdzenie pojedynczego i zbiorczego wyszukiwania wzorca.

### **`test_statistics.py`**

```python
from isotools.statistics import get_media_stats, get_pattern_stats, get_media_usage
from isotools.formats import MEDIA_CAPACITY, SECTOR_SIZE

def test_get_media_stats(tmp_path):
    file = tmp_path / "s.iso"
    file.write_bytes(b"Z" * SECTOR_SIZE)
    stats = get_media_stats(str(file))
    assert stats['sectors'] == 1

def test_get_pattern_stats(tmp_path):
    file = tmp_path / "p.bin"
    file.write_bytes(b"B"*SECTOR_SIZE + b"XY" + b"B"*(SECTOR_SIZE-2))
    ps = get_pattern_stats(str(file), b"XY")
    assert ps['count'] == 1
    assert ps['first_sector'] == 1

def test_get_media_usage(tmp_path):
    file = tmp_path / "u.iso"
    file.write_bytes(b"C" * (MEDIA_CAPACITY['iso']//2))
    usage = get_media_usage(str(file))
    assert pytest.approx(usage['usage'], rel=1e-3) == 50.0
```

- Sprawdzenie aliasu `get_media_stats`, poprawności statystyk wzorców oraz prawidłowego obliczania procentowego wykorzystania. 