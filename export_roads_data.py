from pymongo import MongoClient
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def export_roads_data():
    """Export road data from MongoDB to GeoJSON for web visualization"""
    try:
        # Connect to MongoDB
        client = MongoClient(os.getenv('MONGODB_URI'))
        db = client['bandung_gis']
        collection = db['roads_feature']
        
        # Initialize GeoJSON structure
        geojson = {
            "type": "FeatureCollection",
            "features": []
        }
        
        print("Mengambil data jalan dari MongoDB...")
        
        # Get all roads from all batches
        total_roads = 0
        for batch in collection.find():
            if 'features' in batch:
                for feature in batch['features']:
                    try:
                        if not isinstance(feature, dict):
                            continue
                            
                        # Only include essential properties to reduce file size
                        if 'properties' in feature:
                            properties = {
                                'name': feature['properties'].get('name', 'Unnamed Road'),
                                'highway': feature['properties'].get('highway', 'unclassified')
                            }
                            feature['properties'] = properties
                        
                        geojson['features'].append(feature)
                        total_roads += 1
                        
                        if total_roads % 1000 == 0:
                            print(f"Sudah memproses {total_roads} jalan...")
                            
                    except Exception as e:
                        continue
        
        # Save as JavaScript file
        output_file = 'roads_data.js'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('const roadsData = ')
            json.dump(geojson, f, ensure_ascii=False)
            f.write(';')
        
        print(f"\nBerhasil mengekspor {total_roads} jalan ke {output_file}")
        
    except Exception as e:
        print(f"Error saat mengekspor data: {str(e)}")
    finally:
        client.close()

if __name__ == "__main__":
    export_roads_data()
