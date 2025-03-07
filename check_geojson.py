from pymongo import MongoClient
import json
from bson import json_util

def check_and_fix_geojson():
    # Connect to MongoDB
    client = MongoClient('mongodb+srv://dghost2324:dwifatma2324@cluster0.6l9fb.mongodb.net/bandung_gis')
    db = client['bandung_gis']
    collection = db['roads']
    
    # Ambil satu dokumen untuk diperiksa
    sample_doc = collection.find_one({"properties.name": "Jalan Orange County Boulevard"})
    print("\nData di MongoDB:")
    print(json.dumps(json.loads(json_util.dumps(sample_doc)), indent=2))
    
    # Periksa format GeoJSON
    if sample_doc:
        # Periksa koordinat
        if 'geometry' in sample_doc and 'coordinates' in sample_doc['geometry']:
            coords = sample_doc['geometry']['coordinates']
            print("\nKoordinat valid:", len(coords) >= 2)
            print("Koordinat:", coords)
        
        # Periksa properties
        if 'properties' in sample_doc:
            props = sample_doc['properties']
            print("\nProperties yang ada:")
            for key, value in props.items():
                print(f"- {key}: {value}")
    
    # Buat format FeatureCollection yang benar
    feature_collection = {
        "type": "FeatureCollection",
        "features": [sample_doc] if sample_doc else []
    }
    
    print("\nFormat FeatureCollection yang benar:")
    print(json.dumps(feature_collection, indent=2))
    
    # Update collection dengan format yang benar
    try:
        # Hapus dokumen lama
        collection.delete_one({"properties.name": "Jalan Orange County Boulevard"})
        
        # Insert dengan format baru
        collection.insert_one(feature_collection)
        print("\nBerhasil update format di database")
    except Exception as e:
        print(f"\nError saat update database: {str(e)}")
    
    client.close()

if __name__ == "__main__":
    check_and_fix_geojson()
