```markdown
# Ethereum Transaction Automation Script

Script ini ditulis dalam Python dan menggunakan library `web3.py` untuk mengotomatisasi pengiriman transaksi ETH harian ke kontrak tertentu. Program memungkinkan pengguna menentukan jumlah transaksi per hari dan jumlah hari pelaksanaan. Setiap transaksi dilakukan pada interval acak, dan transaksi akan berhenti setelah waktu yang ditentukan.

## Fitur Utama

- Mengirim transaksi ETH ke alamat kontrak yang ditentukan.
- Melakukan transaksi secara berkala dalam jangka waktu yang ditentukan.
- Mendukung multiple private key dari file `pvkey.txt`.
- Mengelola nonce dinamis untuk setiap transaksi guna menghindari kesalahan nonce.
- Retry otomatis untuk transaksi yang gagal dengan exponential backoff.
- Logging transaksi ke file `transactions.log` untuk keperluan tracking.

## Prasyarat

- Python 3.7 atau yang lebih baru
- Library `web3` untuk interaksi dengan jaringan Ethereum
- Koneksi internet untuk mengakses node Ethereum RPC

### Instalasi
   ```
1. **Install web3**  
   Jalankan perintah berikut untuk menginstall library `web3`:
   ```bash
   pip install web3
   ```

2. **Siapkan File `pvkey.txt`**  
   File `pvkey.txt` harus berisi daftar private key, dengan satu private key per baris:
   ```
   <PRIVATE_KEY_1>
   <PRIVATE_KEY_2>
   ...
   ```

3. **Pengaturan Environment Variables**  
   Pastikan untuk mengatur `RPC_URL` dan `CONTRACT_ADDRESS` sebagai environment variables untuk menjaga fleksibilitas dalam penggantian jaringan dan kontrak:

   ```python
   # Load RPC URL and Contract Address from environment variables or use defaults
   RPC_URL = os.getenv("RPC_URL", "RPC_URL_NETWORK")
   CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS", "CONTRACT_DEPOSIT")
   METHOD_ID = 'METHOD HEX'  # Method ID for the transaction
   ```

   - **`RPC_URL`**: URL RPC dari jaringan Ethereum (contohnya, Alchemy atau Infura).
   - **`CONTRACT_ADDRESS`**: Alamat kontrak tujuan untuk transaksi.
   - **`METHOD_ID`**: ID metode dalam bentuk hexadecimal yang dipakai untuk menyertakan data khusus pada transaksi (contoh: `0x12345678`).

   Atau, Anda bisa langsung mengganti `"RPC_URL_NETWORK"`, `"CONTRACT_DEPOSIT"`, dan `'METHOD HEX'` dengan nilai sesuai jaringan dan kontrak yang Anda gunakan jika ingin langsung mengedit di script.

## Cara Menggunakan

1. **Jalankan Script**  
   Jalankan program dengan perintah berikut:
   ```bash
   python nama_script.py
   ```

2. **Input Jumlah Transaksi dan Hari**  
   Saat menjalankan program, masukkan jumlah transaksi yang ingin dijalankan per hari dan jumlah hari pelaksanaan:
   ```
   Enter the number of transactions to execute each day: 5
   Enter the number of days to run the program: 3
   ```

3. **Pengaturan Waktu dan Transaksi**  
   - Transaksi dilakukan setiap hari dari pukul 07:00 hingga 18:00 UTC.
   - Script akan memulai transaksi pada waktu acak dalam interval ±20% dari rata-rata waktu jeda antar transaksi.
   - Setiap transaksi dikirim dengan nilai ETH acak antara 0.01 dan 0.05 ETH.

## Logging

Program mencatat setiap transaksi yang berhasil maupun gagal di file `transactions.log`:
- Log keberhasilan: mencatat alamat pengirim, hash transaksi, waktu UTC, dan jumlah ETH.
- Log kegagalan: mencatat alamat pengirim dan error yang terjadi saat pengiriman transaksi.

Contoh log transaksi:
```
2024-10-28 07:30:15 - [Day 1] Transaction 1 sent from 0xAbcd...Ef01 with hash: 0x1234...5678 at 2024-10-28 07:30:15 UTC and amount: 0.01234567 ETH
```

## Fungsi Utama

- **`handle_eth_transactions(amount_eth, transaction_number, day_number)`**  
  Fungsi ini menangani pengiriman transaksi ETH menggunakan nonce yang selalu diperbarui. Jika terjadi error, program akan otomatis melakukan retry dengan exponential backoff hingga maksimal 3 kali.

- **`run_daily_transactions(num_transactions, num_days)`**  
  Fungsi ini mengatur jadwal pengiriman transaksi setiap hari dan mengontrol interval antara setiap transaksi.

- **`main()`**  
  Fungsi utama yang meminta input dari pengguna untuk jumlah transaksi dan jumlah hari, lalu menjalankan transaksi berdasarkan jadwal yang ditentukan.

## Penanganan Error

Program ini memiliki beberapa penanganan error:
- **Nonce terlalu rendah**: Jika error nonce terlalu rendah terjadi, program akan mengambil nonce terbaru dari blockchain.
- **Retry otomatis**: Jika transaksi gagal karena masalah sementara, program akan mencoba ulang hingga 3 kali.

## Lisensi

Program ini dapat digunakan dan dimodifikasi sesuai kebutuhan Anda.

## Kontribusi

Anda dipersilakan untuk memberikan kontribusi pada proyek ini dengan melakukan pull request atau melaporkan issue.
```

DONATION
ademulyana.base.eth
0xF752DD7b15cA370127F0E0B7A7f36A5693dE01ad

Telegram Group : https://t.me/airdropexplorerindonesia
