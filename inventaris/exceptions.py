"""Exception khusus aplikasi agar penanganan error spesifik dan jelas."""


class InventarisError(Exception):
    """Kelas induk semua error aplikasi ini."""


class DataFileError(InventarisError):
    """File tidak ditemukan, tidak bisa dibaca/ditulis, atau formatnya rusak."""


class InvalidRecordError(InventarisError):
    """Satu baris data tidak valid (misal stok bukan angka)."""

    def __init__(self, nomor_baris, pesan):
        self.nomor_baris = nomor_baris
        self.pesan = pesan
        super().__init__(f"Baris {nomor_baris}: {pesan}")