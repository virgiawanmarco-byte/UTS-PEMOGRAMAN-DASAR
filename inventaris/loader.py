"""Membaca dan menulis file CSV / JSON."""

import csv
import json
import os

from inventaris.exceptions import DataFileError, InvalidRecordError
from inventaris.validator import KOLOM_WAJIB, validasi_baris, validasi_header


def baca_csv(path):
    """Baca file CSV inventaris.

    Parameter : path (str)
    Return    : tuple (list[dict] valid, list[str] pesan baris ditolak)
    Raise     : DataFileError bila file hilang/rusak
    """
    if not os.path.isfile(path):
        raise DataFileError(f"File tidak ditemukan: {path}")
    valid, ditolak = [], []
    try:
        with open(path, newline="", encoding="utf-8-sig") as f:
            pembaca = csv.DictReader(f)
            validasi_header(pembaca.fieldnames)
            for nomor, baris in enumerate(pembaca, start=2):  # baris 1 = header
                try:
                    valid.append(validasi_baris(baris, nomor))
                except InvalidRecordError as err:
                    ditolak.append(str(err))
    except (OSError, UnicodeDecodeError, csv.Error) as err:
        raise DataFileError(f"Gagal membaca {path}: {err}") from err
    return valid, ditolak


def baca_json(path):
    """Baca file JSON berisi list of object.

    Return : tuple (list[dict] valid, list[str] pesan baris ditolak)
    Raise  : DataFileError
    """
    if not os.path.isfile(path):
        raise DataFileError(f"File tidak ditemukan: {path}")
    try:
        with open(path, encoding="utf-8") as f:
            isi = json.load(f)
    except json.JSONDecodeError as err:
        raise DataFileError(f"JSON tidak valid di {path}: {err}") from err
    except (OSError, UnicodeDecodeError) as err:
        raise DataFileError(f"Gagal membaca {path}: {err}") from err

    if not isinstance(isi, list):
        raise DataFileError("JSON harus berupa list of object.")
    valid, ditolak = [], []
    for nomor, item in enumerate(isi, start=1):
        try:
            if not isinstance(item, dict):
                raise InvalidRecordError(nomor, "item bukan object")
            valid.append(validasi_baris(item, nomor))
        except InvalidRecordError as err:
            ditolak.append(str(err))
    return valid, ditolak


def baca_data(path):
    """Pilih pembaca berdasarkan ekstensi file (.csv atau .json)."""
    ekstensi = os.path.splitext(path)[1].lower()
    if ekstensi == ".csv":
        return baca_csv(path)
    if ekstensi == ".json":
        return baca_json(path)
    raise DataFileError(f"Format '{ekstensi}' tidak didukung (gunakan .csv/.json).")


def _siapkan_folder(path):
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)


def simpan_csv(records, path):
    """Simpan list of dict ke CSV. Return: jumlah baris yang ditulis."""
    try:
        _siapkan_folder(path)
        with open(path, "w", newline="", encoding="utf-8") as f:
            penulis = csv.DictWriter(f, fieldnames=KOLOM_WAJIB)
            penulis.writeheader()
            penulis.writerows(records)
    except OSError as err:
        raise DataFileError(f"Gagal menulis {path}: {err}") from err
    return len(records)


def simpan_json(data, path):
    """Simpan data (dict/list) ke JSON. Return: path file."""
    try:
        _siapkan_folder(path)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except (OSError, TypeError) as err:
        raise DataFileError(f"Gagal menulis {path}: {err}") from err
    return path