---
name: excel-design-system
description: Comprehensive design system and layout standards for AI agents creating executive-ready Excel reports, clinical dashboards, and boardroom analytics.
---

# Executive Excel Design System (Standar Desain Dashboard & Laporan AI Agent)

Sistem Desain ini adalah acuan baku bagi seluruh AI Agent dalam merancang, menstrukturkan, dan memproduksi file spreadsheet Microsoft Excel (.xlsx) untuk konsumsi tingkat Direksi, Manajemen Eksekutif, dan Pemangku Kepentingan Rumah Sakit.

---

## 1. Tata Letak Grid & Proporsi Kolom (Dual-Column Grid)

### A. Aturan Kolom & Margin
1. **Margin Buffer Kiri (Kolom A):**
   - Wajib selalu mengosongkan Kolom A dengan lebar `width = 3`.
   - Ini memberikan *visual breathing room* saat sheet dibuka.
2. **Konten Sisi Kiri (Tabel Eksekutif & Narasi: Kolom B s.d. G):**
   - Kolom B: Lebar `7` (Nomor Urut / Rank).
   - Kolom C: Lebar `30 - 32` (Nama Kategori, Unit Layanan, Faskes, atau Domisili).
   - Kolom D: Lebar `16` (Metrik 1 / Rajal).
   - Kolom E: Lebar `16` (Metrik 2 / Ranap).
   - Kolom F: Lebar `16 - 18` (Metrik 3 / Total Pasien).
   - Kolom G: Lebar `15` (Persentase / Keterangan).
3. **Kolom Spacer Tengah (Kolom H):**
   - Kolom H dikosongkan dengan lebar `width = 4` sebagai pemisah tegas antara tabel dan area grafik.
4. **Konten Sisi Kanan (Area Grafik / Charts: Kolom I s.d. N):**
   - Kolom I s.d. N: Lebar masing-masing `15 - 16`.
   - Total lebar 6 kolom ini menjadi kanvas yang ideal untuk chart berukuran `width = 14`.

---

## 2. Header Banner & Branding

1. **Struktur 3 Baris Header:**
   - **Baris 1:** Nama Institusi (`15pt Bold`, Teks Putih, Fill Navy Slate `#1A1A2E`, Tinggi Baris `28pt`).
   - **Baris 2:** Judul Laporan & Periode (`11pt Bold`, Teks Putih, Fill Brand Orange `#EF6C00`, Tinggi Baris `22pt`).
   - **Baris 3:** Sub-Judul / Topik Sheet (`10pt Bold`, Teks Putih, Fill Dark Slate `#37474F`, Tinggi Baris `20pt`).
2. **Merge Banner:**
   - Selalu merge dari Kolom B hingga Kolom N (atau batas akhir konten).
   - Hindari logo gambar yang mendistorsi aspect ratio sel jika tidak mutlak diperlukan.

---

## 3. Executive KPI Metric Cards

Diletakkan di **Baris 5 sampai 7** sebelum tabel pertama:
- Dibuat dalam 3 blok metrik utama (masing-masing selebar 2 kolom: `B:C`, `D:E`, `F:G`).
- **Header Kartu (Baris 5):** `9pt Bold White`, fill warna kategori (Navy `#1A1A2E`, Blue `#1565C0`, Green `#2E7D32`, atau Orange `#EF6C00`).
- **Nilai Metrik (Baris 6):** `18-20pt Bold`, warna teks sesuai tema kategori, fill `#FFFFFF`.
- **Keterangan / Subtitle (Baris 7):** `8.5pt Italic Muted (#555555)`, fill soft gray `#F5F5F5` dengan bottom border medium.

---

## 4. Penataan Tabel Eksekutif

1. **Section Header:**
   - Tinggi baris `24pt`, font `10.5pt Bold White`, fill warna tema section (Navy, Blue, Green, Teal, dll), left aligned dengan indent 1.
2. **Table Header:**
   - Tinggi baris `22pt`, font `9pt Bold White`, fill `#1A1A2E`, center aligned, thin gray border.
3. **Data Rows (Zebra Striping):**
   - Baris genap: `#FFFFFF`, baris ganjil: `#F8F9FA`.
   - Tinggi baris `20pt`, font `9pt Regular Black`.
   - Alignment: Nomor/Rank `Center`, Teks Deskriptif `Left`, Angka/Metrik `Right`.
4. **Total Row (Bottom Summary):**
   - Font `9pt Bold Black`, fill soft gray `#E9ECEF`.
   - Top Border: Thin Gray (`#888888`), Bottom Border: **Double Navy Line** (`#1A1A2E`).

---

## 5. Narrative Callout Box (Executive Insights)

Diletakkan tepat di bawah tabel terkait:
- Merge dari Kolom B s.d. G dengan tinggi 3 baris.
- Fill background: Soft Cream (`#FFF8E1`).
- Border: Left border **3pt Solid Orange (`#EF6C00`)**, top/bottom/right thin border (`#FFE082`).
- Font: `9pt Regular Slate (#263238)`, wrap text aktif, menyajikan analisis kontekstual singkat (tren, driver pertumbuhan, implikasi manajerial).

---

## 6. Aturan Penempatan & Sourcing Grafik (Anti-Collision Chart Rules)

1. **Dilarang Keras Menaruh Sel Liar (Stray Floating Numbers):**
   - Grafik harus membaca sumber data langsung dari baris tabel eksekutif yang terlihat di sisi kiri.
   - Contoh: `labels_ref = Reference(ws, min_col=3, min_row=r+1, max_row=r+n)`, `data_ref = Reference(ws, min_col=6, min_row=r+1, max_row=r+n)`.
2. **Koordinat Penempatan Grafik Sisi Kanan (Kolom I):**
   - Chart 1: Anchor `I5` (Height `7.5`, Width `14`).
   - Chart 2: Anchor `I16` (Height `7.5`, Width `14`).
   - Chart 3: Anchor `I27` (Height `10.0`, Width `14`).
   - Chart 4: Anchor `I42` (Height `8.5`, Width `14`).
   - Chart 5: Anchor `I56` (Height `9.5`, Width `14`).
3. **Data Labels:**
   - Pie Charts: `showPercent = True`, `showVal = False`.
   - Bar / Column Charts: `showVal = True`, `legend = None` (jika single series).

---

## 7. Format Angka Standar (Number Formatting)

1. **Volume Pasien / Jumlah:** Format `#,##0` (cth: `6,057`).
2. **Persentase / Share:** Format `0.0%` (cth: `87.2%`).
3. **Mata Uang / Finansial:** Format `Rp #,##0` atau `[$Rp-421] #,##0`.
4. **Rasio:** Format `0.0` (cth: `6.8`).

---

## 8. Data Mentah / Orisinal (Raw Datasets)

- Diletakkan di bagian paling bawah sheet (setelah seluruh ringkasan eksekutif selesai).
- Diberi Section Header gelap (`#37474F` atau `#1A1A2E`).
- Menyajikan seluruh kolom asli rekam medis / registrasi dengan format zebra striping rapi untuk keperluan audit internal rumah sakit.

---

## 9. Pengaturan View Worksheet

- Selalu aktifkan: `ws.views.sheetView[0].showGridLines = True`.
- Jangan biarkan gridlines hilang agar tabel tetap terlihat profesional saat diedit oleh user.
