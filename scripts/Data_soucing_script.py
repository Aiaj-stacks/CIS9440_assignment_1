{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "ffa3e2b6-1785-4756-afd8-22e78f658c0d",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Saved data dictionary to: raw_data\\metrobike_trips_data_dictionary.csv\n",
      "Downloading trip data...\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\rijve\\AppData\\Local\\Temp\\ipykernel_42348\\896415104.py:54: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).\n",
      "  timestamp = datetime.utcnow().strftime(\"%Y%m%dT%H%M%SZ\")\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Saved raw sample to: raw_data\\metrobike_trips_sample_20251118T200945Z.csv\n",
      "Rows downloaded: 100000\n"
     ]
    }
   ],
   "source": [
    "import os\n",
    "import json\n",
    "import requests\n",
    "import pandas as pd\n",
    "from datetime import datetime\n",
    "\n",
    "# CONFIG\n",
    "DATASET_RESOURCE = \"https://data.austintexas.gov/resource/tyfh-5r8s.json\"\n",
    "METADATA_URL       = \"https://data.austintexas.gov/api/views/tyfh-5r8s\"\n",
    "OUTDIR             = \"raw_data\"\n",
    "SAMPLE_LIMIT       = 100000  # adjust or remove limit for full data\n",
    "\n",
    "os.makedirs(OUTDIR, exist_ok=True)\n",
    "\n",
    "def fetch_metadata():\n",
    "    r = requests.get(METADATA_URL)\n",
    "    r.raise_for_status()\n",
    "    return r.json()\n",
    "\n",
    "def save_dictionary(meta, outpath):\n",
    "    rows = []\n",
    "    for c in meta.get('columns', []):\n",
    "        rows.append({\n",
    "            'field_name': c.get('fieldName'),\n",
    "            'label':      c.get('name'),\n",
    "            'description':c.get('description') or \"\",\n",
    "            'dataTypeName': c.get('dataTypeName'),\n",
    "            'position':   c.get('position')\n",
    "        })\n",
    "    df = pd.DataFrame(rows).sort_values('position')\n",
    "    df.to_csv(outpath, index=False)\n",
    "    print(\"Saved data dictionary to:\", outpath)\n",
    "    return df\n",
    "\n",
    "def download_data(limit=None, outpath=None):\n",
    "    params = {}\n",
    "    if limit:\n",
    "        params['$limit'] = str(limit)\n",
    "    print(\"Downloading trip data...\")\n",
    "    r = requests.get(DATASET_RESOURCE, params=params, stream=True)\n",
    "    r.raise_for_status()\n",
    "    data = r.json()\n",
    "    df = pd.DataFrame(data)\n",
    "    if outpath:\n",
    "        df.to_csv(outpath, index=False)\n",
    "        print(\"Saved raw sample to:\", outpath)\n",
    "    print(\"Rows downloaded:\", len(df))\n",
    "    return df\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    meta = fetch_metadata()\n",
    "    dict_file = os.path.join(OUTDIR, \"metrobike_trips_data_dictionary.csv\")\n",
    "    save_dictionary(meta, dict_file)\n",
    "    timestamp = datetime.utcnow().strftime(\"%Y%m%dT%H%M%SZ\")\n",
    "    sample_file = os.path.join(OUTDIR, f\"metrobike_trips_sample_{timestamp}.csv\")\n",
    "    download_data(limit=SAMPLE_LIMIT, outpath=sample_file)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "f275f115-24b2-4752-8023-1d118f790deb",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
