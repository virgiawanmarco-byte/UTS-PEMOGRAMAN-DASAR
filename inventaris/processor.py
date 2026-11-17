"""Logika pengolahan data murni (tanpa print dan tanpa akses file)."""


def hapus_duplikat(records):
    """Buang record dengan kode yang sudah pernah muncul (SET dipakai untuk cek cepat).

    Parameter : records (list[dict])
    Return    : tuple (list unik, list duplikat)
    """
    kode_terlihat = set()
    unik, duplikat = [], []
    for r in records:
        if r["kode"] in kode_terlihat:
            duplikat.append(r)
        else:
            kode_terlihat.add(r["kode"])
            unik.append(r)
    return unik, duplikat


def cari_barang(records, kata_kunci):
    """Cari barang berdasarkan potongan nama atau kode (tidak peka huruf besar/kecil).

    Raise : ValueError bila kata kunci kosong
    """
    kunci = kata_kunci.strip().lower()
    if not kunci:
        raise ValueError("Kata kunci pencarian tidak boleh kosong.")
    return [r for r in records if kunci in r["nama"].lower() or kunci in r["kode"].lower()]


def filter_stok_menipis(records, batas=10):
    """Ambil barang dengan stok <= batas, urut dari stok paling sedikit.

    Raise : ValueError bila batas negatif
    """
    if batas < 0:
        raise ValueError("Batas stok tidak boleh negatif.")
    return sorted((r for r in records if r["stok"] <= batas), key=lambda r: r["stok"])


def kelompokkan_per_kategori(records):
    """Kelompokkan record per kategori. Return: dict {kategori: [record, ...]}"""
    kelompok = {}
    for r in records:
        kelompok.setdefault(r["kategori"], []).append(r)
    return kelompok


def rekap_kategori(records):
    """Hitung jumlah jenis, total stok, dan nilai persediaan per kategori.

    Return : dict {kategori: {"jumlah_jenis", "total_stok", "nilai_persediaan"}}
             (dict kosong bila records kosong -> edge case)
    """
    kelompok = kelompokkan_per_kategori(records)
    return {
        kategori: {
            "jumlah_jenis": len(items),
            "total_stok": sum(i["stok"] for i in items),
            "nilai_persediaan": sum(i["stok"] * i["harga"] for i in items),
        }
        for kategori, items in kelompok.items()
    }


def daftar_supplier(records):
    """Kumpulan supplier unik (SET comprehension)."""
    return {r["supplier"] for r in records}


def nilai_total(records):
    """Total nilai persediaan seluruh barang (stok x harga)."""
    return sum(r["stok"] * r["harga"] for r in records)