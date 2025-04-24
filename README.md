### 1. `enumerate()`

`enumerate()` przyjmuje obiekt iterowalny (np. listę, krotkę, string) i zwraca iterator. Ten iterator generuje krotki składające się z licznika (indeksu) i wartości pobranej z iterowalnego obiektu. Domyślnie indeksowanie zaczyna się od `0`, ale można to zmienić podając opcjonalny argument `start`. Jest to szczególnie użyteczne w pętlach `for`, gdy potrzebujemy jednocześnie dostępu do elementu i jego pozycji.
* **Przykład:**
    ```python
    owoc = ['jabłko', 'banan', 'czereśnia']
    for indeks, nazwa in enumerate(owoc, start=1):
        print(f"{indeks}. {nazwa}")
    # Wynik:
    # 1. jabłko
    # 2. banan
    # 3. czereśnia
    ```
[Dokumentacja dostępna tutaj.](https://docs.python.org/3/library/functions.html#enumerate)

### 2. `sorted()`

Wbudowana funkcja `sorted()` tworzy **nową**, posortowaną listę z elementów dowolnego obiektu iterowalnego (np. listy, krotki, zbioru, słownika - sortuje klucze). Oryginalny obiekt pozostaje **niezmieniony**. Funkcja akceptuje dwa opcjonalne argumenty nazwane: `key`, który przyjmuje funkcję używaną do wygenerowania klucza sortowania dla każdego elementu, oraz `reverse`, który jeśli ustawiony na `True`, sortuje elementy w porządku malejącym.

* **Przykład:**
    ```python
    liczby = [3, 1, 4, 1, 5, 9]
    posortowane_liczby = sorted(liczby) # -> [1, 1, 3, 4, 5, 9]
    posortowane_malejaco = sorted(liczby, reverse=True) # -> [9, 5, 4, 3, 1, 1]
    print(liczby) # -> [3, 1, 4, 1, 5, 9] (oryginał niezmieniony)
    ```
* [Dokumentacja dostępna tutaj.](https://docs.python.org/3/howto/sorting.html#sortinghowto)

### 3.`random`

`random` dostarcza funkcji do generowania liczb pseudolosowych oraz wykonywania losowych wyborów. Do najpopularniejszych funkcji należą: `random()` (zwraca losową liczbę zmiennoprzecinkową z przedziału `[0.0, 1.0)`), `randint(a, b)` (zwraca losową liczbę całkowitą z przedziału `[a, b]`, włącznie z `a` i `b`), `choice(seq)` (zwraca losowy element z niepustej sekwencji), `shuffle(x)` (miesza losowo elementy sekwencji `x` *w miejscu*). Domyślnie wykorzystuje generator liczb pseudolosowych Mersenne Twister.
* **UWAGA!** Ten moduł **nie jest przeznaczony do zastosowań kryptograficznych** (np. generowania haseł, tokenów bezpieczeństwa). Do takich celów można użyć modułu `secrets`.
* [Dokumentacja dostępna tutaj.](https://docs.python.org/3/library/random.html)

### 4.`datetime`

`datetime` udostępnia klasy do pracy z datami i czasem. Główne klasy to: `date` (reprezentuje datę: rok, miesiąc, dzień), `time` (reprezentuje czas: godzina, minuta, sekunda, mikrosekunda, informacja o strefie czasowej), `datetime` (połączenie daty i czasu), `timedelta` (reprezentuje różnicę między dwoma obiektami `date`, `time` lub `datetime`, używana do arytmetyki na datach/czasie), oraz `timezone` (abstrakcyjna klasa bazowa dla informacji o strefach czasowych). Moduł pozwala na pobieranie aktualnej daty i czasu (np. `datetime.now()`), wykonywanie obliczeń (np. dodawanie `timedelta` do `datetime`), formatowanie dat/czasu do stringów (`strftime`) oraz parsowanie stringów do obiektów daty/czasu (`strptime`).
* [Dokumentacja dostępna tutaj.](https://docs.python.org/3/library/datetime.html)

### 5.`ZeroDivisionError`

 Wyjątek `ZeroDivisionError` jest zgłaszany, gdy drugi argument operacji dzielenia lub operacji modulo wynosi zero. Dotyczy to operatorów dzielenia zmiennoprzecinkowego (`/`), dzielenia całkowitego (`//`) oraz reszty z dzielenia (`%`). Jest to podklasa `ArithmeticError`. Wystąpienie tego błędu zazwyczaj prowadzi do zatrzymania programu, chyba że zostanie on przechwycony i obsłużony za pomocą bloku `try...except`.
* **działanie**
    ```python
    dzielna = 10
    dzielnik = 0
    try:
        wynik = dzielna / dzielnik
        print(f"Wynik: {wynik}")
    except ZeroDivisionError:
        print("Błąd: Próba dzielenia przez zero!")
    # Wynik:
    # Błąd: Próba dzielenia przez zero!
    ```
* [Dokumentacja dostępna tutaj.](https://docs.python.org/3/library/exceptions.html#ZeroDivisionError)

---