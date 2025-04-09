# Example script to simulate a user uploading a JSON file every
# 3 seconds to an S3 bucket.

import os
import random
import json
import time
from pathlib import Path
import boto3
from dotenv import load_dotenv

# The folder where source files live
DATA_FOLDER = "data-news-articles"
# How frequently to upload a file, in seconds
UPLOAD_INTERVAL = 3
# Total number of uploads to perform
NUM_UPLOADS = 4
# The name of the s3 bucket you're uploading to
S3_BUCKET_NAME = "ds4300-fontenot-project-bucket"


# Load the values from .env into dictionary
def load_env_variables():
    load_dotenv()
    return {
        "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
        "aws_region": os.getenv("AWS_REGION", "us-east-1"),
        "s3_bucket_name": os.getenv("S3_BUCKET_NAME"),
    }


# select a random json file from the input data set
def get_random_json_file(folder_path):
    json_files = list(Path(folder_path).glob("*.json"))
    if not json_files:
        raise FileNotFoundError(f"No JSON files found in {folder_path}")
    return random.choice(json_files)


# upload the selected file to the s3 bucket into uploads folder.
def upload_to_s3(s3_client, file_path, bucket_name):
    try:
        with open(file_path, "rb") as file:
            s3_client.upload_fileobj(
                file, bucket_name, f"uploads/{Path(file_path).name}"
            )
        print(f"Successfully uploaded {file_path.name} to S3")
    except Exception as e:
        print(f"Error uploading {file_path.name}: {str(e)}")


def main():
    # Load AWS credentials from .env
    aws_credentials = load_env_variables()

    # Validate required environment variables
    if not aws_credentials["aws_access_key_id"]:
        raise ValueError("No AWS Access key id set")
    if not aws_credentials["aws_secret_access_key"]:
        raise ValueError("No AWS Secret Access key set")
    if not aws_credentials["aws_region"]:
        raise ValueError("No AWS Region Set")
    if not aws_credentials["s3_bucket_name"]:
        raise ValueError("S3_BUCKET_NAME environment variable is not set")

    # Using the boto3 library, initialize S3 client
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_credentials["aws_access_key_id"],
        aws_secret_access_key=aws_credentials["aws_secret_access_key"],
        region_name=aws_credentials["aws_region"],
    )

    print(
        f"Starting S3 uploader. Will upload a random file every {UPLOAD_INTERVAL} seconds."
    )

    count_uploads = 0

    while count_uploads < NUM_UPLOADS:
        count_uploads += 1
        try:
            file_path = get_random_json_file(DATA_FOLDER)
            upload_to_s3(s3_client, file_path, aws_credentials["s3_bucket_name"])

            # Wait for the specified interval
            time.sleep(UPLOAD_INTERVAL)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            time.sleep(UPLOAD_INTERVAL)  # Wait before retrying


if __name__ == "__main__":
    main()
