import io
import sys
import unittest
from unittest.mock import patch
import runpy
from parameterized import parameterized

from app import Proba, TestStroopa, NAZWY_KOLOROW

class TestProba(unittest.TestCase):
    """
    Testy dla klasy Proba: konstruktor, __str__, zapis wyników oraz wyjątki.
    """
    def setUp(self):
        # Wspólna instancja poprawnej próby
        self.sample = Proba("czerwony", "czerwony", True)

    def test_init_valid_colors(self):
        for slowo in NAZWY_KOLOROW:
            for kolor in NAZWY_KOLOROW:
                Proba(slowo, kolor, slowo == kolor)

    def test_init_invalid_colors_raises(self):
        with self.assertRaises(ValueError):
            Proba("nieistniejący", "czerwony", True)
        with self.assertRaises(ValueError):
            Proba("czerwony", "nieistniejący", False)

    def test_str_representation(self):
        s = str(self.sample)
        self.assertIn("Proba", s)
        self.assertIn("Słowo='czerwony'", s)
        self.assertIn("KolorDruku='czerwony'", s)
        # zgodny typ
        p2 = Proba("fioletowy", "fioletowy", True)
        self.assertIn("Zgodny", str(p2))

    @parameterized.expand([
        ("correct_case", "  NIEBIESKI  ", True),
        ("incorrect_case", "zielony", False),
    ])
    def test_zapisz_wynik_various(self, name, input_str, expected_correct):
        # test dla p = Proba("niebieski","niebieski",True)
        p = Proba("niebieski", "niebieski", True)
        p.zapisz_wynik(input_str, 1.234)
        self.assertEqual(p.odpowiedz_uzytkownika, input_str.strip().lower())
        self.assertAlmostEqual(p.czas_reakcji, 1.234, places=3)
        self.assertEqual(p.poprawna, expected_correct)

class TestTestStroopa(unittest.TestCase):
    """
    Testy dla klasy TestStroopa: inicjalizacja, generowanie prób, zapis wyników i obsługa wyjątków.
    """
    def setUp(self):
        self.count = 3
        self.test = TestStroopa(liczba_prob_na_warunek=self.count)

    def test_init_invalid_count(self):
        with self.assertRaises(ValueError):
            TestStroopa(0)
        with self.assertRaises(ValueError):
            TestStroopa(-1)

    def test_generuj_proby_count_and_flags(self):
        self.test._generuj_proby()
        proby = self.test.proby
        self.assertEqual(len(proby), 2 * self.count)
        zgodne = [p for p in proby if p.zgodny]
        niezgodne = [p for p in proby if not p.zgodny]
        self.assertEqual(len(zgodne), self.count)
        self.assertEqual(len(niezgodne), self.count)
        for p in zgodne:
            self.assertEqual(p.slowo, p.kolor_druku)
        for p in niezgodne:
            self.assertNotEqual(p.slowo, p.kolor_druku)

    def test_zapisz_wynik_proby_accumulates(self):
        p1 = Proba("czerwony", "czerwony", True)
        p1.poprawna = True
        p1.czas_reakcji = 0.5
        p2 = Proba("niebieski", "zielony", False)
        p2.poprawna = False
        self.test._zapisz_wynik_proby(p1)
        self.test._zapisz_wynik_proby(p2)
        self.assertEqual(self.test.wyniki["zgodne_poprawne_czasy"], [0.5])
        self.assertEqual(self.test.wyniki["liczba_niezgodnych_bledow"], 1)

    @patch('app.input', return_value='')
    @patch('app.time.time', side_effect=[0, 1.2])
    def test_przeprowadz_proba_output_and_record(self, mock_time, mock_input):
        p = Proba("czerwony", "czerwony", True)
        buf = io.StringIO()
        old = sys.stdout
        sys.stdout = buf
        try:
            self.test._przeprowadz_proba(p)
        finally:
            sys.stdout = old
        text = buf.getvalue().lower()
        self.assertIn("czerwony", text)
        self.assertIn("błąd", text)
        self.assertAlmostEqual(p.czas_reakcji, 1.2, places=3)
        self.assertFalse(p.poprawna)

    def test_oblicz_i_wyswietl_wyniki_various(self):
        self.test.wyniki = {
            "zgodne_poprawne_czasy": [0.4, 0.6],
            "niezgodne_poprawne_czasy": [1.1, 1.3],
            "liczba_zgodnych_bledow": 1,
            "liczba_niezgodnych_bledow": 2
        }
        buf = io.StringIO()
        old = sys.stdout
        sys.stdout = buf
        try:
            self.test.oblicz_i_wyswietl_wyniki()
        finally:
            sys.stdout = old
        out = buf.getvalue().lower()
        self.assertIn("średni czas (zgodne): 0.500 s", out)
        self.assertIn("średni czas (niezgodne): 1.200 s", out)
        self.assertIn("błędy (zgodne): 1", out)
        self.assertIn("błędy (niezgodne): 2", out)
        self.assertIn("efekt stroopa: 0.700 s", out)

    def test_main_keyboard_interrupt(self):
        # symulacja przerwania testu w __main__, uruchomienie jako __main__
        buf = io.StringIO()
        old = sys.stdout
        sys.stdout = buf
        try:
            with patch('app.TestStroopa.uruchom_test', side_effect=KeyboardInterrupt):
                runpy.run_module('app', run_name="__main__")
        finally:
            sys.stdout = old
        self.assertIn("przerwano test przez użytkownika", buf.getvalue().lower())

if __name__ == '__main__':
    unittest.main()