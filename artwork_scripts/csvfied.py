import pandas as pd
import json
from tqdm import tqdm

def flatten_json(json_data, prefix=""):
    flattened_data = []
    for artwork in tqdm(json_data, desc="Deflattening JSON", unit=""):
        flattened_artwork = artwork.copy()
        details = flattened_artwork.pop("Details", {})
        for key, value in details.items():
            new_key = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                flattened_data.extend(flatten_json([{new_key: value}], new_key))
            else:
                flattened_artwork[new_key] = value
        flattened_data.append(flattened_artwork)
    return flattened_data

def convert_json_to_csv(json_file_path, csv_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)

    flattened_data = flatten_json(json_data)
    total_rows = len(flattened_data)

    df = pd.json_normalize(flattened_data)

    with tqdm(total=total_rows, desc="Converting to CSV", unit="row") as pbar:
        df.to_csv(csv_file_path, index=False, chunksize=1000, line_terminator='\n', encoding='utf-8')
        pbar.update(len(df))

if __name__ == "__main__":
    json_file_path = "../artworks.json"
    csv_file_path = "../artworks.csv"
    convert_json_to_csv(json_file_path, csv_file_path)
    print(" ")
