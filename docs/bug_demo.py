"""Versi AWAL (buggy) pembacaan stok - dipakai untuk demo debugging. Jangan dipakai di aplikasi."""
import csv

with open("data/input/inventaris.csv", newline="", encoding="utf-8-sig") as f:
    for baris in csv.DictReader(f):
        stok = int(baris["stok"])   # BUG: tidak ada penanganan error
