"""Antarmuka command line: argparse + menu interaktif."""

import argparse
import os
import sys

from inventaris import loader, processor, report
from inventaris.exceptions import DataFileError

FILE_DEFAULT = os.path.join("data", "input", "inventaris.csv")
FOLDER_OUTPUT_DEFAULT = os.path.join("data", "output")
BATAS_DEFAULT = 10


def buat_parser():
    """Bangun parser argumen. Return: argparse.ArgumentParser"""
    parser = argparse.ArgumentParser(
        prog="main.py", description="Aplikasi pengolah data inventaris toko (CLI)."
    )
    parser.add_argument("--file", default=FILE_DEFAULT, help="file input .csv/.json")
    parser.add_argument("--out", default=FOLDER_OUTPUT_DEFAULT, help="folder output")
    sub = parser.add_subparsers(dest="perintah")

    sub.add_parser("rekap", help="rekap stok & nilai per kategori")
    p_cari = sub.add_parser("cari", help="cari barang berdasarkan nama/kode")
    p_cari.add_argument("kata_kunci")
    p_menipis = sub.add_parser("menipis", help="tampilkan barang stok menipis")
    p_menipis.add_argument("--batas", type=int, default=BATAS_DEFAULT)
    sub.add_parser("bersihkan", help="hapus duplikat & tampilkan data bersih")
    sub.add_parser("ekspor", help="simpan hasil olahan ke CSV & JSON")
    sub.add_parser("menu", help="mode menu interaktif")
    return parser


def muat_data(path):
    """Baca file, tampilkan ringkasan, hapus duplikat.

    Return : tuple (list unik, list duplikat)
    Raise  : DataFileError
    """
    valid, ditolak = loader.baca_data(path)
    unik, duplikat = processor.hapus_duplikat(valid)
    print(f"[INFO] {path}: {len(valid)} baris valid, "
          f"{len(duplikat)} duplikat dibuang, {len(ditolak)} baris ditolak.")
    for pesan in ditolak:
        print(f"[PERINGATAN] {pesan}")
    return unik, duplikat


def tampilkan_rekap(records):
    """Cetak rekap per kategori."""
    print(report.format_rekap(processor.rekap_kategori(records),
                              processor.nilai_total(records)))
    print("Supplier unik:", ", ".join(sorted(processor.daftar_supplier(records))) or "-")


def ekspor_semua(records, folder):
    """Simpan data bersih, stok menipis (CSV) dan rekap (JSON) ke folder.

    Return : list path file yang dihasilkan
    """
    rekap = processor.rekap_kategori(records)
    ringkasan = {
        "total_jenis_barang": len(records),
        "nilai_total_persediaan": processor.nilai_total(records),
        "rekap_kategori": rekap,
        "supplier": sorted(processor.daftar_supplier(records)),
    }
    path_bersih = os.path.join(folder, "inventaris_bersih.csv")
    path_menipis = os.path.join(folder, "stok_menipis.csv")
    path_rekap = os.path.join(folder, "rekap.json")
    loader.simpan_csv(records, path_bersih)
    loader.simpan_csv(processor.filter_stok_menipis(records, BATAS_DEFAULT), path_menipis)
    loader.simpan_json(ringkasan, path_rekap)
    return [path_bersih, path_menipis, path_rekap]


def baca_angka(pesan, default):
    """Minta angka bulat >= 0 dari pengguna; ulangi sampai valid.

    Parameter : pesan (str) prompt, default (int) dipakai bila input kosong
    Return    : int
    """
    while True:
        teks = input(pesan).strip()
        if teks == "":
            return default
        try:
            nilai = int(teks)
        except ValueError:
            print("  Input harus berupa angka bulat.")
            continue
        if nilai < 0:
            print("  Angka tidak boleh negatif.")
            continue
        return nilai


MENU = """
=== INVENTARIS TOKO ===
1. Lihat semua barang
2. Rekap per kategori
3. Cari barang
4. Barang stok menipis
5. Ekspor hasil
0. Keluar"""


def mode_menu(records, folder_output):
    """Loop menu interaktif dengan validasi input."""
    while True:
        print(MENU)
        try:
            pilihan = input("Pilih menu: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nKeluar.")
            return
        if pilihan == "1":
            print(report.format_tabel(records))
        elif pilihan == "2":
            tampilkan_rekap(records)
        elif pilihan == "3":
            try:
                hasil = processor.cari_barang(records, input("Kata kunci: "))
                print(report.format_tabel(hasil))
            except ValueError as err:
                print(f"  {err}")
        elif pilihan == "4":
            batas = baca_angka(f"Batas stok [{BATAS_DEFAULT}]: ", BATAS_DEFAULT)
            print(report.format_tabel(processor.filter_stok_menipis(records, batas)))
        elif pilihan == "5":
            for path in ekspor_semua(records, folder_output):
                print("  Tersimpan:", path)
        elif pilihan == "0":
            print("Sampai jumpa!")
            return
        else:
            print("  Pilihan tidak dikenal, coba lagi (0-5).")


def jalankan(argv=None):
    """Titik masuk aplikasi.

    Parameter : argv (list[str] | None) - argumen CLI, None = sys.argv
    Return    : int exit code (0 sukses, 1 error data, 2 error argumen)
    """
    parser = buat_parser()
    args = parser.parse_args(argv)
    if args.perintah is None:
        parser.print_help()
        return 2
    try:
        records, _ = muat_data(args.file)
        if args.perintah == "rekap":
            tampilkan_rekap(records)
        elif args.perintah == "cari":
            print(report.format_tabel(processor.cari_barang(records, args.kata_kunci)))
        elif args.perintah == "menipis":
            print(report.format_tabel(processor.filter_stok_menipis(records, args.batas)))
        elif args.perintah == "bersihkan":
            print(report.format_tabel(records))
        elif args.perintah == "ekspor":
            for path in ekspor_semua(records, args.out):
                print("Tersimpan:", path)
        elif args.perintah == "menu":
            mode_menu(records, args.out)
    except DataFileError as err:
        print(f"[ERROR] {err}", file=sys.stderr)
        return 1
    except ValueError as err:
        print(f"[ERROR] Input tidak sesuai: {err}", file=sys.stderr)
        return 2
    return 0