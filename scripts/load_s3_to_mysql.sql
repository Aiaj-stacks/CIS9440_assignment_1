import pandas as pd
import boto3
from sqlalchemy import create_engine
from io import StringIO

# --- CONFIGURATION ---
# AWS Config
BUCKET_NAME = 'cis9440biketrip'
FILE_KEY = 'raw/metrobike/metrobike_trips_sample_data.csv'

# MySQL Config (Update these!)
DB_USER = 'root'  # Usually 'root'
DB_PASSWORD = 'Lolomg123'  # YOUR MySQL password
DB_HOST = 'localhost'  # Or your host IP
DB_PORT = '3306'
DB_NAME = 'cis9440_final' # The database name you created


def load_data():
    # 1. Read CSV from S3
    print("Downloading from S3...")
    s3 = boto3.client(
        's3',
        aws_access_key_id='AKIAYA366JSWUADUTCR5',  # e.g. AKIAIOSFODNN7EXAMPLE
        aws_secret_access_key='OH/FNe7GLcOIzdZwuSXMUn44fYDVsvDjCLR4vqLg',  # e.g. wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
        region_name='us-east-1'  # Change if your bucket is in a different region (e.g. us-east-2)
    )

    obj = s3.get_object(Bucket=BUCKET_NAME, Key=FILE_KEY)

    df = pd.read_csv(obj['Body'])

    # 2. Clean Data for MySQL
    # MySQL doesn't like NaN for integers, fill with 0 or handle appropriately
    df['year'] = df['year'].fillna(0).astype(int)
    df['trip_duration_minutes'] = df['trip_duration_minutes'].fillna(0).astype(int)

    # Ensure datetime is formatted correctly

    df['checkout_datetime'] = pd.to_datetime(df['checkout_datetime'])

    # 3. Connect to MySQL
    print("Connecting to MySQL...")
    connection_str = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(connection_str)

    # 4. Upload to Staging Table
    print("Uploading to Staging Table...")
    df.to_sql('staging_metrobike', con=engine, if_exists='append', index=False)

    print("Success! Data is in MySQL Staging table.")


if __name__ == "__main__":
    load_data()

