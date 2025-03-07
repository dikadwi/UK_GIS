# Sistem Informasi Geografis (GIS)

Implementasi sistem informasi geografis modern menggunakan OpenLayers, MongoDB, dan WhatsApp API.

## Tech Stack

### Backend
- Node.js/Go untuk Cloud Functions
- MongoDB Atlas dengan Geospatial Features
- WhatsApp Business API
- JWT Authentication

### Frontend
- OpenLayers untuk visualisasi peta
- React.js framework
- Axios untuk HTTP client
- TailwindCSS untuk styling

### Database
- MongoDB dengan Geospatial Indexes
- GeoJSON data format
- Spatial Query Operators

## Fitur Utama

1. Visualisasi Data Geospasial
   - Tampilan peta interaktif dengan OpenLayers
   - Multiple base layers
   - Custom styling untuk fitur geospasial
   - Real-time updates

2. Manajemen Data
   - CRUD operasi untuk data geospasial
   - Bulk import/export
   - Validasi data GeoJSON
   - Versioning dan history

3. Analisis Spasial
   - Nearest neighbor search
   - Radius queries
   - Route calculation
   - Geofencing

4. Integrasi WhatsApp
   - Location sharing
   - Command-based interactions
   - Automated notifications
   - Custom responses

## Setup Development

### Prerequisites
1. Node.js dan npm
2. MongoDB Atlas account
3. WhatsApp Business API access
4. Git

### Langkah Instalasi
1. Clone repository
2. Setup MongoDB Atlas dengan geospatial indexes
3. Konfigurasi environment variables
4. Install dependencies
5. Deploy cloud functions
6. Run frontend development server

## Dokumentasi API

API documentation tersedia di:
- Swagger UI: `/api-docs`
- Postman Collection: `/postman`

## Kontribusi
Project ini open untuk kontribusi. Silakan buat issue atau pull request untuk perbaikan atau penambahan fitur.

## Tutorial: Visualisasi Data Jalan Kota Bandung

Tutorial ini akan menjelaskan langkah-langkah untuk mengambil data jalan dari OpenStreetMap, menyimpannya ke MongoDB, dan memvisualisasikannya menggunakan GitHub Pages.

### Daftar Isi
1. [Persiapan](#1-persiapan)
2. [Mengambil Data OSM](#2-mengambil-data-osm)
3. [Menyimpan ke MongoDB](#3-menyimpan-ke-mongodb)
4. [Membuat Visualisasi](#4-membuat-visualisasi)
5. [Deploy ke GitHub Pages](#5-deploy-ke-github-pages)

### 1. Persiapan

#### Instalasi Dependencies
```bash
pip install osmnx pymongo python-dotenv folium branca
```

#### Setup Environment Variables
Buat file `.env` dengan isi:
```
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
```

### 2. Mengambil Data OSM

#### Script: osm_to_mongodb.py
```python
import osmnx as ox
import json
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def get_road_data(place_name="Bandung, Indonesia"):
    print(f"Mengambil data jalan untuk {place_name}...")
    G = ox.graph_from_place(place_name, network_type="drive")
    edges = ox.graph_to_gdfs(G, nodes=False)
    geojson_roads = json.loads(edges.to_json())
    return geojson_roads
```

### 3. Menyimpan ke MongoDB

#### Menyimpan Data dalam Batch
```python
def save_to_mongodb(geojson_data):
    try:
        client = MongoClient(os.getenv('MONGODB_URI'))
        db = client['bandung_gis']
        collection = db['roads_feature']
        
        # Hapus data lama
        collection.delete_many({})
        
        # Proses per batch (5000 jalan per batch)
        batch_size = 5000
        features = geojson_data['features']
        total_features = len(features)
        total_batches = (total_features + batch_size - 1) // batch_size
        
        for batch_num in range(total_batches):
            start_idx = batch_num * batch_size
            end_idx = min(start_idx + batch_size, total_features)
            batch_features = features[start_idx:end_idx]
            
            feature_collection = {
                "type": "FeatureCollection",
                "features": batch_features,
                "batch_info": {
                    "batch_number": batch_num + 1,
                    "total_batches": total_batches,
                    "start_index": start_idx,
                    "size": len(batch_features)
                }
            }
            
            collection.insert_one(feature_collection)
            
        # Buat index geospasial
        collection.create_index([("features.geometry", "2dsphere")])
        
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        client.close()
```

### 3.5 Menguji Endpoint API Petapedia

Setelah data tersimpan di MongoDB, kita bisa menguji endpoint API dari Petapedia untuk mencari jalan terdekat dan informasi jalan.

#### Setup Token WhatsAuth
```python
import requests
import json

def get_whatsauth_token(phone_number, otp):
    """
    Mendapatkan token WhatsAuth
    """
    url = "https://petapedia.if.co.id/api/whatsauth/login"
    payload = {
        "phone": phone_number,
        "otp": otp
    }
    response = requests.post(url, json=payload)
    return response.json().get('token')

def test_nearest_road_api():
    """
    Menguji API pencarian jalan terdekat
    """
    # Koordinat untuk pengujian (contoh: Alun-alun Bandung)
    lat = -6.9218571
    lon = 107.6025123
    
    # Setup headers dengan token
    headers = {
        'Authorization': f'Bearer {YOUR_WHATSAUTH_TOKEN}'
    }
    
    # Endpoint untuk mencari jalan terdekat
    url = f"https://petapedia.if.co.id/api/nearestroad?lat={lat}&long={lon}"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print("Jalan terdekat:")
            print(json.dumps(data, indent=2))
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error: {str(e)}")

def search_road_by_name(road_name):
    """
    Mencari jalan berdasarkan nama
    """
    headers = {
        'Authorization': f'Bearer {YOUR_WHATSAUTH_TOKEN}'
    }
    
    url = f"https://petapedia.if.co.id/api/roads/search?name={road_name}"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"\nHasil pencarian untuk '{road_name}':")
            print(json.dumps(data, indent=2))
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error: {str(e)}")

# Contoh penggunaan
if __name__ == "__main__":
    # 1. Dapatkan token (hanya perlu dilakukan sekali)
    # token = get_whatsauth_token("YOUR_PHONE", "YOUR_OTP")
    
    # 2. Uji API jalan terdekat
    test_nearest_road_api()
    
    # 3. Uji pencarian jalan
    search_road_by_name("Asia Afrika")
```

#### Endpoint API yang Tersedia
1. **Login WhatsAuth**
   - URL: `https://petapedia.if.co.id/api/whatsauth/login`
   - Method: POST
   - Body: `{"phone": "string", "otp": "string"}`

2. **Jalan Terdekat**
   - URL: `https://petapedia.if.co.id/api/nearestroad`
   - Method: GET
   - Parameters: `lat` (latitude), `long` (longitude)
   - Headers: Authorization Bearer Token

3. **Pencarian Jalan**
   - URL: `https://petapedia.if.co.id/api/roads/search`
   - Method: GET
   - Parameters: `name` (nama jalan)
   - Headers: Authorization Bearer Token

4. **Semua Jalan**
   - URL: `https://petapedia.if.co.id/api/roads`
   - Method: GET
   - Headers: Authorization Bearer Token

#### Response Format
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "LineString",
        "coordinates": [[lon1, lat1], [lon2, lat2]]
      },
      "properties": {
        "name": "Nama Jalan",
        "highway": "Tipe Jalan"
      }
    }
  ]
}
```

#### Troubleshooting API
- Pastikan token WhatsAuth masih valid
- Periksa format koordinat (latitude: -90 to 90, longitude: -180 to 180)
- Gunakan try-catch untuk menangani error
- Periksa response status code dan pesan error

### 4. Membuat Visualisasi

#### Export Data untuk Web
Buat script `export_roads_data.py`:
```python
def export_roads_data():
    client = MongoClient(os.getenv('MONGODB_URI'))
    db = client['bandung_gis']
    collection = db['roads_feature']
    
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }
    
    for batch in collection.find():
        if 'features' in batch:
            for feature in batch['features']:
                geojson['features'].append(feature)
    
    with open('roads_data.js', 'w') as f:
        f.write('const roadsData = ')
        json.dump(geojson, f)
        f.write(';')
```

#### Membuat Halaman Web
1. Buat `index.html` untuk tampilan peta
2. Buat `map.js` untuk logika visualisasi
3. Gunakan Leaflet.js untuk rendering peta

### 5. Deploy ke GitHub Pages

#### Persiapan Repository
```bash
# Inisialisasi Git
git init

# Buat branch gh-pages
git checkout -b gh-pages

# Tambahkan remote repository
git remote add origin https://github.com/username/repo.git
```

#### Upload ke GitHub
```bash
# Add files
git add index.html map.js roads_data.js

# Commit
git commit -m "Initial commit: Bandung Roads Visualization"

# Push ke GitHub
git push -f origin gh-pages
```

#### Aktifkan GitHub Pages
1. Buka repository di GitHub
2. Pergi ke Settings > Pages
3. Pilih branch "gh-pages"
4. Simpan pengaturan

Peta akan dapat diakses di: `https://username.github.io/repo/`

## Fitur Visualisasi
- Warna berbeda untuk setiap tipe jalan
- Popup informasi saat mengklik jalan
- Legenda jenis jalan
- Zoom dan pan interaktif

## Troubleshooting
- Jika data terlalu besar, pastikan menggunakan batching
- Periksa koneksi MongoDB
- Pastikan format GeoJSON valid
- Periksa JavaScript Console untuk error

## Kontribusi
Silakan berkontribusi dengan membuat pull request atau melaporkan issues.