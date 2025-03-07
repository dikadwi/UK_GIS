from pymongo import MongoClient
import json
from bson import ObjectId

def convert_all_roads():
    # Connect to MongoDB
    client = MongoClient('mongodb+srv://dghost2324:dwifatma2324@cluster0.6l9fb.mongodb.net/bandung_gis')
    db = client['bandung_gis']
    roads = db['roads']
    
    try:
        # Ambil semua data jalan
        all_roads = list(roads.find({}))
        print(f"Total dokumen yang akan dikonversi: {len(all_roads)}")
        
        # Format semua jalan sebagai features
        features = []
        for road in all_roads:
            if 'geometry' in road and 'properties' in road:
                # Hapus _id dari dokumen asli
                if '_id' in road:
                    del road['_id']
                
                # Pastikan tipe data adalah string
                if 'properties' in road:
                    for key, value in road['properties'].items():
                        if isinstance(value, ObjectId):
                            road['properties'][key] = str(value)
                        elif value is None:
                            road['properties'][key] = ""
                
                features.append(road)
        
        # Buat FeatureCollection
        feature_collection = {
            "type": "FeatureCollection",
            "features": features
        }
        
        # Buat collection baru untuk menyimpan hasil konversi
        roads_converted = db['roads_converted']
        roads_converted.drop()  # Hapus collection lama jika ada
        
        # Simpan FeatureCollection
        result = roads_converted.insert_one(feature_collection)
        
        # Buat index geospasial
        roads_converted.create_index([("features.geometry", "2dsphere")])
        
        print(f"\nBerhasil mengkonversi dan menyimpan {len(features)} jalan")
        print("Collection baru: roads_converted")
        
        # Tampilkan contoh data yang sudah dikonversi
        sample = roads_converted.find_one()
        if sample and 'features' in sample:
            print("\nContoh data yang sudah dikonversi:")
            print(f"Total features: {len(sample['features'])}")
            if len(sample['features']) > 0:
                print("\nContoh feature pertama:")
                print(json.dumps(sample['features'][0], default=str, indent=2))
        
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        client.close()

def verify_conversion():
    # Connect to MongoDB
    client = MongoClient('mongodb+srv://dghost2324:dwifatma2324@cluster0.6l9fb.mongodb.net/bandung_gis')
    db = client['bandung_gis']
    roads_converted = db['roads_converted']
    
    try:
        # Ambil dan periksa data
        data = roads_converted.find_one()
        if data:
            print("\nVerifikasi Data:")
            print(f"Tipe dokumen utama: {data.get('type', 'tidak ada')}")
            features = data.get('features', [])
            print(f"Jumlah features: {len(features)}")
            
            if features:
                # Periksa beberapa feature pertama
                for i, feature in enumerate(features[:3]):
                    print(f"\nFeature #{i+1}:")
                    print(f"- Type: {feature.get('type', 'tidak ada')}")
                    print(f"- Geometry type: {feature.get('geometry', {}).get('type', 'tidak ada')}")
                    print(f"- Properties: {json.dumps(feature.get('properties', {}), default=str)}")
    
    except Exception as e:
        print(f"Error saat verifikasi: {str(e)}")
    finally:
        client.close()

if __name__ == "__main__":
    print("Memulai konversi data...")
    convert_all_roads()
    print("\nMemulai verifikasi data...")
    verify_conversion()
