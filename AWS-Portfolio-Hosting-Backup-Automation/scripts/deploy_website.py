#!/usr/bin/env python3

import boto3
import os
from pathlib import Path
import mimetypes
from botocore.exceptions import ClientError
from boto3.exceptions import S3UploadFailedError
import logging
import hashlib

s3 = boto3.client('s3')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
    )

logger = logging.getLogger(__name__)

def deploy_website(s3, file_path, bucket, s3_key, content_type, retries=3):
    for attempt in range(1, retries + 1):
        try:
            s3.upload_file(
                str(file_path),
                bucket,
                s3_key,
                ExtraArgs={
                    "ContentType": content_type
                }
            )

            logger.info(f"Uploaded {s3_key}")
            return True

        except (S3UploadFailedError, ClientError) as e:
            logger.warning(f"Attempt {attempt} failed for {s3_key}: {e}")

            if isinstance(e, ClientError):
                code = e.response["Error"]["Code"]
                if code in ["AccessDenied", "NoSuchBucket"]:
                    logger.error(f"Permanent error ({code}) → not retrying")
                    return False

            if attempt == retries:
                logger.error(f"Failed after {retries} attempts: {s3_key}")
                return False

            time.sleep(2 ** attempt) 

        except Exception as e:
            logger.error(f"Unexpected error for {s3_key}: {e}")
            return False

def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def get_s3_objects_map(s3, bucket):
    objects_map = {}

    paginator = s3.get_paginator('list_objects_v2')

    for page in paginator.paginate(Bucket=bucket):
        if 'Contents' in page:
            for obj in page['Contents']:
                key = obj['Key']
                etag = obj['ETag'].strip('"')
                objects_map[key] = etag

    return objects_map

def validate_bucket(s3, bucket):
    try:
        s3.head_bucket(Bucket=bucket)
        logger.info(f"Bucket '{bucket}' is accessible")
        return True

    except ClientError as e:
        code = e.response["Error"]["Code"]

        if code == "404":
            logger.error(f"Bucket '{bucket}' does not exist")
        elif code == "403":
            logger.error(f"Access denied to bucket '{bucket}'")
        else:
            logger.error(f"Error accessing bucket: {code}")

        return False

def main():
    local_dir = Path("/home/abou/AWS-Portfolio-Hosting-Backup-Automation/website")
    bucket = "my-abou-portfolio-site"

    stats = {
    "uploaded": 0,
    "updated": 0,
    "skipped": 0,
    "failed": 0
    }

    if not local_dir.is_dir():
        raise ValueError(f"Directory does not exist: {local_dir}")
    if not os.access(local_dir, os.R_OK):
        raise PermissionError(f"Directory not readable: {local_dir}")
    if not any(local_dir.rglob('*')):
        logger.warning("No files found to upload")  

    if not validate_bucket(s3, bucket):
        return 

    s3_objects = get_s3_objects_map(s3, bucket)

    for file_path in local_dir.rglob('*'):
        if file_path.is_file():

           content_type, _ = mimetypes.guess_type(file_path)
           if content_type is None:
              content_type = "application/octet-stream"

           s3_key = str(file_path.relative_to(local_dir))           

           if s3_key not in s3_objects:
              success = deploy_website(s3, file_path, bucket, s3_key, content_type, retries=3)
              if success:
                 stats["uploaded"] += 1
              else:
                 stats["failed"] += 1
           else:
               local_hash = calculate_md5(file_path)
               
               if local_hash != s3_objects[s3_key]:
                  success = deploy_website(s3, file_path, bucket, s3_key, content_type, retries=3)
                  if success:
                     stats["updated"] += 1
                  else:
                     stats["failed"] += 1
               else:
                  logger.info(f"Skipping {s3_key} (unchanged)")
                  stats["skipped"] += 1

    total = sum(stats.values())            

    logger.info("Deployment Summary:")
    logger.info("-" * 40)
    logger.info(f"Total: {total}")
    logger.info(f"Uploaded: {stats['uploaded']}")
    logger.info(f"Updated:  {stats['updated']}")
    logger.info(f"Skipped:  {stats['skipped']}")
    logger.info(f"Failed:   {stats['failed']}")
    logger.info("-" * 40)

if __name__ == "__main__":
    main()
