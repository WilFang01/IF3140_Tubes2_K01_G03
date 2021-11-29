# Serial Optimistic Concurrency Control

## Phase Serial OCC :
Transaksi pada optimistic concurrency control ini dibagi menjadi 3 fase :
1. Read Phase : Eksekusi transaksi dan update pada local
2. Validation Phase : Pengecekan terhadap eksekusi dari transaksi apakah sudah benar. Jika tidak, melakukan abort terhadap transaksi
3. Write Phase : Transfer data dari local ke database

## Cara menjalankan program :
1. Masuk ke folder OCC
2. Jalankan `python OCC.py`
3. Masukkan jumlah transaksi (Contoh : dalam kasus [T1,T2,T3], artinya terdapat 3 transaksi)
4. Masukkan jumlah schedule (read, write, commit)
5. Masukkan data seluruh schedule dengan format yang sesuai
6. Program OCC akan berjalan

## Author :
Kelompok G03 - K1 MBD 2021/2022