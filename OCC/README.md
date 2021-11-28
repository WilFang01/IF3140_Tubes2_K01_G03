# Serial Optimistic Concurrency Control

## Phase Serial OCC :
Transaksi pada optimistic concurrency control ini dibagi menjadi 3 fase :
1. Read Phase : Eksekusi transaksi dan update pada local
2. Validation Phase : Pengecekan terhadap eksekusi dari transaksi apakah sudah benar. Jika tidak, melakukan abort terhadap transaksi
3. Write Phase : Transfer data dari local ke database

## Author :
Kelompok G03 - K1 MBD 2021/2022