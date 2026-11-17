# Catatan Debugging

## Skenario error
Versi awal pembacaan data memakai `int(baris["stok"])` tanpa penanganan error (`docs/bug_demo.py`).
Pada data yang mengandung `stok = abc` (baris 15), program langsung berhenti:

```
Traceback (most recent call last):
  File "docs/bug_demo.py", line 6, in <module>
    stok = int(baris["stok"])   # BUG: tidak ada penanganan error
ValueError: invalid literal for int() with base 10: 'abc'
```

## Langkah debugging
1. **Reproduksi**: jalankan `python docs/bug_demo.py`, error muncul konsisten.
2. **Baca traceback dari bawah**: `ValueError ... 'abc'` -> ada nilai non-angka pada kolom stok.
3. **Lokalisasi**: tambahkan `print(repr(baris))` sebelum `int(...)` (atau `breakpoint()` lalu `p baris`)
   -> terlihat `{'kode': 'BRG013', ..., 'stok': 'abc', ...}`.
4. **Akar masalah**: program berasumsi semua data bersih (tidak defensif).
5. **Perbaikan**: konversi dipindah ke `validator._ke_int()` dengan `try/except ValueError` yang
   melempar `InvalidRecordError` membawa nomor baris; `loader` menangkapnya, mengumpulkan pesan,
   dan melanjutkan ke baris berikutnya.
6. **Verifikasi**: `python main.py rekap` -> `[PERINGATAN] Baris 15: stok harus angka bulat, ditemukan 'abc'`
   dan unit test `test_stok_bukan_angka` lulus.
