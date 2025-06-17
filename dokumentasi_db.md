# Ini adalah dokumentasi database untuk aplikasi web lapKeu

## Dokumentasi ini dibuat oleh Abdullah Afif Habiburrohman

### NIM: 24/537611/SV/24441 ; Teknologi Rekayasa Perangkat Lunak D-IV UGM angkatan 24

# Summary

## Syarat kelengkapan untuk dipenuhi:

1. Jumlah tabel: min. 5
2. Jumlah query complex (JOIN, subquery, dst): min. 3
3. Jumlah view dan/atau fungsi: min. 2
4. Jumlah Prosedur: min. 1
5. Jumlah Trigger: min. 2

## Versi database:

phpMyAdmin versi: 5.2.1deb3
Versi server: 8.0.42-0ubuntu0.24.04.1
Versi PHP: 8.3.6

## Target yang sudah dipenuhi:

1. Jumlah tabel: 7 tabel
2. Jumlah query complex: 5+ pada PHP
3. Jumlah view/fungsi: 1 view dan 1 fungsi
4. Jumlah prosedur: 1 prosedur
5. Jumlah trigger: 2 trigger

# Hasil dan Penjelasan

## 1. Tabel-tabel

### A. `lapkeu_user`

```sql
CREATE TABLE `lapkeu_user` (
`user_id` int NOT NULL AUTO_INCREMENT,
`username` varchar(25) NOT NULL,
`password` varchar(255) NOT NULL,
`role` enum('Admin','Accountant','Viewer') NOT NULL DEFAULT 'Viewer',
`created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY (`user_id`),
UNIQUE KEY `username` (`username`)
);
```

Tujuan: Autentikasi user dan role user

### B. `lapkeu_business`

```sql
CREATE TABLE `lapkeu_business` (
`business_id` int NOT NULL AUTO_INCREMENT,
`user_id` int NOT NULL,
`name` varchar(50) NOT NULL,
`industry` varchar(50) DEFAULT NULL,
`address` varchar(200) DEFAULT NULL,
`created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY (`business_id`),
KEY `user_id` (`user_id`),
FOREIGN KEY (`user_id`) REFERENCES `lapkeu_user` (`user_id`) ON DELETE CASCADE
);
```

Tujuan: Manajemen bisnis

### C. `lapkeu_accounts`

```sql
CREATE TABLE `lapkeu_accounts` (
`account_id` int NOT NULL AUTO_INCREMENT,
`business_id` int NOT NULL,
`account_name` varchar(50) NOT NULL,
`account_type` enum('Asset','Liability','Equity','Revenue','Expense') NOT NULL,
`created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY (`account_id`),
KEY `business_id` (`business_id`),
FOREIGN KEY (`business_id`) REFERENCES `lapkeu_business` (`business_id`) ON DELETE CASCADE
);
```

Tujuan: Nama-nama akun yang digunakan

### D. `lapkeu_transaction`

```sql
CREATE TABLE `lapkeu_transaction` (
`transaction_id` int NOT NULL AUTO_INCREMENT,
`business_id` int NOT NULL,
`date` date NOT NULL,
`description` varchar(200) NOT NULL,
`amount_used` decimal(15,2) NOT NULL DEFAULT '0.00',
`created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY (`transaction_id`),
KEY `business_id` (`business_id`),
FOREIGN KEY (`business_id`) REFERENCES `lapkeu_business` (`business_id`) ON DELETE CASCADE
);
```

Tujuan: Catatan transaksi utama

### E. `lapkeu_transaction_detail`

```sql
CREATE TABLE `lapkeu_transaction_detail` (
`detail_id` int NOT NULL AUTO_INCREMENT,
`transaction_id` int NOT NULL,
`account_id` int NOT NULL,
`amount` decimal(15,2) NOT NULL,
`type` enum('Credit','Debit') NOT NULL,
`created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY (`detail_id`),
KEY `transaction_id` (`transaction_id`),
KEY `account_id` (`account_id`),
FOREIGN KEY (`transaction_id`) REFERENCES `lapkeu_transaction` (`transaction_id`) ON DELETE CASCADE,
FOREIGN KEY (`account_id`) REFERENCES `lapkeu_accounts` (`account_id`) ON DELETE CASCADE
);
```

Tujuan: Catatan transaksi mendetail

### F. `lapkeu_financial`

```sql
CREATE TABLE `lapkeu_financial` (
`report_id` int NOT NULL AUTO_INCREMENT,
`business_id` int NOT NULL,
`start_date` date NOT NULL,
`end_date` date NOT NULL,
`is_finalized` tinyint(1) DEFAULT '0',
`finalized_by` int DEFAULT NULL,
`finalized_at` timestamp NULL DEFAULT NULL,
`created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY (`report_id`),
KEY `business_id` (`business_id`),
KEY `finalized_by` (`finalized_by`),
FOREIGN KEY (`business_id`) REFERENCES `lapkeu_business` (`business_id`) ON DELETE CASCADE,
FOREIGN KEY (`finalized_by`) REFERENCES `lapkeu_user` (`user_id`) ON DELETE SET NULL
);
```

Tujuan: Catatan laporan keuangan

### G. `lapkeu_contact`

```sql
CREATE TABLE `lapkeu_contact` (
`contact_id` int NOT NULL AUTO_INCREMENT,
`name` varchar(100) NOT NULL,
`email` varchar(100) NOT NULL,
`subject` varchar(200) NOT NULL,
`message` text NOT NULL,
`created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY (`contact_id`),
KEY `idx_created_at` (`created_at`)
);
```

Tujuan: Penyimpanan comment dari pengunjung web

## 2. Query complex

### A. Ringkasan transaksi

```sql
SELECT
    t.transaction_id,
    t.description,
    t.date,
    t.amount_used,
    f_validate_transaction_balance(t.transaction_id) as is_balanced_function,
    vts.is_balanced as is_balanced_view,
    vts.total_debit,
    vts.total_credit
-- Select kolom yang ditampilkan

FROM lapkeu_transaction t
LEFT JOIN v_transaction_summary vts ON t.transaction_id = vts.transaction_id
-- Tabel-tabel yang digunakan digabung dengan join

WHERE t.business_id = ?
-- (?) disini akan dimasukkan oleh PHP, ubah dengan (1/2/3) untuk testing

ORDER BY t.date DESC, t.transaction_id DESC
-- Menampilkan transaksi terbaru-terlama
```

### B. Lihat akun dan transaksinya

```sql
SELECT
    a.account_id,
    a.account_name,
    a.account_type,
--Select kolom yang ditampilkan

    COALESCE(SUM(CASE WHEN td.type = 'Debit' THEN td.amount ELSE 0 END), 0) as total_debit,
    COALESCE(SUM(CASE WHEN td.type = 'Credit' THEN td.amount ELSE 0 END), 0) as total_credit,
    COALESCE(SUM(CASE WHEN td.type = 'Debit' THEN td.amount
                      WHEN td.type = 'Credit' THEN -td.amount ELSE 0 END), 0) as balance
-- Coalesce digunakan untuk menghandle Null, jika hasinya null, maka diganti jadi 0
-- SUM digunakan untuk menjumlah semua nilai

FROM lapkeu_accounts a
LEFT JOIN lapkeu_transaction_detail td ON a.account_id = td.account_id
LEFT JOIN lapkeu_transaction t ON td.transaction_id = t.transaction_id
-- Tabel-tabel yang digunakan digabung dengan join

WHERE a.business_id = ? AND (t.date IS NULL OR t.date BETWEEN ? AND ?)
-- Terdapat 3 (?) disini, untuk testing bisa memasukkan nilai:
-- (?) pertama dengan (1/2/3)
-- (?) kedua dan ketiga dengan tanggal, formatnya 'YYYY-MM-DD', contoh: '2025-06-17'

GROUP BY a.account_id, a.account_name, a.account_type
-- Ini digunakan untuk tidak mengulang baris, terutama pada fungsi agregat seperti SUM()

ORDER BY a.account_type, a.account_name
-- Menampilkannya berdasarkan urutan tipe akun
```

### C. Detail transaksi dengan informasi akun

```sql
SELECT
    td.detail_id,
    td.account_id,
    td.amount,
    td.type,
    a.account_name,
    a.account_type
-- Select kolom yang ditampilkan

FROM lapkeu_transaction_detail td
JOIN lapkeu_accounts a ON td.account_id = a.account_id
-- Tabel-tabel yang digunakan digabung dengan join

WHERE td.transaction_id = ?
-- Ubah dengan id transaksi (int) untuk testing

ORDER BY td.detail_id
-- Diurutkan supaya rapih, biasanya Debit pertama
```

### D. Masih banyak lagi pada file-file PHP

## 3. View dan Fungsi

### A. View, untuk menampilkan semua data transaksi

```sql
CREATE VIEW `v_transaction_summary` AS
-- Inisiasi view

SELECT
    t.transaction_id,
    t.business_id,
    b.name AS business_name,
    t.date AS transaction_date,
    t.description,
    t.amount_used,
-- Select kolom yang digunakan

    COUNT(td.detail_id) AS detail_count,
    SUM(CASE WHEN td.type = 'Debit' THEN td.amount ELSE 0 END) AS total_debit,
    SUM(CASE WHEN td.type = 'Credit' THEN td.amount ELSE 0 END) AS total_credit,
    (ABS(SUM(CASE WHEN td.type = 'Debit' THEN td.amount ELSE 0 END) -
         SUM(CASE WHEN td.type = 'Credit' THEN td.amount ELSE 0 END)) < 0.01) AS is_balanced,
    t.created_at
-- COUNT untuk menghitung banyaknya kejadian
-- SUM untuk menjumlah data

FROM lapkeu_transaction t
JOIN lapkeu_business b ON t.business_id = b.business_id
LEFT JOIN lapkeu_transaction_detail td ON t.transaction_id = td.transaction_id
-- Tabel-tabel yang digunakan digabung dengan join

GROUP BY t.transaction_id, t.business_id, b.name, t.date, t.description, t.amount_used, t.created_at;
-- Ini digunakan untuk tidak mengulang baris, terutama pada fungsi agregat seperti SUM(), COUNT()
```

### B. Function, untuk memvalidasi transaksi

```sql
CREATE FUNCTION f_validate_transaction_balance(p_transaction_id INT)
-- Inisiasi fungsi dengan sebuah parameter bertipe data integer

RETURNS TINYINT(1)
DETERMINISTIC
READS SQL DATA
-- Returns tinyint akan menghasilkan nilai 0/1 (true/false)
-- Deterministic digunakan untuk caching jawaban dan memastikan hasil yang sama jika input sama
-- Reads sql data memastikan tidak ada write yang terjadi, dan hanya read

BEGIN
    DECLARE v_debit_total DECIMAL(15,2) DEFAULT 0;
    DECLARE v_credit_total DECIMAL(15,2) DEFAULT 0;
-- DECLARE menciptakan variabel lokal dengan tipe data desimal dengan 2 nilai dibelakang koma, default 0

    SELECT COALESCE(SUM(amount), 0) INTO v_debit_total
    FROM lapkeu_transaction_detail
    WHERE transaction_id = p_transaction_id AND type = 'Debit';
-- Memasukkan data ke variabel v_debit_total

    SELECT COALESCE(SUM(amount), 0) INTO v_credit_total
    FROM lapkeu_transaction_detail
    WHERE transaction_id = p_transaction_id AND type = 'Credit';
-- Memasukkan data ke variabel v_credit_total

    RETURN (ABS(v_debit_total - v_credit_total) < 0.01);
    -- ABS() membuat nilai menjadi absolut (+)
    -- 0.01 digunakan untuk membuat toleransi nilai, karena terkadang A - A = 0.0000001 yang mana bukan 0, padahal iya
END
```

## 4. Prosedur

### A. Prosedur membuat transaksi

```sql
CREATE PROCEDURE sp_create_transaction(
    IN p_business_id INT,
    IN p_date DATE,
    IN p_description VARCHAR(200),
    IN p_details JSON
)
-- Inisiasi prosedur dengan beberapa parameter

BEGIN
    DECLARE v_transaction_id INT;
    DECLARE v_total_debit DECIMAL(15,2) DEFAULT 0;
    DECLARE v_total_credit DECIMAL(15,2) DEFAULT 0;
    DECLARE v_detail_count INT DEFAULT 0;
    DECLARE v_i INT DEFAULT 0;
    DECLARE v_account_id INT;
    DECLARE v_amount DECIMAL(15,2);
    DECLARE v_type VARCHAR(10);
-- Mendeklarasikan variabel dengan tipe datanya masing-masing

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
-- Ini adalah kode untuk menghandle error, jika terjadi error maka kembalikan ke pengaturan awal

    START TRANSACTION;
-- Mulai, bagian setelah ini dapat dikembalikan (undo) ketika terjadi error

    SET v_detail_count = JSON_LENGTH(p_details);
-- Melihat berapa banyak data untuk di looping

    IF v_detail_count = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Transaction must have at least one detail';
    END IF;
-- Jika jumlah detail adalah 0, maka keluarkan error

    WHILE v_i < v_detail_count DO
        SET v_account_id = JSON_UNQUOTE(JSON_EXTRACT(p_details, CONCAT('$[', v_i, '].account_id')));
        SET v_amount = JSON_UNQUOTE(JSON_EXTRACT(p_details, CONCAT('$[', v_i, '].amount')));
        SET v_type = JSON_UNQUOTE(JSON_EXTRACT(p_details, CONCAT('$[', v_i, '].type')));
-- Iterasi ke tiap elemen di JSON
-- CONCAT membuat path JSON seperti '$[0].account_id', '$[1].account_id' untuk mengakses elemen array
-- JSON_EXTRACT mengambil nilai dari path JSON tersebut
-- JSON_UNQUOTE menghilangkan tanda kutip dari hasil JSON
-- Mengambil data dari JSON

        IF v_type = 'Debit' THEN
            SET v_total_debit = v_total_debit + v_amount;
        ELSEIF v_type = 'Credit' THEN
            SET v_total_credit = v_total_credit + v_amount;
        END IF;
-- Menghitung total debit dan kredit

        SET v_i = v_i + 1;
-- Untuk lanjut ke nilai berikutnya
    END WHILE;

    -- Validate balance
    IF ABS(v_total_debit - v_total_credit) > 0.01 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Transaction is not balanced - debits must equal credits';
    END IF;
-- Jika nilai tidak 0, maka error

    INSERT INTO lapkeu_transaction (business_id, date, description, amount_used)
    VALUES (p_business_id, p_date, p_description, v_total_debit);
-- Jika baik-baik saja, maka lanjutkan ke insert

    SET v_transaction_id = LAST_INSERT_ID();
-- Mengambil id transaksi setelah insert

    SET v_i = 0;
    WHILE v_i < v_detail_count DO
        SET v_account_id = JSON_UNQUOTE(JSON_EXTRACT(p_details, CONCAT('$[', v_i, '].account_id')));
        SET v_amount = JSON_UNQUOTE(JSON_EXTRACT(p_details, CONCAT('$[', v_i, '].amount')));
        SET v_type = JSON_UNQUOTE(JSON_EXTRACT(p_details, CONCAT('$[', v_i, '].type')));
-- Mengambil data dari JSON

        INSERT INTO lapkeu_transaction_detail (transaction_id, account_id, amount, type)
        VALUES (v_transaction_id, v_account_id, v_amount, v_type);
-- Memasukkan data ke detail transaksi

        SET v_i = v_i + 1;
-- Untuk lanjut ke nilai berikutnya
    END WHILE;

    COMMIT;
-- Commit perubahan yang terjadi
    SELECT v_transaction_id as transaction_id;
-- Me-return id transaksi
END
```

## 5. Trigger

### A. Trigger untuk mengupdate jumlah transaksi

```sql
CREATE TRIGGER `tr_update_transaction_amount`
-- Inisiasi trigger

AFTER INSERT ON `lapkeu_transaction_detail`
-- Trigger akan bekerja setelah insertion ke tabel `lapkeu_transaction_detail`

FOR EACH ROW
-- Trigger akan bekerja sekali setiap ada sebuah insertion yang dilakukan

BEGIN
    UPDATE lapkeu_transaction
-- Trigger akan mengupdate tabel ini
    SET amount_used = (
        SELECT COALESCE(SUM(amount), 0)
        FROM lapkeu_transaction_detail
        WHERE transaction_id = NEW.transaction_id
        AND type = 'Debit'
    )
    WHERE transaction_id = NEW.transaction_id;
-- Trigger akan memasukkan data ini
END
```

### B. Trigger untuk memvalidasi nilai transaksi

```sql
CREATE TRIGGER `tr_validate_transaction_balance`
-- Inisiasi trigger

AFTER INSERT ON `lapkeu_transaction_detail`
-- Trigger akan bekerja setelah insertion ke tabel `lapkeu_transaction_detail`

FOR EACH ROW
-- Trigger akan bekerja sekali setiap ada sebuah insertion yang dilakukan

BEGIN
    DECLARE v_debit_total DECIMAL(15,2) DEFAULT 0;
    DECLARE v_credit_total DECIMAL(15,2) DEFAULT 0;
-- Deklarasi variabel dan tipe datanya

    SELECT COALESCE(SUM(amount), 0) INTO v_debit_total
    FROM lapkeu_transaction_detail
    WHERE transaction_id = NEW.transaction_id AND type = 'Debit';
-- Mengisi cariabel v_debit_total berdasarkan nilai baru yang dimasukkan

    SELECT COALESCE(SUM(amount), 0) INTO v_credit_total
    FROM lapkeu_transaction_detail
    WHERE transaction_id = NEW.transaction_id AND type = 'Credit';
-- Mengisi cariabel v_credit_total berdasarkan nilai baru yang dimasukkan

    IF ABS(v_debit_total - v_credit_total) > 0.01 AND
       (SELECT COUNT(*) FROM lapkeu_transaction_detail WHERE transaction_id = NEW.transaction_id) > 1 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Transaction details are not balanced - debits must equal credits';
    END IF;
-- Hentikan insertion jika transaksi tidak seimbang dan sudah memiliki lebih dari 1 detail
END
```
