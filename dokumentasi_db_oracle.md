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

Oracle Database 21c Enterprise Edition
Oracle SQL Developer

## Target yang sudah dipenuhi:

1. Jumlah tabel: 7 tabel
2. Jumlah query complex: 5+ pada PHP
3. Jumlah view/fungsi: 1 view dan 1 fungsi
4. Jumlah prosedur: 1 prosedur
5. Jumlah trigger: 9 trigger (2 business logic + 7 auto-increment)

# Hasil dan Penjelasan

## Hasil-hasil ini adalah yang dieksport dari Oracle sqldeveloper, C##AFIF0 adalah nama usernya

## 1. Tabel-tabel

### A. `LAPKEU_USER`

```sql
CREATE TABLE "C##AFIF0"."LAPKEU_USER" (
    "USER_ID" NUMBER(10,0),
    "USERNAME" VARCHAR2(25 BYTE) NOT NULL,
    "PASSWORD" VARCHAR2(255 BYTE) NOT NULL,
    "ROLE" VARCHAR2(15 BYTE) DEFAULT 'Viewer' NOT NULL,
    "CREATED_AT" TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY ("USER_ID"),
    UNIQUE ("USERNAME"),
    CONSTRAINT "CHK_USER_ROLE" CHECK (ROLE IN ('Admin', 'Accountant', 'Viewer'))
);
```

Tujuan: Autentikasi user dan role user

### B. `LAPKEU_BUSINESS`

```sql
CREATE TABLE "C##AFIF0"."LAPKEU_BUSINESS" (
    "BUSINESS_ID" NUMBER(10,0),
    "USER_ID" NUMBER(10,0) NOT NULL,
    "NAME" VARCHAR2(50 BYTE) NOT NULL,
    "INDUSTRY" VARCHAR2(50 BYTE),
    "ADDRESS" VARCHAR2(200 BYTE),
    "CREATED_AT" TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY ("BUSINESS_ID"),
    FOREIGN KEY ("USER_ID") REFERENCES "LAPKEU_USER" ("USER_ID") ON DELETE CASCADE
);
```

Tujuan: Manajemen bisnis

### C. `LAPKEU_ACCOUNTS`

```sql
CREATE TABLE "C##AFIF0"."LAPKEU_ACCOUNTS" (
    "ACCOUNT_ID" NUMBER(10,0),
    "BUSINESS_ID" NUMBER(10,0) NOT NULL,
    "ACCOUNT_NAME" VARCHAR2(50 BYTE) NOT NULL,
    "ACCOUNT_TYPE" VARCHAR2(15 BYTE) NOT NULL,
    "CREATED_AT" TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY ("ACCOUNT_ID"),
    FOREIGN KEY ("BUSINESS_ID") REFERENCES "LAPKEU_BUSINESS" ("BUSINESS_ID") ON DELETE CASCADE,
    CONSTRAINT "CHK_ACCOUNT_TYPE" CHECK (ACCOUNT_TYPE IN ('Asset', 'Liability', 'Equity', 'Revenue', 'Expense'))
);
```

Tujuan: Nama-nama akun yang digunakan

### D. `LAPKEU_TRANSACTION`

```sql
CREATE TABLE "C##AFIF0"."LAPKEU_TRANSACTION" (
    "TRANSACTION_ID" NUMBER(10,0),
    "BUSINESS_ID" NUMBER(10,0) NOT NULL,
    "TRANSACTION_DATE" DATE NOT NULL,
    "DESCRIPTION" VARCHAR2(200 BYTE) NOT NULL,
    "AMOUNT_USED" NUMBER(15,2) DEFAULT 0.00 NOT NULL,
    "CREATED_AT" TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY ("TRANSACTION_ID"),
    FOREIGN KEY ("BUSINESS_ID") REFERENCES "LAPKEU_BUSINESS" ("BUSINESS_ID") ON DELETE CASCADE
);
```

Tujuan: Catatan transaksi utama

### E. `LAPKEU_TRANSACTION_DETAIL`

```sql
CREATE TABLE "C##AFIF0"."LAPKEU_TRANSACTION_DETAIL" (
    "DETAIL_ID" NUMBER(10,0),
    "TRANSACTION_ID" NUMBER(10,0) NOT NULL,
    "ACCOUNT_ID" NUMBER(10,0) NOT NULL,
    "AMOUNT" NUMBER(15,2) NOT NULL,
    "TYPE" VARCHAR2(10 BYTE) NOT NULL,
    "CREATED_AT" TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY ("DETAIL_ID"),
    FOREIGN KEY ("TRANSACTION_ID") REFERENCES "LAPKEU_TRANSACTION" ("TRANSACTION_ID") ON DELETE CASCADE,
    FOREIGN KEY ("ACCOUNT_ID") REFERENCES "LAPKEU_ACCOUNTS" ("ACCOUNT_ID") ON DELETE CASCADE,
    CONSTRAINT "CHK_TRANSACTION_TYPE" CHECK (TYPE IN ('Credit', 'Debit'))
);
```

Tujuan: Catatan transaksi mendetail

### F. `LAPKEU_FINANCIAL`

```sql
CREATE TABLE "C##AFIF0"."LAPKEU_FINANCIAL" (
    "REPORT_ID" NUMBER(10,0),
    "BUSINESS_ID" NUMBER(10,0) NOT NULL,
    "START_DATE" DATE NOT NULL,
    "END_DATE" DATE NOT NULL,
    "IS_FINALIZED" NUMBER(1,0) DEFAULT 0,
    "FINALIZED_BY" NUMBER(10,0),
    "FINALIZED_AT" TIMESTAMP(6),
    "CREATED_AT" TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY ("REPORT_ID"),
    FOREIGN KEY ("BUSINESS_ID") REFERENCES "LAPKEU_BUSINESS" ("BUSINESS_ID") ON DELETE CASCADE,
    FOREIGN KEY ("FINALIZED_BY") REFERENCES "LAPKEU_USER" ("USER_ID") ON DELETE SET NULL,
    CONSTRAINT "CHK_IS_FINALIZED" CHECK (IS_FINALIZED IN (0, 1))
);
```

Tujuan: Catatan laporan keuangan

### G. `LAPKEU_CONTACT`

```sql
CREATE TABLE "C##AFIF0"."LAPKEU_CONTACT" (
    "CONTACT_ID" NUMBER(10,0),
    "NAME" VARCHAR2(100 BYTE) NOT NULL,
    "EMAIL" VARCHAR2(100 BYTE) NOT NULL,
    "SUBJECT" VARCHAR2(200 BYTE) NOT NULL,
    "MESSAGE" CLOB NOT NULL,
    "CREATED_AT" TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY ("CONTACT_ID")
);

CREATE INDEX "IDX_CONTACT_CREATED_AT" ON "LAPKEU_CONTACT" ("CREATED_AT");
```

Tujuan: Penyimpanan comment dari pengunjung web

## 2. Query complex

### A. Ringkasan transaksi

```sql
SELECT
    t.TRANSACTION_ID,
    t.DESCRIPTION,
    t.TRANSACTION_DATE,
    t.AMOUNT_USED,
    F_VALIDATE_TRANSACTION_BALANCE(t.TRANSACTION_ID) as IS_BALANCED_FUNCTION,
    vts.IS_BALANCED as IS_BALANCED_VIEW,
    vts.TOTAL_DEBIT,
    vts.TOTAL_CREDIT
-- Select kolom yang ditampilkan

FROM LAPKEU_TRANSACTION t
LEFT JOIN V_TRANSACTION_SUMMARY vts ON t.TRANSACTION_ID = vts.TRANSACTION_ID
-- Tabel-tabel yang digunakan digabung dengan join

WHERE t.BUSINESS_ID = :business_id
-- (:business_id) disini akan dimasukkan oleh PHP, ubah dengan (1/2/3) untuk testing

ORDER BY t.TRANSACTION_DATE DESC, t.TRANSACTION_ID DESC;
-- Menampilkan transaksi terbaru-terlama
```

### B. Lihat akun dan transaksinya

```sql
SELECT
    a.ACCOUNT_ID,
    a.ACCOUNT_NAME,
    a.ACCOUNT_TYPE,
-- Select kolom yang ditampilkan

    NVL(SUM(CASE WHEN td.TYPE = 'Debit' THEN td.AMOUNT ELSE 0 END), 0) as TOTAL_DEBIT,
    NVL(SUM(CASE WHEN td.TYPE = 'Credit' THEN td.AMOUNT ELSE 0 END), 0) as TOTAL_CREDIT,
    NVL(SUM(CASE WHEN td.TYPE = 'Debit' THEN td.AMOUNT
                 WHEN td.TYPE = 'Credit' THEN -td.AMOUNT ELSE 0 END), 0) as BALANCE
-- NVL digunakan untuk menghandle Null, jika hasilnya null, maka diganti jadi 0
-- SUM digunakan untuk menjumlah semua nilai

FROM LAPKEU_ACCOUNTS a
LEFT JOIN LAPKEU_TRANSACTION_DETAIL td ON a.ACCOUNT_ID = td.ACCOUNT_ID
LEFT JOIN LAPKEU_TRANSACTION t ON td.TRANSACTION_ID = t.TRANSACTION_ID
-- Tabel-tabel yang digunakan digabung dengan join

WHERE a.BUSINESS_ID = :business_id AND (t.TRANSACTION_DATE IS NULL OR t.TRANSACTION_DATE BETWEEN :start_date AND :end_date)
-- Terdapat 3 parameter disini, untuk testing bisa memasukkan nilai:
-- :business_id dengan (1/2/3)
-- :start_date dan :end_date dengan tanggal, formatnya DATE '2025-06-17'

GROUP BY a.ACCOUNT_ID, a.ACCOUNT_NAME, a.ACCOUNT_TYPE
-- Ini digunakan untuk tidak mengulang baris, terutama pada fungsi agregat seperti SUM()

ORDER BY a.ACCOUNT_TYPE, a.ACCOUNT_NAME;
-- Menampilkannya berdasarkan urutan tipe akun
```

### C. Detail transaksi dengan informasi akun

```sql
SELECT
    td.DETAIL_ID,
    td.ACCOUNT_ID,
    td.AMOUNT,
    td.TYPE,
    a.ACCOUNT_NAME,
    a.ACCOUNT_TYPE
-- Select kolom yang ditampilkan

FROM LAPKEU_TRANSACTION_DETAIL td
JOIN LAPKEU_ACCOUNTS a ON td.ACCOUNT_ID = a.ACCOUNT_ID
-- Tabel-tabel yang digunakan digabung dengan join

WHERE td.TRANSACTION_ID = :transaction_id
-- Ubah dengan id transaksi (NUMBER) untuk testing

ORDER BY td.DETAIL_ID;
-- Diurutkan supaya rapih, biasanya Debit pertama
```

### D. Masih banyak lagi pada file-file PHP

## 3. View dan Fungsi

### A. View, untuk menampilkan semua data transaksi

```sql
CREATE VIEW V_TRANSACTION_SUMMARY AS
-- Inisiasi view

SELECT
    t.TRANSACTION_ID,
    t.BUSINESS_ID,
    b.NAME AS BUSINESS_NAME,
    t.TRANSACTION_DATE,
    t.DESCRIPTION,
    t.AMOUNT_USED,
-- Select kolom yang digunakan

    COUNT(td.DETAIL_ID) AS DETAIL_COUNT,
    NVL(SUM(CASE WHEN td.TYPE = 'Debit' THEN td.AMOUNT ELSE 0 END), 0) AS TOTAL_DEBIT,
    NVL(SUM(CASE WHEN td.TYPE = 'Credit' THEN td.AMOUNT ELSE 0 END), 0) AS TOTAL_CREDIT,
    CASE
        WHEN ABS(NVL(SUM(CASE WHEN td.TYPE = 'Debit' THEN td.AMOUNT ELSE 0 END), 0) -
                 NVL(SUM(CASE WHEN td.TYPE = 'Credit' THEN td.AMOUNT ELSE 0 END), 0)) < 0.01
        THEN 1
        ELSE 0
    END AS IS_BALANCED,
    t.CREATED_AT
-- COUNT untuk menghitung banyaknya kejadian
-- SUM untuk menjumlah data
-- CASE untuk conditional logic

FROM LAPKEU_TRANSACTION t
JOIN LAPKEU_BUSINESS b ON t.BUSINESS_ID = b.BUSINESS_ID
LEFT JOIN LAPKEU_TRANSACTION_DETAIL td ON t.TRANSACTION_ID = td.TRANSACTION_ID
-- Tabel-tabel yang digunakan digabung dengan join

GROUP BY t.TRANSACTION_ID, t.BUSINESS_ID, b.NAME, t.TRANSACTION_DATE, t.DESCRIPTION, t.AMOUNT_USED, t.CREATED_AT;
-- Ini digunakan untuk tidak mengulang baris, terutama pada fungsi agregat seperti SUM(), COUNT()
```

### B. Function, untuk memvalidasi transaksi

```sql
CREATE OR REPLACE FUNCTION F_VALIDATE_TRANSACTION_BALANCE(p_transaction_id IN NUMBER)
-- Inisiasi fungsi dengan sebuah parameter bertipe data NUMBER

RETURN NUMBER
DETERMINISTIC
-- Returns NUMBER akan menghasilkan nilai 0/1 (false/true)
-- DETERMINISTIC digunakan untuk caching jawaban dan memastikan hasil yang sama jika input sama

IS
    v_debit_total NUMBER(15,2) := 0;
    v_credit_total NUMBER(15,2) := 0;
-- Menciptakan variabel lokal dengan tipe data NUMBER dengan 2 nilai dibelakang koma, default 0

BEGIN
    SELECT NVL(SUM(AMOUNT), 0) INTO v_debit_total
    FROM LAPKEU_TRANSACTION_DETAIL
    WHERE TRANSACTION_ID = p_transaction_id AND TYPE = 'Debit';
-- Memasukkan data ke variabel v_debit_total

    SELECT NVL(SUM(AMOUNT), 0) INTO v_credit_total
    FROM LAPKEU_TRANSACTION_DETAIL
    WHERE TRANSACTION_ID = p_transaction_id AND TYPE = 'Credit';
-- Memasukkan data ke variabel v_credit_total

    IF ABS(v_debit_total - v_credit_total) < 0.01 THEN
        RETURN 1;
    ELSE
        RETURN 0;
    END IF;
    -- ABS() membuat nilai menjadi absolut (+)
    -- 0.01 digunakan untuk membuat toleransi nilai, karena terkadang A - A = 0.0000001 yang mana bukan 0, padahal iya

EXCEPTION
    WHEN OTHERS THEN
        RETURN 0;
END;
```

## 4. Prosedur

### A. Prosedur membuat transaksi

```sql
CREATE OR REPLACE PROCEDURE SP_CREATE_TRANSACTION(
    p_business_id IN NUMBER,
    p_date IN DATE,
    p_description IN VARCHAR2,
    p_details IN CLOB
)
-- Inisiasi prosedur dengan beberapa parameter
-- CLOB digunakan untuk data JSON yang panjang

IS
    v_transaction_id NUMBER;
    v_total_debit NUMBER(15,2) := 0;
    v_total_credit NUMBER(15,2) := 0;
    v_detail_count NUMBER := 0;
    v_account_id NUMBER;
    v_amount NUMBER(15,2);
    v_type VARCHAR2(10);
    -- Variables untuk parsing JSON manual
    v_json_start NUMBER;
    v_json_end NUMBER;
    v_detail_json VARCHAR2(4000);
    v_field_start NUMBER;
    v_field_end NUMBER;
-- Mendeklarasikan variabel dengan tipe datanya masing-masing

BEGIN
    SAVEPOINT sp_transaction_start;
-- Savepoint untuk rollback jika terjadi error

    -- Menghitung jumlah objek JSON menggunakan REGEXP_COUNT
    v_detail_count := REGEXP_COUNT(p_details, '\{[^}]*\}');
-- Melihat berapa banyak data untuk di looping

    IF v_detail_count = 0 THEN
        RAISE_APPLICATION_ERROR(-20002, 'Transaction must have at least one detail');
    END IF;
-- Jika jumlah detail adalah 0, maka keluarkan error

    -- Parsing JSON manual untuk kompatibilitas dengan semua versi Oracle
    v_json_start := 1;
    FOR i IN 1..v_detail_count LOOP
        -- Mencari awal dan akhir setiap objek JSON
        v_json_start := INSTR(p_details, '{', v_json_start);
        v_json_end := INSTR(p_details, '}', v_json_start);

        IF v_json_start = 0 OR v_json_end = 0 THEN
            RAISE_APPLICATION_ERROR(-20003, 'Invalid JSON format at detail ' || i);
        END IF;

        v_detail_json := SUBSTR(p_details, v_json_start, v_json_end - v_json_start + 1);

        -- Ekstrak account_id dari JSON
        v_field_start := INSTR(v_detail_json, '"account_id"');
        IF v_field_start > 0 THEN
            v_field_start := INSTR(v_detail_json, ':', v_field_start) + 1;
            v_field_end := LEAST(
                NVL(INSTR(v_detail_json, ',', v_field_start), LENGTH(v_detail_json)),
                NVL(INSTR(v_detail_json, '}', v_field_start), LENGTH(v_detail_json))
            );
            v_account_id := TO_NUMBER(TRIM(REPLACE(REPLACE(SUBSTR(v_detail_json, v_field_start, v_field_end - v_field_start), '"', ''), ' ', '')));
        ELSE
            RAISE_APPLICATION_ERROR(-20004, 'Missing account_id in detail ' || i);
        END IF;

        -- Ekstrak amount dari JSON
        v_field_start := INSTR(v_detail_json, '"amount"');
        IF v_field_start > 0 THEN
            v_field_start := INSTR(v_detail_json, ':', v_field_start) + 1;
            v_field_end := LEAST(
                NVL(INSTR(v_detail_json, ',', v_field_start), LENGTH(v_detail_json)),
                NVL(INSTR(v_detail_json, '}', v_field_start), LENGTH(v_detail_json))
            );
            v_amount := TO_NUMBER(TRIM(REPLACE(REPLACE(SUBSTR(v_detail_json, v_field_start, v_field_end - v_field_start), '"', ''), ' ', '')));
        ELSE
            RAISE_APPLICATION_ERROR(-20005, 'Missing amount in detail ' || i);
        END IF;

        -- Ekstrak type dari JSON
        v_field_start := INSTR(v_detail_json, '"type"');
        IF v_field_start > 0 THEN
            v_field_start := INSTR(v_detail_json, ':', v_field_start) + 1;
            v_field_start := INSTR(v_detail_json, '"', v_field_start) + 1;
            v_field_end := INSTR(v_detail_json, '"', v_field_start);
            v_type := SUBSTR(v_detail_json, v_field_start, v_field_end - v_field_start);
        ELSE
            RAISE_APPLICATION_ERROR(-20006, 'Missing type in detail ' || i);
        END IF;
-- Parsing manual JSON karena Oracle versi lama tidak mendukung JSON native

        -- Validasi type value

-- Menghitung total debit dan kredit

        v_json_start := v_json_end + 1;
-- Untuk lanjut ke nilai berikutnya
    END LOOP;

    -- Validasi balance
    IF ABS(v_total_debit - v_total_credit) > 0.01 THEN
        RAISE_APPLICATION_ERROR(-20008, 'Transaction is not balanced - debits must equal credits');
    END IF;
-- Jika nilai tidak seimbang, maka error

    INSERT INTO LAPKEU_TRANSACTION (BUSINESS_ID, TRANSACTION_DATE, DESCRIPTION, AMOUNT_USED)
    VALUES (p_business_id, p_date, p_description, v_total_debit)
    RETURNING TRANSACTION_ID INTO v_transaction_id;
-- Jika baik-baik saja, maka lanjutkan ke insert dan ambil ID yang baru dibuat

    -- Insert transaction details (parse ulang untuk insertion)
    v_json_start := 1;
    FOR i IN 1..v_detail_count LOOP
        -- Parsing ulang JSON untuk setiap detail
        v_json_start := INSTR(p_details, '{', v_json_start);
        v_json_end := INSTR(p_details, '}', v_json_start);

        IF v_json_start = 0 OR v_json_end = 0 THEN
            RAISE_APPLICATION_ERROR(-20003, 'Invalid JSON format at detail ' || i);
        END IF;

        v_detail_json := SUBSTR(p_details, v_json_start, v_json_end - v_json_start + 1);

        -- Ekstrak account_id dari JSON
        v_field_start := INSTR(v_detail_json, '"account_id"');
        IF v_field_start > 0 THEN
            v_field_start := INSTR(v_detail_json, ':', v_field_start) + 1;
            v_field_end := LEAST(
                NVL(INSTR(v_detail_json, ',', v_field_start), LENGTH(v_detail_json)),
                NVL(INSTR(v_detail_json, '}', v_field_start), LENGTH(v_detail_json))
            );
            v_account_id := TO_NUMBER(TRIM(REPLACE(REPLACE(SUBSTR(v_detail_json, v_field_start, v_field_end - v_field_start), '"', ''), ' ', '')));
        ELSE
            RAISE_APPLICATION_ERROR(-20004, 'Missing account_id in detail ' || i);
        END IF;

        -- Ekstrak amount dari JSON
        v_field_start := INSTR(v_detail_json, '"amount"');
        IF v_field_start > 0 THEN
            v_field_start := INSTR(v_detail_json, ':', v_field_start) + 1;
            v_field_end := LEAST(
                NVL(INSTR(v_detail_json, ',', v_field_start), LENGTH(v_detail_json)),
                NVL(INSTR(v_detail_json, '}', v_field_start), LENGTH(v_detail_json))
            );
            v_amount := TO_NUMBER(TRIM(REPLACE(REPLACE(SUBSTR(v_detail_json, v_field_start, v_field_end - v_field_start), '"', ''), ' ', '')));
        ELSE
            RAISE_APPLICATION_ERROR(-20005, 'Missing amount in detail ' || i);
        END IF;

        -- Ekstrak type dari JSON
        v_field_start := INSTR(v_detail_json, '"type"');
        IF v_field_start > 0 THEN
            v_field_start := INSTR(v_detail_json, ':', v_field_start) + 1;
            v_field_start := INSTR(v_detail_json, '"', v_field_start) + 1;
            v_field_end := INSTR(v_detail_json, '"', v_field_start);
            v_type := SUBSTR(v_detail_json, v_field_start, v_field_end - v_field_start);
        ELSE
            RAISE_APPLICATION_ERROR(-20006, 'Missing type in detail ' || i);
        END IF;

        -- Validasi type value
        IF v_type NOT IN ('Debit', 'Credit') THEN
            RAISE_APPLICATION_ERROR(-20007, 'Invalid type "' || v_type || '" in detail ' || i || '. Must be Debit or Credit');
        END IF;

        INSERT INTO LAPKEU_TRANSACTION_DETAIL (TRANSACTION_ID, ACCOUNT_ID, AMOUNT, TYPE)
        VALUES (v_transaction_id, v_account_id, v_amount, v_type);
-- Memasukkan data ke detail transaksi

        v_json_start := v_json_end + 1;
-- Untuk lanjut ke nilai berikutnya
    END LOOP;

    COMMIT;
-- Commit perubahan yang terjadi

    DBMS_OUTPUT.PUT_LINE('Transaction created with ID: ' || v_transaction_id);
-- Output ID transaksi yang dibuat

EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK TO sp_transaction_start;
        RAISE;
-- Rollback jika terjadi error
END;
```

## 5. Trigger

### A. Trigger untuk mengupdate jumlah transaksi (Compound Trigger)

```sql
CREATE OR REPLACE EDITIONABLE TRIGGER "C##AFIF0"."TR_UPDATE_TRANSACTION_AMOUNT"
-- Inisiasi trigger compound untuk update amount transaksi
FOR INSERT ON LAPKEU_TRANSACTION_DETAIL
-- Trigger akan bekerja pada insertion ke tabel LAPKEU_TRANSACTION_DETAIL
COMPOUND TRIGGER

    TYPE t_update_transaction_ids IS TABLE OF NUMBER;
    v_update_transaction_ids t_update_transaction_ids := t_update_transaction_ids();
-- Deklarasi collection untuk menyimpan transaction_id yang perlu diupdate

    AFTER EACH ROW IS
-- Section yang berjalan setelah setiap baris diinsert
    BEGIN
        v_update_transaction_ids.EXTEND;
        v_update_transaction_ids(v_update_transaction_ids.COUNT) := :NEW.TRANSACTION_ID;
-- Mengumpulkan transaction_id dari setiap baris yang diinsert
    END AFTER EACH ROW;

    AFTER STATEMENT IS
-- Section yang berjalan setelah SEMUA insertion selesai
    BEGIN
        FOR i IN 1..v_update_transaction_ids.COUNT LOOP
            UPDATE LAPKEU_TRANSACTION
            SET AMOUNT_USED = (
                SELECT NVL(SUM(AMOUNT), 0)
                FROM LAPKEU_TRANSACTION_DETAIL
                WHERE TRANSACTION_ID = v_update_transaction_ids(i)
                AND TYPE = 'Debit'
            )
            WHERE TRANSACTION_ID = v_update_transaction_ids(i);
-- Update amount_used berdasarkan total debit untuk setiap transaksi
        END LOOP;

        v_update_transaction_ids.DELETE;
-- Bersihkan collection setelah selesai
    END AFTER STATEMENT;

END TR_UPDATE_TRANSACTION_AMOUNT;
```

### B. Trigger untuk memvalidasi nilai transaksi (Compound Trigger)

```sql
CREATE OR REPLACE EDITIONABLE TRIGGER "C##AFIF0"."TR_VALIDATE_TRANSACTION_BALANCE"
-- Inisiasi trigger compound untuk validasi keseimbangan transaksi
FOR INSERT ON LAPKEU_TRANSACTION_DETAIL
-- Trigger akan bekerja pada insertion ke  tabel LAPKEU_TRANSACTION_DETAIL
COMPOUND TRIGGER

    TYPE t_validate_transaction_ids IS TABLE OF NUMBER;
    v_validate_transaction_ids t_validate_transaction_ids := t_validate_transaction_ids();
-- Deklarasi collection untuk menyimpan transaction_id yang perlu divalidasi

    AFTER EACH ROW IS
-- Section yang berjalan setelah setiap baris diinsert
    BEGIN
        v_validate_transaction_ids.EXTEND;
        v_validate_transaction_ids(v_validate_transaction_ids.COUNT) := :NEW.TRANSACTION_ID;
-- Mengumpulkan transaction_id dari setiap baris yang diinsert
    END AFTER EACH ROW;

    AFTER STATEMENT IS
-- Section yang berjalan setelah SEMUA insertion selesai
        v_debit_total NUMBER(15,2);
        v_credit_total NUMBER(15,2);
        v_detail_count NUMBER;
-- Deklarasi variabel untuk perhitungan validasi
    BEGIN
        FOR i IN 1..v_validate_transaction_ids.COUNT LOOP
            SELECT NVL(SUM(CASE WHEN TYPE = 'Debit' THEN AMOUNT ELSE 0 END), 0),
                   NVL(SUM(CASE WHEN TYPE = 'Credit' THEN AMOUNT ELSE 0 END), 0),
                   COUNT(*)
            INTO v_debit_total, v_credit_total, v_detail_count
            FROM LAPKEU_TRANSACTION_DETAIL
            WHERE TRANSACTION_ID = v_validate_transaction_ids(i);
-- Menghitung total debit, kredit, dan jumlah detail untuk setiap transaksi

            IF v_detail_count > 1 AND ABS(v_debit_total - v_credit_total) > 0.01 THEN
                RAISE_APPLICATION_ERROR(-20001, 'Transaction ' || v_validate_transaction_ids(i) ||
                    ' is not balanced - debits (' || v_debit_total || ') must equal credits (' || v_credit_total || ')');
            END IF;
-- Jika transaksi tidak seimbang dan memiliki lebih dari 1 detail, keluarkan error
        END LOOP;

        v_validate_transaction_ids.DELETE;
-- Bersihkan collection setelah selesai
    END AFTER STATEMENT;

END TR_VALIDATE_TRANSACTION_BALANCE;
```

**Catatan Penting**: Kedua trigger di atas menggunakan **Compound Trigger** untuk menghindari ORA-04091 (mutating table error). Trigger akan bekerja setelah SEMUA insert dalam satu statement selesai, bukan per baris.

### C. Trigger Auto-increment (7 trigger)

Oracle tidak memiliki AUTO_INCREMENT seperti MySQL, sehingga perlu menggunakan trigger dan sequence:

```sql
-- Trigger untuk LAPKEU_USER
CREATE OR REPLACE EDITIONABLE TRIGGER "C##AFIF0"."TRG_LAPKEU_USER_ID"
    BEFORE INSERT ON LAPKEU_USER
-- Trigger berjalan sebelum insertion ke tabel LAPKEU_USER
    FOR EACH ROW
-- Trigger berjalan untuk setiap baris yang diinsert
BEGIN
    IF :NEW.USER_ID IS NULL THEN
        :NEW.USER_ID := seq_lapkeu_user.NEXTVAL;
    END IF;
-- Jika USER_ID kosong, isi dengan nilai berikutnya dari sequence
END;

-- Trigger untuk LAPKEU_BUSINESS
CREATE OR REPLACE EDITIONABLE TRIGGER "C##AFIF0"."TRG_LAPKEU_BUSINESS_ID"
    BEFORE INSERT ON LAPKEU_BUSINESS
    FOR EACH ROW
BEGIN
    IF :NEW.BUSINESS_ID IS NULL THEN
        :NEW.BUSINESS_ID := seq_lapkeu_business.NEXTVAL;
    END IF;
END;

-- Trigger untuk LAPKEU_ACCOUNTS
CREATE OR REPLACE EDITIONABLE TRIGGER "C##AFIF0"."TRG_LAPKEU_ACCOUNTS_ID"
    BEFORE INSERT ON LAPKEU_ACCOUNTS
    FOR EACH ROW
BEGIN
    IF :NEW.ACCOUNT_ID IS NULL THEN
        :NEW.ACCOUNT_ID := seq_lapkeu_accounts.NEXTVAL;
    END IF;
END;

-- Trigger untuk LAPKEU_TRANSACTION
CREATE OR REPLACE EDITIONABLE TRIGGER "C##AFIF0"."TRG_LAPKEU_TRANSACTION_ID"
    BEFORE INSERT ON LAPKEU_TRANSACTION
    FOR EACH ROW
BEGIN
    IF :NEW.TRANSACTION_ID IS NULL THEN
        :NEW.TRANSACTION_ID := seq_lapkeu_transaction.NEXTVAL;
    END IF;
END;

-- Trigger untuk LAPKEU_TRANSACTION_DETAIL
CREATE OR REPLACE EDITIONABLE TRIGGER "C##AFIF0"."TRG_LAPKEU_TRANSACTION_DETAIL_ID"
    BEFORE INSERT ON LAPKEU_TRANSACTION_DETAIL
    FOR EACH ROW
BEGIN
    IF :NEW.DETAIL_ID IS NULL THEN
        :NEW.DETAIL_ID := seq_lapkeu_transaction_detail.NEXTVAL;
    END IF;
END;

-- Trigger untuk LAPKEU_FINANCIAL
CREATE OR REPLACE EDITIONABLE TRIGGER "C##AFIF0"."TRG_LAPKEU_FINANCIAL_ID"
    BEFORE INSERT ON LAPKEU_FINANCIAL
    FOR EACH ROW
BEGIN
    IF :NEW.REPORT_ID IS NULL THEN
        :NEW.REPORT_ID := seq_lapkeu_financial.NEXTVAL;
    END IF;
END;

-- Trigger untuk LAPKEU_CONTACT
CREATE OR REPLACE EDITIONABLE TRIGGER "C##AFIF0"."TRG_LAPKEU_CONTACT_ID"
    BEFORE INSERT ON LAPKEU_CONTACT
    FOR EACH ROW
BEGIN
    IF :NEW.CONTACT_ID IS NULL THEN
        :NEW.CONTACT_ID := seq_lapkeu_contact.NEXTVAL;
    END IF;
END;
```

**Catatan**: Trigger auto-increment ini menggantikan fungsi AUTO_INCREMENT MySQL dan bukan merupakan business logic trigger.

## 6. Sequences (Oracle Specific)

Oracle menggunakan sequences untuk auto-increment:

```sql
-- Contoh sequence untuk user_id
CREATE SEQUENCE seq_lapkeu_user
START WITH 1
INCREMENT BY 1
NOCACHE
NOCYCLE;

-- Sequences serupa dibuat untuk semua tabel auto-increment
```

## Perbedaan Utama MySQL vs Oracle:

1. Tipe Data: `INT` → `NUMBER`, `VARCHAR()` → `VARCHAR2()`, `TEXT` → `CLOB`
2. Auto-increment: `AUTO_INCREMENT` → `SEQUENCE + TRIGGER`
3. NULL Handling: `COALESCE()` → `NVL()`
4. JSON: MySQL native JSON → Oracle manual parsing (CLOB)
5. Error Handling: `SIGNAL SQLSTATE` → `RAISE_APPLICATION_ERROR`
6. Bind Variables: `?` → `:parameter_name`

## Kesimpulan

Database Oracle ini memiliki fungsionalitas yang identik dengan versi MySQL, dengan penyesuaian syntax dan implementasi yang sesuai dengan karakteristik Oracle Database.
