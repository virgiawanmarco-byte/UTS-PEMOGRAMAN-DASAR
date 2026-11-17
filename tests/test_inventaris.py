"""Unit test (standard library unittest). Jalankan: python -m unittest discover -s tests -v"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inventaris import loader, processor
from inventaris.exceptions import DataFileError, InvalidRecordError
from inventaris.validator import validasi_baris

CONTOH = [
    {"kode": "A1", "nama": "Gula", "kategori": "Sembako", "stok": 10, "harga": 1000, "supplier": "S1"},
    {"kode": "A2", "nama": "Beras", "kategori": "Sembako", "stok": 0, "harga": 2000, "supplier": "S2"},
    {"kode": "A1", "nama": "Gula", "kategori": "Sembako", "stok": 10, "harga": 1000, "supplier": "S1"},
]


class TestProcessor(unittest.TestCase):
    def test_hapus_duplikat(self):
        unik, dup = processor.hapus_duplikat(CONTOH)
        self.assertEqual(len(unik), 2)
        self.assertEqual(len(dup), 1)

    def test_rekap_normal(self):
        unik, _ = processor.hapus_duplikat(CONTOH)
        self.assertEqual(processor.rekap_kategori(unik)["Sembako"]["nilai_persediaan"], 10000)

    def test_rekap_data_kosong_edge_case(self):
        self.assertEqual(processor.rekap_kategori([]), {})
        self.assertEqual(processor.nilai_total([]), 0)

    def test_stok_nol_masuk_menipis(self):
        hasil = processor.filter_stok_menipis(CONTOH, 0)
        self.assertEqual([r["kode"] for r in hasil], ["A2"])

    def test_cari_kata_kunci_kosong(self):
        with self.assertRaises(ValueError):
            processor.cari_barang(CONTOH, "   ")


class TestValidator(unittest.TestCase):
    def test_stok_bukan_angka(self):
        with self.assertRaises(InvalidRecordError):
            validasi_baris({**CONTOH[0], "stok": "abc"}, 2)

    def test_normalisasi_kode(self):
        hasil = validasi_baris({**CONTOH[0], "kode": " a1 "}, 2)
        self.assertEqual(hasil["kode"], "A1")


class TestLoader(unittest.TestCase):
    def test_file_tidak_ada(self):
        with self.assertRaises(DataFileError):
            loader.baca_csv("tidak_ada.csv")

    def test_header_hilang(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "x.csv")
            with open(p, "w") as f:
                f.write("kode,nama\nA,B\n")
            with self.assertRaises(DataFileError):
                loader.baca_csv(p)

    def test_roundtrip_csv(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "out.csv")
            loader.simpan_csv(CONTOH[:2], p)
            valid, ditolak = loader.baca_csv(p)
            self.assertEqual(valid, CONTOH[:2])
            self.assertEqual(ditolak, [])


if __name__ == "__main__":
    unittest.main()
