import os
import json
import requests
import pandas as pd
from datetime import datetime

# CONFIG
DATASET_RESOURCE = "https://data.austintexas.gov/resource/tyfh-5r8s.json"
METADATA_URL       = "https://data.austintexas.gov/api/views/tyfh-5r8s"
OUTDIR             = "raw_data"
SAMPLE_LIMIT       = 100000  # adjust or remove limit for full data

os.makedirs(OUTDIR, exist_ok=True)

def fetch_metadata():
    r = requests.get(METADATA_URL)
    r.raise_for_status()
    return r.json()

def save_dictionary(meta, outpath):
    rows = []
    for c in meta.get('columns', []):
        rows.append({
            'field_name': c.get('fieldName'),
            'label':      c.get('name'),
            'description':c.get('description') or "",
            'dataTypeName': c.get('dataTypeName'),
            'position':   c.get('position')
        })
    df = pd.DataFrame(rows).sort_values('position')
    df.to_csv(outpath, index=False)
    print("Saved data dictionary to:", outpath)
    return df

def download_data(limit=None, outpath=None):
    params = {}
    if limit:
        params['$limit'] = str(limit)
    print("Downloading trip data...")
    r = requests.get(DATASET_RESOURCE, params=params, stream=True)
    r.raise_for_status()
    data = r.json()
    df = pd.DataFrame(data)
    if outpath:
        df.to_csv(outpath, index=False)
        print("Saved raw sample to:", outpath)
    print("Rows downloaded:", len(df))
    return df

if __name__ == "__main__":
    meta = fetch_metadata()
    dict_file = os.path.join(OUTDIR, "metrobike_trips_data_dictionary.csv")
    save_dictionary(meta, dict_file)
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    sample_file = os.path.join(OUTDIR, f"metrobike_trips_sample_{timestamp}.csv")
    download_data(limit=SAMPLE_LIMIT, outpath=sample_file)
