# Proyek Sistem Informasi Geografis (GIS)

## Deskripsi
Proyek ini merupakan implementasi Sistem Informasi Geografis (GIS) menggunakan arsitektur Serverless Micro-Frontend dengan JavaScript ES6 untuk frontend dan Golang untuk backend. Proyek dikembangkan menggunakan metodologi Agile Scrum dan teknik belajar Pomodoro.

## Pre-Requisite
- Web Service dengan menggunakan Javascript ES6 Frontend dan Golang Backend
- Sintaks HTML5
- Git dan Github Pages
- Arsitektur Serverless Micro-Frontend
- MongoDB dan PostGreSQL (Database)
- Agile Scrum (RPL)

## Software Pendukung
- VSCode
- MongoCompass
- Git Bash
- Domyikado (Timer Pomodoro)

## Parameter Penilaian
| Parameter | Bobot |
|-----------|-------|
| Develop Frontend Menggunakan GoCroot | 25% |
| Develop Backend Menggunakan JSCroot | 25% |
| Feedback Dari Product Owner Real | 10% |
| Task Jalan tanpa Bug dan sudah di deploy di main | 20% |
| Team Menggunakan WhatsAuth | 10% |
| Team Menggunakan API PetaPedia | 10% |

## Rencana Implementasi Intensif (2 Hari)

### Hari 1: Setup dan Pengembangan Core Features

#### Pagi (08:00 - 12:00)
##### Sesi 1-2: Setup Lingkungan & Repository (1 jam)
- Instalasi VSCode, Git Bash, MongoCompass
- Membuat repository GitHub dan mengaktifkan GitHub Pages
- Clone template starter yang sudah menyediakan struktur dasar

##### Sesi 3-4: Setup Database & Konfigurasi (1 jam)
- Setup MongoDB (local atau Atlas)
- Setup PostgreSQL dengan PostGIS (local atau managed service)
- Konfigurasi koneksi database di project

##### Sesi 5-8: Pengembangan Backend dengan JSCroot (2 jam)
- Implementasi API endpoints untuk data GIS
- Integrasi dengan MongoDB dan PostgreSQL
- Implementasi autentikasi dasar

#### Siang/Sore (13:00 - 19:00)
##### Sesi 9-12: Pengembangan Frontend dengan GoCroot (2 jam)
- Setup komponen UI dasar
- Implementasi tampilan peta dasar
- Konfigurasi interaksi dasar dengan peta

##### Sesi 13-16: Integrasi WhatsAuth (2 jam)
- Setup WhatsAuth SDK
- Implementasi login/register menggunakan WhatsAuth
- Pengujian flow autentikasi

##### Sesi 17-18: Integrasi API PetaPedia (1 jam)
- Registrasi dan mendapatkan API key (jika diperlukan)
- Implementasi fetch data dari PetaPedia
- Menampilkan data PetaPedia di peta

### Hari 2: Finalisasi dan Deployment

#### Pagi (08:00 - 12:00)
##### Sesi 1-4: Debugging dan Testing (2 jam)
- Testing semua fitur utama
- Perbaikan bug dan masalah yang ditemukan
- Optimasi performa dasar

##### Sesi 5-8: Implementasi Agile Sederhana (2 jam)
- Setup board Scrum sederhana di GitHub Projects
- Dokumentasi sprint singkat yang dilakukan
- Persiapan demo untuk Product Owner

#### Siang/Sore (13:00 - 19:00)
##### Sesi 9-10: Presentasi ke Product Owner (1 jam)
- Demo aplikasi ke Product Owner
- Mendapatkan feedback langsung

##### Sesi 11-14: Implementasi Feedback (2 jam)
- Revisi berdasarkan feedback yang diterima
- Perbaikan UI/UX jika diperlukan

##### Sesi 15-18: Deployment dan Dokumentasi (2 jam)
- Finalisasi kode untuk deployment
- Deploy ke GitHub Pages (branch main)
- Penulisan dokumentasi singkat
- Final testing untuk memastikan tidak ada bug

## Struktur Proyek
```
gis-project/
├── frontend/                 # GoCroot Frontend
│   ├── public/               # Static files
│   ├── src/                  # Source code
│   │   ├── components/       # UI Components
│   │   ├── pages/            # Page components
│   │   ├── services/         # API services
│   │   └── utils/            # Utility functions
│   └── package.json          # Dependencies
├── backend/                  # JSCroot Backend
│   ├── controllers/          # Request handlers
│   ├── models/               # Database models
│   ├── routes/               # API routes
│   └── main.go               # Entry point
├── database/                 # Database scripts
│   ├── mongo/                # MongoDB setup
│   └── postgresql/           # PostgreSQL/PostGIS setup
└── README.md                 # Documentation
```

## Implementasi Teknik Pomodoro
Teknik Pomodoro digunakan untuk meningkatkan fokus dan produktivitas:
- Setiap sesi Pomodoro: 25 menit fokus penuh
- Istirahat pendek: 5 menit
- Setelah 4 sesi Pomodoro, istirahat panjang: 15-30 menit

## Tips Implementasi Cepat
1. **Gunakan Starter Templates**:
   - Manfaatkan template yang tersedia untuk GoCroot dan JSCroot
   - Gunakan boilerplate untuk integrasi dengan WhatsAuth

2. **Prioritaskan Fitur Berdasarkan Bobot Penilaian**:
   - Fokus pada backend (25%) dan frontend (25%) terlebih dahulu
   - Pastikan deployment berjalan tanpa bug (20%)

3. **Minimalisasi Scope**:
   - Implementasikan fitur minimum yang memenuhi syarat penilaian
   - Gunakan library dan komponen yang sudah jadi

4. **Paralelkan Pekerjaan Jika Memungkinkan**:
   - Jika bekerja dalam tim, bagi tugas berdasarkan keahlian
   - Setup backend dan frontend dapat dikerjakan secara paralel

5. **Siapkan Contingency Plan**:
   - Identifikasi bagian yang mungkin bermasalah dan siapkan solusi alternatif
   - Siapkan mockup data jika integrasi API bermasalah

## Sumber Daya
- [Dokumentasi GoCroot](https://example.com/gocroot)
- [Dokumentasi JSCroot](https://example.com/jscroot)
- [API PetaPedia](https://example.com/petapedia)
- [WhatsAuth Documentation](https://example.com/whatsauth)