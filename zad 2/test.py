import io
import sys
import unittest
from unittest.mock import patch

# Importujemy z app.py, nie stroop.py
from app import Trial, StroopTest, NAZWY_KOLOROW


class TestTrial(unittest.TestCase):
    """
    Testy dla klasy Trial: konstruktor, __str__ oraz zapis wyników.
    """
    def test_init_valid_colors(self):
        # poprawne kolory nie powinny rzucać wyjątku
        for slowo in NAZWY_KOLOROW:
            for kolor in NAZWY_KOLOROW:
                Trial(slowo, kolor, slowo == kolor)

    def test_init_invalid_colors_raises(self):
        # nieznane kolory powinny skutkować ValueError
        with self.assertRaises(ValueError):
            Trial("nieistniejący", "czerwony", True)
        with self.assertRaises(ValueError):
            Trial("czerwony", "nieistniejący", False)

    def test_str_representation(self):
        t1 = Trial("czerwony", "zielony", False)
        s = str(t1)
        self.assertIn("Niezgodny", s)
        self.assertIn("Słowo='czerwony'", s)
        self.assertIn("KolorTuszu='zielony'", s)
        t2 = Trial("fioletowy", "fioletowy", True)
        self.assertIn("Zgodny", str(t2))

    def test_zapisz_wynik_correct_and_incorrect(self):
        t = Trial("niebieski", "niebieski", True)
        t.zapisz_wynik("  NIEBIESKI  ", 0.753)
        self.assertEqual(t.odpowiedz_uzytkownika, "niebieski")
        self.assertAlmostEqual(t.czas_reakcji, 0.753, places=3)
        self.assertTrue(t.poprawna)

        t2 = Trial("zielony", "czerwony", False)
        t2.zapisz_wynik("zielony", 1.234)
        self.assertFalse(t2.poprawna)

class TestStroopTest(unittest.TestCase):
    """
    Testy dla klasy StroopTest: inicjalizacja, generowanie prób,
    zapisywanie wyników oraz wyświetlanie wyników.
    """
    def setUp(self):
        self.count = 3
        self.st = StroopTest(liczba_prob_na_warunek=self.count)

    def test_init_invalid_count(self):
        with self.assertRaises(ValueError):
            StroopTest(0)
        with self.assertRaises(ValueError):
            StroopTest(-1)

    def test_generuj_proby_count_and_flags(self):
        self.st._generuj_proby()
        proby = self.st.proby
        # 2 * count prób
        self.assertEqual(len(proby), 2 * self.count)
        # zgodne i niezgodne
        zgodne = [p for p in proby if p.zgodny]
        niezgodne = [p for p in proby if not p.zgodny]
        self.assertEqual(len(zgodne), self.count)
        self.assertEqual(len(niezgodne), self.count)
        # w próbach zgodnych slowo == kolor_tuszu
        for p in zgodne:
            self.assertEqual(p.slowo, p.kolor_tuszu)
        # w niezgodnych różne
        for p in niezgodne:
            self.assertNotEqual(p.slowo, p.kolor_tuszu)

    def test_zapisz_wynik_proby_accumulates(self):
        # przygotuj dwie próby ręcznie
        p1 = Trial("czerwony", "czerwony", True)
        p1.poprawna = True
        p1.czas_reakcji = 0.5
        p2 = Trial("niebieski", "zielony", False)
        p2.poprawna = False

        # początkowe wartości wyniki
        self.assertEqual(self.st.wyniki["zgodne_poprawne_czasy"], [])
        self.assertEqual(self.st.wyniki["liczba_niezgodnych_bledow"], 0)

        self.st._zapisz_wynik_proby(p1)
        self.st._zapisz_wynik_proby(p2)

        self.assertEqual(self.st.wyniki["zgodne_poprawne_czasy"], [0.5])
        self.assertEqual(self.st.wyniki["liczba_niezgodnych_bledow"], 1)

    @patch('app.input', return_value='')
    @patch('app.time.time', side_effect=[0, 1.2])
    def test_przeprowadz_probe_output_and_record(self, mock_time, mock_input):
        t = Trial("czerwony", "czerwony", True)
        buf = io.StringIO()
        sys_stdout = sys.stdout
        sys.stdout = buf
        try:
            self.st._przeprowadz_probe(t)
        finally:
            sys.stdout = sys_stdout
        text = buf.getvalue().lower()
        # sprawdzamy, czy wydrukowano słowo oraz komunikat o błędzie
        self.assertIn("czerwony", text)
        self.assertIn("błąd", text)
        # sprawdź ustawienie czasu i poprawność
        self.assertAlmostEqual(t.czas_reakcji, 1.2, places=3)
        self.assertFalse(t.poprawna)

    def test_oblicz_i_wyswietl_wyniki_various(self):
        # ustaw ręcznie wyniki
        self.st.wyniki = {
            "zgodne_poprawne_czasy": [0.4, 0.6],
            "niezgodne_poprawne_czasy": [1.1, 1.3],
            "liczba_zgodnych_bledow": 1,
            "liczba_niezgodnych_bledow": 2
        }
        buf = io.StringIO()
        sys_stdout = sys.stdout
        sys.stdout = buf
        try:
            self.st.oblicz_i_wyswietl_wyniki()
        finally:
            sys.stdout = sys_stdout
        out = buf.getvalue()
        # średnie czasy
        self.assertIn("średni czas (zgodne): 0.500 s", out.lower())
        self.assertIn("średni czas (niezgodne): 1.200 s", out.lower())
        # liczniki
        self.assertIn("błędy (zgodne): 1", out.lower())
        self.assertIn("błędy (niezgodne): 2", out.lower())
        # efekt stroopa = 0.7
        self.assertIn("efekt stroopa: 0.700 s", out.lower())

if __name__ == '__main__':
    unittest.main()