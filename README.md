# Tokopedia Fake Detector 🔍

Aplikasi buat ngecek toko atau produk di Tokopedia itu asli atau palsu. Jadi kalau kamu ragu sama toko yang mau kamu beli, tinggal cek pakai tool ini aja!

## Apa Sih Ini? 

Tool ini bakal nganalisis toko/produk Tokopedia dari berbagai sisi:
- Pola review yang mencurigakan
- Rating yang aneh-aneh
- Pembeli yang sama berulang
- Waktu transaksi yang gak wajar
- Varian produk yang gak masuk akal
- Dan masih banyak lagi!

## Yang Kamu Butuhin

- Python 3.8 keatas
- Koneksi internet (buat ngambil data dari Tokopedia)

## Cara Install

1. Clone atau download dulu project ini
2. Masuk ke folder projectnya
3. Install requirement yang dibutuhin:

```bash
pip install -r requirements.txt
```

Udah, gitu aja! Gampang kan?

## Cara Pakai

Tinggal jalanin aja:

```bash
python main.py
```

Nanti bakal muncul menu interaktif. Kamu tinggal:
1. Pilih mau cek toko atau produk
2. Masukin URL/link tokopedia nya
3. Tunggu bentar, lagi dianalisis
4. Lihat hasilnya deh!

## Fitur-Fitur Keren

### 🎯 Pattern Analyzer
Ngecek pola-pola aneh di review. Misal reviewnya kok mirip-mirip semua, atau ada kata yang diulang-ulang terus.

### 👥 Buyer Analyzer  
Ngeliat pembeli yang sama beli berulang kali. Kalau ada yang beli 10x dalam sehari, mencurigakan gak tuh?

### ⭐ Rating Analyzer
Analisis distribusi rating. Kalau semua rating 5 bintang tanpa yang 4,3,2,1 sama sekali, hmm... 

### ⏰ Time Analyzer
Ngecek waktu transaksi. Masa iya ada yang beli jam 3 pagi terus-terusan?

### 📦 Variant Analyzer
Liat varian produk yang gak masuk akal. Misal jual baju tapi variannya ada "Merah 1GB" 😅

### 🔐 Trust Analyzer
Ngitung skor kepercayaan toko secara keseluruhan.

### 📊 Fake Scorer
Kasih skor final berapa persen kemungkinan toko/produk itu palsu.

## Cara Baca Hasilnya

Nanti bakal ada skor dari 0-100%:
- **0-30%** = Kemungkinan besar aman, silakan beli
- **31-60%** = Hati-hati, cek dulu review dan tokonya
- **61-80%** = Mencurigakan banget, mending cari toko lain
- **81-100%** = Jangan beli! Kemungkinan besar palsu

## Tips Pakai

1. **Jangan cuma liat skor akhir** - Baca juga detail analisisnya biar tau masalahnya dimana
2. **Cek beberapa produk** - Kalau mau mastiin toko, cek beberapa produk mereka
3. **Tetep pake logika** - Tool ini cuma bantu analisis, keputusan tetep di kamu

## Catatan Penting

- Tool ini cuma buat membantu analisis, bukan 100% akurat
- Tetep hati-hati belanja online
- Kalau ragu, mending gak usah beli
- Selalu cek official store kalau ada

## Ada Masalah?

Kalau nemu bug atau ada saran, langsung aja bikin issue di GitHub atau kontak developer.

## Disclaimer

Tool ini dibuat untuk edukasi dan membantu konsumen. Bukan untuk menjelekkan toko tertentu. Hasil analisis berdasarkan data yang tersedia dan algoritma yang ada. Keputusan pembelian tetap ada di tangan kamu!

---

**Happy Shopping! Belanja yang aman ya! 🛍️**
