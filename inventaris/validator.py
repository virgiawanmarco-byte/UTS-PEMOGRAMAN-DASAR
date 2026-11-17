"""Validasi dan normalisasi data (defensive programming)."""

from inventaris.exceptions import DataFileError, InvalidRecordError

KOLOM_WAJIB = ("kode", "nama", "kategori", "stok", "harga", "supplier")


def bersihkan_teks(nilai):
    """Rapikan teks: ubah None jadi '', hapus spasi berlebih.

    Parameter : nilai (apa saja)
    Return    : str yang sudah dirapikan
    """
    return " ".join(str(nilai if nilai is not None else "").split())


def validasi_header(nama_kolom):
    """Pastikan semua kolom wajib ada.

    Parameter : nama_kolom (list[str] | None) - header dari file
    Return    : None
    Raise     : DataFileError bila ada kolom yang hilang
    """
    if not nama_kolom:
        raise DataFileError("File kosong atau tidak memiliki header.")
    hilang = set(KOLOM_WAJIB) - {k.strip().lower() for k in nama_kolom}
    if hilang:
        raise DataFileError(f"Kolom wajib hilang: {', '.join(sorted(hilang))}")


def _ke_int(teks, nama_field, nomor_baris):
    """Ubah teks ke int atau lempar InvalidRecordError."""
    try:
        return int(teks)
    except ValueError:
        raise InvalidRecordError(
            nomor_baris, f"{nama_field} harus angka bulat, ditemukan '{teks}'"
        ) from None


def validasi_baris(baris, nomor_baris):
    """Validasi satu baris data lalu kembalikan versi bersihnya.

    Parameter : baris (dict) - satu record mentah
                nomor_baris (int) - posisi di file, untuk pesan error
    Return    : dict dengan stok & harga bertipe int
    Raise     : InvalidRecordError bila ada field tidak valid
    """
    data = {k.strip().lower(): bersihkan_teks(v) for k, v in baris.items() if k}
    data["kode"] = data.get("kode", "").upper()

    for field in ("kode", "nama", "kategori", "supplier"):
        if not data.get(field):
            raise InvalidRecordError(nomor_baris, f"{field} tidak boleh kosong")

    data["stok"] = _ke_int(data.get("stok", ""), "stok", nomor_baris)
    data["harga"] = _ke_int(data.get("harga", ""), "harga", nomor_baris)

    if data["stok"] < 0:
        raise InvalidRecordError(nomor_baris, "stok tidak boleh negatif")
    if data["harga"] <= 0:
        raise InvalidRecordError(nomor_baris, "harga harus lebih dari 0")

    return {k: data[k] for k in KOLOM_WAJIB}