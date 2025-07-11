import argparse
import boto3
import fnmatch
from botocore.exceptions import NoCredentialsError, ClientError

def search_s3_bucket(bucket_name, pattern):
    """
    Searches for files in an S3 bucket matching a given pattern.

    Args:
        bucket_name (str): The name of the S3 bucket.
        pattern (str): The glob-style pattern to match against file names (e.g., "*.txt").
    """
    print(f"Searching for '{pattern}' in bucket '{bucket_name}'...")
    print("--------------------------------------------------")

    try:
        s3_client = boto3.client('s3')
        # Use a paginator to handle buckets with many objects
        paginator = s3_client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=bucket_name)

        found_files = False
        for page in pages:
            if "Contents" in page:
                for obj in page['Contents']:
                    key = obj['Key']
                    # Check if the key matches the glob pattern
                    if fnmatch.fnmatch(key, pattern):
                        print(f"- {key}")
                        found_files = True

        if not found_files:
            print("No files found matching the pattern.")

    except NoCredentialsError:
        print("Error: AWS credentials not found.")
        print("Please configure your credentials (e.g., via 'aws configure').")
        return
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchBucket':
            print(f"Error: The bucket '{bucket_name}' does not exist.")
        else:
            print(f"An unexpected error occurred: {e}")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return

    print("--------------------------------------------------")
    print("Search complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Search for files in an AWS S3 bucket using a glob pattern.",
        epilog="Example: python search_s3.py my-s3-bucket "reports/*.csv""
    )
    parser.add_argument("bucket_name", help="The name of the S3 bucket to search in.")
    parser.add_argument("pattern", help="The glob pattern to search for (e.g., "*.log").")
    
    args = parser.parse_args()
    
    search_s3_bucket(args.bucket_name, args.pattern)
