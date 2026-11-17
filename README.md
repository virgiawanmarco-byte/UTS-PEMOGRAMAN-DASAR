# Aplikasi Pengolah Data Inventaris Toko (CLI)

UTS Pemrograman Dasar (TK091) - Universitas Amikom Yogyakarta, Semester Ganjil 2026/2027
Nama: Marco Virgiawan Prabuarto | NIM: 25.83.1220 | Link repository: https://github.com/virgiawanmarco-byte/UTS-PEMOGRAMAN-DASAR.git

## Deskripsi
Aplikasi command line berbasis Python (hanya standard library) untuk mengolah data
persediaan barang toko kelontong: rekap per kategori, pencarian, filter stok menipis,
penghapusan duplikat, dan ekspor hasil ke CSV/JSON.

- **Target pengguna**: pemilik / penjaga toko kecil.
- **Input**: file `.csv` atau `.json` dengan kolom `kode, nama, kategori, stok, harga, supplier`.
- **Output**: tabel di terminal + file `inventaris_bersih.csv`, `stok_menipis.csv`, `rekap.json`.

## Persyaratan
- Python 3.8 atau lebih baru
- **Tidak ada dependency eksternal** (hanya `argparse, csv, json, os, sys, tempfile, unittest`)

## Cara Menjalankan
Jalankan dari folder root proyek (yang berisi `main.py`):

```bash
python main.py rekap                          # rekap stok & nilai per kategori
python main.py cari gula                      # cari berdasarkan nama/kode
python main.py menipis --batas 10             # barang dengan stok <= 10
python main.py bersihkan                      # tampilkan data tanpa duplikat
python main.py ekspor                         # tulis hasil ke data/output/
python main.py menu                           # mode menu interaktif
python main.py --file data/input/inventaris_contoh.json rekap   # input JSON
python main.py --file data/input/inventaris_kosong.csv rekap    # edge case file kosong
```

Opsi global: `--file <path>` (default `data/input/inventaris.csv`), `--out <folder>` (default `data/output`).
Di Windows gunakan `python` atau `py`; di Linux/macOS bisa `python3`.

Menjalankan unit test:
```bash
python -m unittest discover -s tests -v
```

## Struktur Program
```
uts_inventaris/
├── main.py                  # entry point
├── README.md
├── inventaris/              # package buatan sendiri
│   ├── __init__.py
│   ├── cli.py               # argparse + menu interaktif (orkestrasi)
│   ├── loader.py            # baca/tulis CSV & JSON
│   ├── validator.py         # validasi & normalisasi data
│   ├── processor.py         # logika pengolahan data (murni)
│   ├── report.py            # format tampilan teks
│   └── exceptions.py        # exception khusus
├── data/input/              # contoh file input (normal, kosong, JSON)
├── data/output/             # hasil ekspor + hasil_run.txt
├── tests/test_inventaris.py # 10 unit test
└── docs/                    # catatan debugging
```

Alur dependensi: `main -> cli -> (loader -> validator -> exceptions), processor, report`.
`processor` dan `report` tidak mengakses file; `loader` tidak mencetak ke layar (single responsibility).

## Penanganan Error
| Kondisi | Penanganan |
|---|---|
| File tidak ditemukan / format tidak didukung / header hilang | `DataFileError`, pesan `[ERROR]`, exit code 1 |
| Baris tidak valid (stok `abc`, negatif, nama kosong) | `InvalidRecordError`, baris dilewati + `[PERINGATAN]` |
| Argumen tidak sesuai (`--batas -5`, kata kunci kosong) | `ValueError`, exit code 2 |
| Input menu salah | diulang sampai valid; Ctrl+C/EOF keluar dengan rapi |

## Referensi dan Bantuan AI
- Dokumentasi resmi Python (docs.python.org): modul csv, json, argparse, unittest.
- Library: hanya Python standard library, tidak ada dependency eksternal.
- Bantuan AI: saya menggunakan Claude (Anthropic) untuk membantu menyusun
  rancangan aplikasi, kode program, unit test, README, dan lembar jawaban.
  Saya menjalankan sendiri program di komputer saya, menguji hasilnya,
  mengunggah proyek ke GitHub, dan mempelajari cara kerja kodenya.
