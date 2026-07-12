#!/usr/bin/env python3
import boto3

s3 = boto3.client("s3")

bucket = "my-abou-portfolio-site"

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
print(get_s3_objects_map(s3, bucket))





