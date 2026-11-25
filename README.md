# Hackathon Berantas Web Ilegal di Indo

Repo tim untuk **Hackathon Berantas Web Ilegal di Indo** (IMPHNEN Anti Judol).
Kompetisi mengumpulkan dan melaporkan link/domain web ilegal (judi online) ke panitia.
Satu entri yang dinilai **Valid** = **1 poin**. Tim dengan poin terbanyak menang.

Sumber aturan resmi: https://imphnen.dev/hackaton-anti-judol/info#aturan

## Tim

- Nama tim: **jowoborot**
- Anggota: meryzennn, deva
- Kode tim: dibagikan lewat chat privat (repo ini publik, kode tidak ditulis di sini)

## Jadwal penting (WIB)

| Tahap | Waktu |
|---|---|
| Pendaftaran | Rab 25 Nov 00.00 sampai Jum 4 Des 00.00 |
| Submit entri | Sab 5 Des 00.00 sampai Kam 10 Des 00.00 |
| Pengumuman | Sen 14 Des 00.00 (setelah semua entri selesai dinilai) |

Panitia bisa menutup pendaftaran lebih awal, jadi jangan mepet.

## Cara menang

- Poin hanya masuk setelah panitia menilai entri **Valid**.
- Entri yang masih **Menunggu penilaian** belum dihitung.
- Kalau poin sama, tim yang mencapai poin terakhirnya lebih dulu berada di atas.
  Yang dihitung jam submit, bukan jam dinilai.

## Entri yang sah

- Satu link atau domain.
- Berbentuk http atau https tanpa port, tanpa nama pengguna atau kata sandi,
  bukan alamat IP atau localhost, maksimal 300 karakter.
- Belum dipegang entri lain yang masih berjalan (dari tim mana pun).
- Disubmit lewat form resmi selagi submit dibuka.
- Dinilai Valid oleh panitia.

Status entri: **Menunggu penilaian** (poin belum masuk), **Valid** (+1),
**Duplikat** (0), **Ditolak** (0, alasan tampil di baris entri).

## Aturan duplikat

Dua tulisan dianggap link yang sama kalau bentuk catatnya sama. Yang dibuang saat dicatat:
http/https, `www.`, huruf besar di nama domain, query setelah `?`, bagian setelah `#`,
dan garis miring di akhir. Path tetap dihitung dan peka huruf besar-kecil.

Contoh:

| Ditulis | Dicatat |
|---|---|
| `https://www.TokoBudi.id/` | `tokobudi.id` |
| `tokobudi.id` | `tokobudi.id` |
| `http://TOKOBUDI.id/?utm=ig#promo` | `tokobudi.id` |
| `tokobudi.id/produk` | `tokobudi.id/produk` |
| `blog.tokobudi.id` | `blog.tokobudi.id` |

Yang lebih dulu tercatat dan masih berjalan (Menunggu penilaian atau Valid) yang memegang link itu.
Entri berikutnya dengan bentuk catat yang sama langsung berstatus Duplikat dan tidak dapat poin.
Entri yang Ditolak tidak memegang link, jadi link yang sama bisa disubmit lagi.

## Alur kerja tim

1. Temukan kandidat link web ilegal.
2. Normalisasi link pakai tool di repo ini, lalu cek apakah sudah pernah disubmit tim:

   ```bash
   python3 tools/normalize.py https://contoh-domain-ilegal.xyz
   python3 tools/normalize.py --check entries.md https://contoh-domain-ilegal.xyz
   ```

3. Kalau bersih (format sah dan belum ada di `entries.md`), submit lewat form resmi.
4. Catat di `entries.md`: link, bentuk catat, jam submit (WIB), status awal Menunggu penilaian.
5. Update status di `entries.md` setelah panitia menilai (Valid / Duplikat / Ditolak + alasan).

## Isi repo

- `README.md` — dokumen ini.
- `entries.md` — catatan semua entri yang disubmit tim beserta statusnya.
- `tools/normalize.py` — normalisasi link sesuai aturan resmi + cek duplikat terhadap `entries.md`.

## Catatan

- Satu akun hanya bisa masuk satu tim. Tim maksimal 4 orang.
- Kamu bisa keluar dari tim selama tim belum punya entri. Setelah ada entri, tim tidak bisa ditinggalkan.
- Semua anggota bisa submit; entri dan poin masuk ke tim, bukan ke orangnya.
- Hadiah untuk 3 tim teratas di papan akhir. Detailnya ada di halaman Hadiah resmi.
