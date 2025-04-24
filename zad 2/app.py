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

print(Fore.RED + 'Ten tekst jest czerwony')
print(Fore.GREEN + Back.YELLOW + 'Ten tekst jest zielony na żółtym tle')
print(Fore.BLUE + Style.BRIGHT + 'Ten tekst jest jasno niebieski i pogrubiony')
print('Ten tekst jest już w domyślnym kolorze.')  # autoreset=True

class Trial: # reprezentuje pojedynczą próbę w teście stroopa
    def __init__(self, slowo, kolor_tuszu, zgodny):
        if slowo not in mapowane_kolorki or kolor_tuszu not in mapowane_kolorki:
            raise ValueError("ej! użyto nieznanego koloru.")
        self.slowo = slowo
        self.kolor_tuszu = kolor_tuszu
        self.zgodny = zgodny
        self.czas_reakcji = None
        self.odpowiedz_uzytkownika = None
        self.poprawna = None

    def __str__(self):
        typ = "Zgodny" if self.zgodny else "Niezgodny"
        return f"Próba ({typ}): Słowo='{self.slowo}', KolorTuszu='{self.kolor_tuszu}'"

    def zapisz_wynik(self, odpowiedz, czas):
        self.odpowiedz_uzytkownika = odpowiedz.lower().strip()
        self.czas_reakcji = czas
        self.poprawna = (self.odpowiedz_uzytkownika == self.kolor_tuszu)

class StroopTest: # zarządza przebiegiem testu Stroopa
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
        # Zgodne
        for _ in range(self.liczba_prob_na_warunek):
            kolor = random.choice(NAZWY_KOLOROW)
            self.proby.append(Trial(kolor, kolor, True))
        # Niezgodne
        for _ in range(self.liczba_prob_na_warunek):
            slowo = random.choice(NAZWY_KOLOROW)
            kolor_tuszu = random.choice(NAZWY_KOLOROW)
            while kolor_tuszu == slowo:
                kolor_tuszu = random.choice(NAZWY_KOLOROW)
            self.proby.append(Trial(slowo, kolor_tuszu, False))
        random.shuffle(self.proby)

    def _wyswietl_instrukcje(self):
        print("--- Test Stroopa ---")
        print("Instrukcja:")
        print("Na ekranie pojawi się słowo (nazwa koloru).")
        print("Twoim zadaniem jest jak najszybsze podanie nazwy koloru,")
        print("w jakim to słowo jest wyświetlone.")
        print("Ignoruj znaczenie słowa – skup się wyłącznie na kolorze druku.")
        print(f"Dostępne kolory: {', '.join(NAZWY_KOLOROW)}")
        print(f"\nTest będzie się składał z {len(self.proby)} prób.")
        input("Naciśnij Enter, aby rozpocząć...")
        print("-" * 40)

    def _przeprowadz_probe(self, proba: Trial):  # colorama, by wyświetlić słowo we właściwym kolorze:
        kolor = mapowane_kolorki[proba.kolor_tuszu]      # słowo drukujemy wielkimi literami, w kolorze tuszu.
        print(kolor + proba.slowo.upper() + Style.RESET_ALL)
        sys.stdout.write("Podaj kolor, który widzisz: ")
        sys.stdout.flush()

        start = time.time()
        odp = input()
        koniec = time.time()

        proba.zapisz_wynik(odp, koniec - start)
        if proba.poprawna:
            print(f"Dobrze! Czas: {proba.czas_reakcji:.3f} s")
        else:
            print(f"Błąd. Poprawna odpowiedź to: {proba.kolor_tuszu}. Twój czas: {proba.czas_reakcji:.3f} s")
        time.sleep(0.5)

    def _zapisz_wynik_proby(self, proba):
        if proba.poprawna:
            if proba.zgodny:
                self.wyniki["zgodne_poprawne_czasy"].append(proba.czas_reakcji)
            else:
                self.wyniki["niezgodne_poprawne_czasy"].append(proba.czas_reakcji)
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
            self._przeprowadz_probe(p)
            self._zapisz_wynik_proby(p)
        print("\n--- Koniec Testu. Dzięki! ---")

    def oblicz_i_wyswietl_wyniki(self):
        print("\n--- O to wyniki: ---")
        if self.wyniki["zgodne_poprawne_czasy"]:
            scz = sum(self.wyniki["zgodne_poprawne_czasy"]) / len(self.wyniki["zgodne_poprawne_czasy"])
            print(f"Średni czas (zgodne): {scz:.3f} s")
        else:
            print("Brak poprawnych odpowiedzi w próbach zgodnych.")
        if self.wyniki["niezgodne_poprawne_czasy"]:
            snc = sum(self.wyniki["niezgodne_poprawne_czasy"]) / len(self.wyniki["niezgodne_poprawne_czasy"])
            print(f"Średni czas (niezgodne): {snc:.3f} s")
        else:
            print("Brak poprawnych odpowiedzi w próbach niezgodnych.")
        bz = len(self.wyniki["zgodne_poprawne_czasy"])
        bn = len(self.wyniki["niezgodne_poprawne_czasy"])
        ez = self.wyniki["liczba_zgodnych_bledow"]
        en = self.wyniki["liczba_niezgodnych_bledow"]
        print(f"\nPoprawne (zgodne): {bz}, Błędy (zgodne): {ez}")
        print(f"Poprawne (niezgodne): {bn}, Błędy (niezgodne): {en}")
        if bz and bn:
            efekt = (sum(self.wyniki["niezgodne_poprawne_czasy"]) / bn) - (sum(self.wyniki["zgodne_poprawne_czasy"]) / bz)
            print(f"\nEfekt Stroopa: {efekt:.3f} s")
            if efekt > 0:
                print("(odpowiedzi na próby niezgodne są wolniejsze.)")
            else:
                print("(Nie zaobserwowano typowego efektu Stroopa.)")

if __name__ == "__main__":
    try:
        test = StroopTest(liczba_prob_na_warunek=10)
        test.uruchom_test()
        test.oblicz_i_wyswietl_wyniki()
    except ValueError as e:
        print(f"Błąd: {e}")
    except KeyboardInterrupt:
        print("\nuser przerwał test.")
