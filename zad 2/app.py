import random
import time
import sys
from colorama import Fore, Back, Style, init

init(autoreset=True)

mapowane_kolorki = {
    "czerwony": Fore.RED,
    "niebieski": Fore.BLUE,
    "zielony": Fore.GREEN,
    "żółty": Fore.YELLOW,
    "fioletowy": Fore.MAGENTA,
    "pomarańczowy": Fore.LIGHTRED_EX
}

NAZWY_KOLOROW = list(mapowane_kolorki.keys())

# Przykładowe wyświetlenie kolorów
print(Fore.RED + 'Ten tekst jest czerwony')
print(Fore.GREEN + Back.YELLOW + 'Ten tekst jest zielony na żółtym tle')
print(Fore.BLUE + Style.BRIGHT + 'Ten tekst jest jasno niebieski i pogrubiony')
print('Ten tekst jest już w domyślnym kolorze.')  # autoreset=True

class Proba:
    """
    Reprezentuje pojedynczą próbę w teście Stroopa.
    """
    def __init__(self, slowo, kolor_druku, zgodny):
        if slowo not in mapowane_kolorki or kolor_druku not in mapowane_kolorki:
            raise ValueError("Użyto nieznanego koloru.")
        self.slowo = slowo
        self.kolor_druku = kolor_druku
        self.zgodny = zgodny
        self.czas_reakcji = None
        self.odpowiedz_uzytkownika = None
        self.poprawna = None

    def __str__(self):
        typ = "Zgodny" if self.zgodny else "Niezgodny"
        return f"Proba ({typ}): Słowo='{self.slowo}', KolorDruku='{self.kolor_druku}'"

    def zapisz_wynik(self, odpowiedz, czas):
        self.odpowiedz_uzytkownika = odpowiedz.lower().strip()
        self.czas_reakcji = czas
        self.poprawna = (self.odpowiedz_uzytkownika == self.kolor_druku)

class TestStroopa:
    """
    Zarządza przebiegiem testu Stroopa.
    """
    def __init__(self, liczba_prob_na_warunek=10):
        if liczba_prob_na_warunek <= 0:
            raise ValueError("Liczba prób musi być dodatnia.")
        self.liczba_prob_na_warunek = liczba_prob_na_warunek
        self.proby = []
        self.wyniki = {
            "zgodne_poprawne_czasy": [],
            "niezgodne_poprawne_czasy": [],
            "liczba_zgodnych_bledow": 0,
            "liczba_niezgodnych_bledow": 0
        }

    def _generuj_proby(self):
        self.proby.clear()
        # prób zgodnych
        for _ in range(self.liczba_prob_na_warunek):
            kolor = random.choice(NAZWY_KOLOROW)
            self.proby.append(Proba(kolor, kolor, True))
        # prób niezgodnych
        for _ in range(self.liczba_prob_na_warunek):
            slowo = random.choice(NAZWY_KOLOROW)
            kolor_druku = random.choice(NAZWY_KOLOROW)
            while kolor_druku == slowo:
                kolor_druku = random.choice(NAZWY_KOLOROW)
            self.proby.append(Proba(slowo, kolor_druku, False))
        random.shuffle(self.proby)

    def _wyswietl_instrukcje(self):
        print("--- Test Stroopa ---")
        print("Instrukcja:")
        print("Nazwij kolor druku widocznych słów, ignorując ich znaczenie.")
        print(f"Dostępne kolory: {', '.join(NAZWY_KOLOROW)}")
        print(f"Test składa się z {len(self.proby)} prób.")
        input("Naciśnij Enter, aby rozpocząć...")
        print("-" * 40)

    def _przeprowadz_proba(self, proba: Proba):
        kod = mapowane_kolorki[proba.kolor_druku]
        print(kod + proba.slowo.upper() + Style.RESET_ALL)
        sys.stdout.write("Podaj kolor druku: ")
        sys.stdout.flush()

        start = time.time()
        odp = input()
        koniec = time.time()

        proba.zapisz_wynik(odp, koniec - start)
        if proba.poprawna:
            print(f"Dobrze! Czas: {proba.czas_reakcji:.3f} s")
        else:
            print(f"Błąd. Poprawna odpowiedź: {proba.kolor_druku}. Czas: {proba.czas_reakcji:.3f} s")
        time.sleep(0.5)

    def _zapisz_wynik_proby(self, proba: Proba):
        if proba.poprawna:
            lista = "zgodne_poprawne_czasy" if proba.zgodny else "niezgodne_poprawne_czasy"
            self.wyniki[lista].append(proba.czas_reakcji)
        else:
            key = "liczba_zgodnych_bledow" if proba.zgodny else "liczba_niezgodnych_bledow"
            self.wyniki[key] += 1

    def uruchom_test(self):
        self._generuj_proby()
        if not self.proby:
            print("Brak prób do przeprowadzenia.")
            return
        self._wyswietl_instrukcje()
        for idx, p in enumerate(self.proby, start=1):
            print(f"\n--- Próba {idx}/{len(self.proby)} ---")
            self._przeprowadz_proba(p)
            self._zapisz_wynik_proby(p)
        print("\n--- Koniec Testu ---")

    def oblicz_i_wyswietl_wyniki(self):
        print("\n--- Wyniki ---")
        zg = self.wyniki["zgodne_poprawne_czasy"]
        nz = self.wyniki["niezgodne_poprawne_czasy"]
        if zg:
            print(f"Średni czas (zgodne): {sum(zg)/len(zg):.3f} s")
        else:
            print("Brak poprawnych odpowiedzi w próbach zgodnych.")
        if nz:
            print(f"Średni czas (niezgodne): {sum(nz)/len(nz):.3f} s")
        else:
            print("Brak poprawnych odpowiedzi w próbach niezgodnych.")
        print(f"Poprawne (zgodne): {len(zg)}, Błędy (zgodne): {self.wyniki['liczba_zgodnych_bledow']}")
        print(f"Poprawne (niezgodne): {len(nz)}, Błędy (niezgodne): {self.wyniki['liczba_niezgodnych_bledow']}")
        if zg and nz:
            efekt = (sum(nz)/len(nz)) - (sum(zg)/len(zg))
            print(f"Efekt Stroopa: {efekt:.3f} s")
            if efekt > 0:
                print("(reakcje w próbach niezgodnych wolniejsze)")
            else:
                print("(brak typowego efektu Stroopa)")

if __name__ == "__main__":
    try:
        test = TestStroopa(liczba_prob_na_warunek=10)
        test.uruchom_test()
        test.oblicz_i_wyswietl_wyniki()
    except ValueError as e:
        print(f"Błąd: {e}")
    except KeyboardInterrupt:
        print("\nPrzerwano test przez użytkownika.")