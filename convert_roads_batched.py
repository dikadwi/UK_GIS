from pymongo import MongoClient
import json
from bson import ObjectId
import math

def convert_roads_in_batches():
    # Connect to MongoDB
    client = MongoClient('mongodb+srv://dghost2324:dwifatma2324@cluster0.6l9fb.mongodb.net/bandung_gis')
    db = client['bandung_gis']
    roads = db['roads']
    roads_batched = db['roads_batched']
    
    try:
        # Hapus collection lama jika ada
        roads_batched.drop()
        
        # Hitung total dokumen
        total_docs = roads.count_documents({})
        # Batasi ukuran batch (sekitar 5000 dokumen per batch)
        batch_size = 5000
        total_batches = math.ceil(total_docs / batch_size)
        
        print(f"Total dokumen: {total_docs}")
        print(f"Jumlah batch: {total_batches}")
        
        # Proses per batch
        for batch_num in range(total_batches):
            start_idx = batch_num * batch_size
            
            print(f"\nMemproses batch {batch_num + 1}/{total_batches}")
            
            # Ambil dokumen untuk batch ini
            batch_docs = list(roads.find({}).skip(start_idx).limit(batch_size))
            
            # Format features untuk batch ini
            features = []
            for road in batch_docs:
                if 'geometry' in road and 'properties' in road:
                    # Hapus _id dari dokumen asli
                    if '_id' in road:
                        del road['_id']
                    
                    # Konversi semua nilai ke string jika perlu
                    if 'properties' in road:
                        for key, value in road['properties'].items():
                            if isinstance(value, ObjectId):
                                road['properties'][key] = str(value)
                            elif value is None:
                                road['properties'][key] = ""
                    
                    features.append(road)
            
            # Buat FeatureCollection untuk batch ini
            feature_collection = {
                "type": "FeatureCollection",
                "features": features,
                "batch_info": {
                    "batch_number": batch_num + 1,
                    "total_batches": total_batches,
                    "start_index": start_idx,
                    "size": len(features)
                }
            }
            
            # Simpan batch
            roads_batched.insert_one(feature_collection)
            print(f"Batch {batch_num + 1} berhasil disimpan dengan {len(features)} features")
        
        # Buat index geospasial
        roads_batched.create_index([("features.geometry", "2dsphere")])
        print("\nIndex geospasial berhasil dibuat")
        
        # Verifikasi hasil
        total_collections = roads_batched.count_documents({})
        print(f"\nTotal collections yang tersimpan: {total_collections}")
        
        # Tampilkan contoh dari batch pertama
        first_batch = roads_batched.find_one()
        if first_batch:
            print("\nContoh data dari batch pertama:")
            print(f"Batch info: {json.dumps(first_batch['batch_info'], indent=2)}")
            if first_batch['features']:
                print("\nContoh feature pertama:")
                print(json.dumps(first_batch['features'][0], default=str, indent=2))
    
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        client.close()

if __name__ == "__main__":
    print("Memulai konversi data dalam batch...")
    convert_roads_in_batches()
