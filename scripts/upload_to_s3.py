import os
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

# -----------------------------
# CONFIGURATION
# -----------------------------
# Set these as ENV variables (recommended):
# export AWS_ACCESS_KEY_ID="YOUR_KEY"
# export AWS_SECRET_ACCESS_KEY="YOUR_SECRET"
# export AWS_DEFAULT_REGION="us-east-1"
#
# Example bucket/prefix:
# export S3_BUCKET="my-metrobike-project"
# export S3_PREFIX="raw/metrobike/"

BUCKET_NAME = os.environ.get("S3_BUCKET")
PREFIX      = os.environ.get("S3_PREFIX", "raw/metrobike/")
DATA_DIR    = r"C:\Users\rijve\CIS9440_asignment_1\raw_data"   # Local folder holding the downloaded files

# Create client
s3 = boto3.client("s3")


# -----------------------------
# UPLOAD FUNCTION
# -----------------------------
def upload_file_to_s3(local_path, s3_bucket, s3_key):
    """
    Uploads a single file to S3 with clean error handling.
    """
    try:
        print(f"Uploading {local_path} → s3://{s3_bucket}/{s3_key}")

        s3.upload_file(local_path, s3_bucket, s3_key)

        print(f"✔ Successfully uploaded: s3://{s3_bucket}/{s3_key}")
        return True

    except FileNotFoundError:
        print(f"❌ ERROR: Local file not found: {local_path}")
        return False

    except NoCredentialsError:
        print("❌ ERROR: AWS credentials not found. Set environment variables.")
        return False

    except ClientError as e:
        print(f"❌ AWS Client Error: {e}")
        return False


# -----------------------------
# BULK UPLOAD FUNCTION
# -----------------------------
def upload_all_files():
    """
    Uploads all files inside raw_data/ to the configured S3 bucket.
    """
    if not BUCKET_NAME:
        print("❌ ERROR: S3_BUCKET environment variable is not set.")
        return

    if not os.path.isdir(DATA_DIR):
        print(f"❌ ERROR: Directory '{DATA_DIR}' does not exist.")
        return

    files = os.listdir(DATA_DIR)

    if not files:
        print("⚠ No files found in raw_data/. Nothing to upload.")
        return

    print(f"Found {len(files)} file(s) in {DATA_DIR}/ to upload.\n")

    for f in files:
        local_path = os.path.join(DATA_DIR, f)

        # Construct S3 key
        s3_key = f"{PREFIX}{f}"

        upload_file_to_s3(local_path, BUCKET_NAME, s3_key)


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    print("Starting S3 upload process...\n")
    upload_all_files()
    print("\nUpload process completed.\n")
