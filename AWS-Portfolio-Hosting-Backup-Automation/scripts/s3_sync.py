#!/usr/bin/env python3

import boto3
import os
import logging
import hashlib
import argparse
from pathlib import Path
from botocore.exceptions import ClientError
from boto3.exceptions import S3UploadFailedError

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def compute_checksum(file_path: Path) -> str:
    md5 = hashlib.md5()

    with file_path.open("rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5.update(chunk)

    return md5.hexdigest()

def build_local_manifest(source_dir: Path) -> dict:
    manifest = {}

    for file_path in source_dir.rglob("*"):
        if not file_path.is_file():
            continue

        size = file_path.stat().st_size
        if size == 0:
            continue

        rel_path = str(file_path.relative_to(source_dir))

        try:
            manifest[rel_path] = {
                "size": size,
                "checksum": compute_checksum(file_path)
            }
        except Exception as e:
            logger.warning(f"Skipping {file_path}: {e}")

    return manifest
    
def build_s3_manifest(s3, bucket: str, prefix: str = "") -> dict:
    manifest = {}

    paginator = s3.get_paginator("list_objects_v2")

    try:
        for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
            for obj in page.get("Contents", []):
                key = obj["Key"]

                if key.endswith("/"):
                    continue

                rel_path = key[len(prefix):] if key.startswith(prefix) else key

                manifest[rel_path] = {
                    "size": obj["Size"],
                    "checksum": obj["ETag"].strip('"')  
                }

    except ClientError as e:
        logger.error(f"S3 listing failed: {e}")
        raise

    return manifest

def build_sync_plan(local_manifest, s3_manifest):
    to_upload = []
    to_skip = []
    to_delete_local = []

    for path, meta in local_manifest.items():
        if path not in s3_manifest:
            to_upload.append(path)
        elif meta["checksum"] != s3_manifest[path]["checksum"]:
            to_upload.append(path)
        else:
            to_skip.append(path)

    for path in s3_manifest:
        if path not in local_manifest:
            to_delete_local.append(path)

    return to_upload, to_skip, to_delete_local

class SyncStats:
    def __init__(self):
        self.uploaded = 0
        self.skipped = 0
        self.deleted = 0

def upload_files(s3, bucket, base_path, files, stats):
    total = len(files)

    for i, path in enumerate(files, 1):
        local_path = os.path.join(base_path, path)

        try:
            s3.upload_file(local_path, bucket, path)
            stats.uploaded += 1
            logger.info(f"Uploaded ({i}/{total}): {path}")

        except (ClientError, S3UploadFailedError) as e:
            logger.error(f"Upload failed for {path}: {e}")

def delete_local_files(base_path, files, stats):
    for path in files:
        full_path = os.path.join(base_path, path)

        try:
            if os.path.exists(full_path):
                os.remove(full_path)
                stats.deleted += 1
                logger.info(f"Deleted: {path}")
        except Exception as e:
            logger.error(f"Delete failed for {path}: {e}")

def sync(local_manifest, s3_manifest, s3, bucket, base_path, delete=False, dry_run=False):
    stats = SyncStats()

    to_upload, to_skip, to_delete_local = build_sync_plan(
        local_manifest, s3_manifest
    )

    logger.info(f"To upload: {len(to_upload)}")
    logger.info(f"To skip: {len(to_skip)}")
    logger.info(f"To delete: {len(to_delete_local)}")

    if dry_run:
        logger.info("=== DRY RUN MODE ===")

        for path in to_upload:
            logger.info(f"[DRY RUN] would upload: {path}")
            stats.uploaded += 1

        for path in to_skip:
            stats.skipped += 1

        if delete:
            for path in to_delete_local:
                logger.info(f"[DRY RUN] would delete: {path}")
                stats.deleted += 1

    else:
        upload_files(s3, bucket, base_path, to_upload, stats)

        stats.skipped += len(to_skip)

        if delete:
            delete_local_files(base_path, to_delete_local, stats)

    logger.info("Sync complete")
    logger.info(
        f"Uploaded={stats.uploaded}, Skipped={stats.skipped}, Deleted={stats.deleted}"
    )

def parse_args():
    parser = argparse.ArgumentParser(description="S3 sync tool")

    parser.add_argument("--source", required=True)
    parser.add_argument("--bucket", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--delete", action="store_true")

    return parser.parse_args()

def main():
    args = parse_args()

    source_dir = Path(args.source)

    if not source_dir.exists():
        logger.critical("Source directory does not exist")
        return

    s3 = boto3.client("s3")

    try:
        local_manifest = build_local_manifest(source_dir)
        s3_manifest = build_s3_manifest(s3, args.bucket)

        sync(
            local_manifest,
            s3_manifest,
            s3,
            args.bucket,
            source_dir,
            delete=args.delete,
            dry_run=args.dry_run
        )

    except Exception as e:
        logger.critical(f"Fatal error: {e}")

if __name__ == "__main__":
    main()
