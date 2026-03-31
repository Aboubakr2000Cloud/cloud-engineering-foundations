# Week 10 — Learning Notes: AWS IAM & S3

## 📚 Overview

Week 10 introduced real AWS cloud infrastructure - setting up a secure AWS account, mastering S3 object storage, and building cloud-integrated automation tools. This was the transition from local development to cloud engineering.

---

## 1️⃣ AWS Account Setup & Security

### Key Concepts

**Root vs IAM User:**
- Root: Full account access (dangerous!)
- IAM: Limited permissions (safe for daily work)

**MFA (Multi-Factor Authentication):**
- Password + phone code = 2-factor security
- Virtual MFA (app) vs hardware token

### Code Example

```bash
# AWS CLI configuration
aws configure
# Stores credentials in ~/.aws/credentials
# Stores region in ~/.aws/config
```

---

## 2️⃣ IAM (Identity and Access Management)

### What I Learned

**IAM is AWS security foundation:**
- Controls WHO can access WHAT
- Free service (no charges)
- Applies to all AWS services

**IAM Components:**
- **Users:** Individual identities
- **Groups:** Collections of users
- **Roles:** Temporary credentials for services
- **Policies:** JSON permission documents

### Key Concepts

**Principle of Least Privilege:**
- Give ONLY permissions needed
- Start restrictive, expand if needed
- Never give full access unless necessary

**Policy Structure:**
```json
{
  "Effect": "Allow",
  "Action": ["s3:GetObject", "s3:PutObject"],
  "Resource": "arn:aws:s3:::my-bucket/*"
}
```

---

## 3️⃣ S3 (Simple Storage Service)

### What I Learned

**S3 is object storage, not filesystem:**
- No real folders (just key prefixes)
- Unlimited storage
- Pay per GB stored + requests
- 99.999999999% durability ("11 nines")

**Key concepts:**
- **Bucket:** Container (globally unique name)
- **Object:** File stored in bucket
- **Key:** Object's path/name (e.g., `folder/file.txt`)

### Code Examples

```python
import boto3

s3 = boto3.client('s3')

# Upload file
s3.upload_file('local.txt', 'my-bucket', 's3-key.txt')

# Download file
s3.download_file('my-bucket', 's3-key.txt', 'downloaded.txt')

# List buckets
response = s3.list_buckets()
for bucket in response['Buckets']:
    print(bucket['Name'])

# Delete object
s3.delete_object(Bucket='my-bucket', Key='file.txt')
```

---

## 4️⃣ Static Website Hosting on S3

### What I Learned

**S3 can host static websites:**
- HTML, CSS, JavaScript only
- No server-side code (PHP, Python, etc.)
- Fast, cheap, scalable

**Requirements:**
- Bucket policy for public read access
- Static website hosting enabled
- Index document specified

### Code Example

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::my-bucket/*"
  }]
}
```

---

## 5️⃣ boto3 for S3 Operations

### What I Learned

**boto3 provides programmatic AWS access:**
- Python SDK for all AWS services
- Two interfaces: client (low-level), resource (high-level)
- Uses AWS CLI credentials automatically

**Error handling with boto3:**
```python
from botocore.exceptions import ClientError

try:
    s3.upload_file('file.txt', 'bucket', 'key.txt')
except ClientError as e:
    code = e.response['Error']['Code']
    if code == 'NoSuchBucket':
        print("Bucket doesn't exist")
    elif code == 'AccessDenied':
        print("No permission")
```

---

## 6️⃣ Checksum Verification & Data Integrity

### What I Learned

**Checksums verify data integrity:**
- MD5 for local files
- SHA256 for backups (more secure)
- S3 ETag (often MD5, not always)

**Store checksums in S3 metadata:**
```python
s3.upload_file(
    'backup.tar.gz',
    'bucket',
    'backup.tar.gz',
    ExtraArgs={'Metadata': {'sha256': checksum}}
)

# Verify later
head = s3.head_object(Bucket='bucket', Key='backup.tar.gz')
stored_checksum = head['Metadata']['sha256']
```

**Why this matters:**
- Detect corrupted uploads
- Verify backups before deleting local copies
- Production backup systems REQUIRE this

---

## 7️⃣ S3 Pagination

### What I Learned

**S3 list operations return max 1000 objects:**
- Must paginate for larger buckets
- Use paginator (automatic pagination)

```python
# Wrong (breaks with >1000 objects)
response = s3.list_objects_v2(Bucket='bucket')
objects = response['Contents']  # Only first 1000!

# Correct (handles any size)
paginator = s3.get_paginator('list_objects_v2')
for page in paginator.paginate(Bucket='bucket'):
    for obj in page.get('Contents', []):
        print(obj['Key'])
```

**This is critical for production code!**

---

## 8️⃣ Sync Algorithms

### What I Learned

**Three-phase sync pattern:**
1. Build local manifest (files + checksums)
2. Build remote manifest (S3 objects + ETags)
3. Calculate diff (upload, skip, delete)

**Why not just upload everything?**
- Wastes bandwidth
- Costs money (S3 PUT requests)
- Takes longer
- Inefficient

**Checksum comparison:**
- Only upload if checksum differs
- Skip unchanged files
- This is how rsync works!

---

## 9️⃣ Date-Based Storage Organization

### What I Learned

**Production pattern for backups:**
```
backups/
  2025/
    02/
      10/
        backup_143022.tar.gz
      11/
        backup_084530.tar.gz
```

**Why organize by date?**
- Easy to find backups from specific day
- Supports S3 lifecycle policies
- Scales to millions of files
- Standard in production systems

```python
def build_s3_key(prefix, filename, dt):
    date_path = f"{dt.year}/{dt.month:02d}/{dt.day:02d}/"
    return f"{prefix}{date_path}{filename}"
```

---

## 🔟 AWS Error Handling Patterns

### What I Learned

**AWS errors across ALL services follow same pattern:**
```python
except ClientError as e:
    code = e.response['Error']['Code']
    message = e.response['Error']['Message']
```

**Common error codes:**
- `NoSuchBucket` - Bucket doesn't exist
- `NoSuchKey` - Object doesn't exist
- `AccessDenied` - No permission
- `InvalidBucketName` - Name rules violated

**Classify errors:**
- **Permanent:** Don't retry (AccessDenied, NoSuchBucket)
- **Transient:** Retry with backoff (network errors, throttling)

**This pattern applies to EC2, DynamoDB, Lambda, everything!**

---

## 📊 Week 10 Summary

### Skills Acquired

- [x] AWS account setup and security
- [x] IAM users, groups, policies
- [x] S3 bucket operations (create, upload, download, delete)
- [x] Static website hosting
- [x] boto3 programming
- [x] Checksum verification
- [x] S3 pagination
- [x] Sync algorithms
- [x] Date-based organization
- [x] AWS error handling

### Key Takeaways

1. **Security first:** MFA, IAM users, least privilege
2. **S3 isn't a filesystem:** Objects with keys, not files in folders
3. **Pagination is critical:** list_objects_v2 limit is 1000
4. **Verify uploads:** Compare checksums before trusting data
5. **Organize by date:** Scalable pattern for backups
6. **Error classification:** Permanent vs transient determines retry logic

### What I'm Most Proud Of

- Built production-grade deployment script with checksum comparison
- Integrated S3 into Week 8 backup with full verification
- Implemented sync algorithm from scratch
- Handled real AWS error scenarios
- Debugged complex integration issues

---

## 🚀 Real-World Applications

**This week's skills apply directly to:**
- Automated backups to cloud
- Static website hosting
- File synchronization systems
- Data pipelines
- Log archival
- Disaster recovery

**Pattern recognition:**
The error handling, pagination, and verification patterns learned this week apply to ALL AWS services I'll use going forward.

---

## 💡 Key Insights

**Integration is harder than building:**
Adding S3 to existing backup script was harder than writing new code. This is real-world engineering - most work is modifying existing systems.

**Debugging builds expertise:**
Spent more time debugging than coding. Each bug taught something valuable about AWS behavior, boto3 quirks, and edge cases.

**Production requires verification:**
Can't just upload and hope. Must verify checksums, handle errors, log everything. This is the difference between toy projects and production systems.

---

**Week 10 Complete!** This week established the foundation for all future AWS work. Understanding IAM, S3, and boto3 patterns will make EC2, VPC, Lambda, and other services much easier. Ready for Week 11! 
