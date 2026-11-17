"""Format tampilan teks untuk terminal."""


def rupiah(angka):
    """Format int ke 'Rp 1.250.000'."""
    return "Rp " + f"{angka:,}".replace(",", ".")


def format_tabel(records):
    """Ubah list record menjadi tabel teks. Return: str"""
    if not records:
        return "(tidak ada data)"
    judul = f"{'Kode':<8}{'Nama':<22}{'Kategori':<16}{'Stok':>6}{'Harga':>12}"
    garis = "-" * len(judul)
    baris = [
        f"{r['kode']:<8}{r['nama'][:21]:<22}{r['kategori']:<16}{r['stok']:>6}{rupiah(r['harga']):>12}"
        for r in records
    ]
    return "\n".join([judul, garis, *baris])


def format_rekap(rekap, total):
    """Format hasil rekap per kategori. Return: str"""
    if not rekap:
        return "(tidak ada data untuk direkap)"
    judul = f"{'Kategori':<16}{'Jenis':>7}{'Total Stok':>12}{'Nilai Persediaan':>20}"
    garis = "-" * len(judul)
    baris = [
        f"{kat:<16}{v['jumlah_jenis']:>7}{v['total_stok']:>12}{rupiah(v['nilai_persediaan']):>20}"
        for kat, v in sorted(rekap.items())
    ]
    return "\n".join([judul, garis, *baris, garis, f"{'TOTAL':<35}{rupiah(total):>20}"])