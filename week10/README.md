# Week 10 — AWS IAM & S3

## Overview

This week focused on AWS fundamentals - setting up a secure AWS account, understanding Identity and Access Management (IAM), and mastering S3 object storage. The projects demonstrate real-world cloud automation: portfolio website hosting, backup system integration, and S3 management utilities.

**Key Learning Areas:**
- AWS account setup and security (MFA, billing alerts)
- IAM users, groups, roles, and policies
- S3 bucket management and operations
- Static website hosting on AWS
- boto3 for programmatic AWS access
- Cloud backup strategies with verification
- Automated deployment pipelines

---

## Projects

### 1. Static Portfolio Website on S3

Professional portfolio website hosted on AWS S3 with automated deployment.

**Features:**
- Static website hosting on S3
- Public access with bucket policies
- Custom deployment automation
- Only uploads changed files (checksum comparison)
- Content-type detection and setting
- Deployment statistics and logging

**Live URL:** `http://my-abou-portfolio-site.s3-website-eu-west-1.amazonaws.com`

**Tech Stack:** HTML, CSS, Python, boto3, S3, IAM

---

### 2. Automated Website Deployment Script

Python script that intelligently deploys website files to S3.

**File:** `scripts/deploy_website.py`

**Features:**
- Compares local files with S3 (MD5 checksums)
- Only uploads new or changed files
- Automatic content-type detection
- Retry logic with exponential backoff
- Error classification (permanent vs transient)
- Deployment statistics (uploaded, updated, skipped, failed)
- S3 pagination support (handles large buckets)

**Usage:**
```bash
python scripts/deploy_website.py
```

**Output:**
```
2025-02-10 14:30:22 - INFO - Bucket 'my-portfolio' is accessible
2025-02-10 14:30:23 - INFO - Uploaded index.html
2025-02-10 14:30:23 - INFO - Updated style.css
2025-02-10 14:30:23 - INFO - Skipping logo.png (unchanged)
2025-02-10 14:30:24 - INFO - Deployment Summary:
2025-02-10 14:30:24 - INFO - Total: 15
2025-02-10 14:30:24 - INFO - Uploaded: 3
2025-02-10 14:30:24 - INFO - Updated: 2
2025-02-10 14:30:24 - INFO - Skipped: 10
```

---

### 3. Enhanced Backup System (Week 8 + S3)

Extended Week 8 backup automation with AWS S3 cloud upload capabilities.

**File:** `backup_with_s3.py`

**New Features:**
- Uploads backups to S3 after local creation
- Stores SHA256 checksum in S3 object metadata
- Verifies uploads by comparing checksums
- Date-organized S3 structure (backups/2025/02/10/)
- Separate retention policies (local vs S3)
- S3 rotation (deletes old cloud backups)
- Optional local cleanup after verified upload
- CLI flags to control S3 upload behavior

**Configuration (.env):**
```
# S3 Settings
UPLOAD_TO_S3=true
S3_BACKUP_BUCKET=your-backups-bucket
S3_PREFIX=backups/
S3_RETENTION_DAYS=30
DELETE_LOCAL_AFTER_UPLOAD=false
```

**Usage:**
```bash
# Backup with S3 upload
python backup_with_s3.py --upload

# Backup without S3 (local only)
python backup_with_s3.py --no-upload

# Upload and delete local after verification
python backup_with_s3.py --upload --delete-local
```

**S3 Organization:**
```
s3://my-backups/
  backups/
    2025/
      02/
        10/
          project_20250210_143022.tar.gz
          project_20250210_143022.json
```

---

### 4. S3 Sync Utility

General-purpose S3 synchronization tool with diff-based uploads.

**File:** `scripts/s3_sync.py`

**Features:**
- Three-phase sync algorithm (scan local → scan S3 → calculate diff)
- Checksum-based comparison (MD5 for local, ETag for S3)
- Only uploads new/changed files
- Optional deletion of remote files
- Dry-run mode
- Progress tracking and statistics

**Usage:**
```bash
# Sync local folder to S3 bucket
python s3_sync.py --source ./website --bucket my-bucket

# Dry-run (preview changes)
python s3_sync.py --source ./website --bucket my-bucket --dry-run

# Sync with deletion of extra S3 files
python s3_sync.py --source ./website --bucket my-bucket --delete
```

**Output:**
```
2025-02-10 15:00:00 - INFO - To upload: 3
2025-02-10 15:00:00 - INFO - To skip: 12
2025-02-10 15:00:00 - INFO - To delete: 1
2025-02-10 15:00:01 - INFO - Uploaded (1/3): new-page.html
2025-02-10 15:00:02 - INFO - Uploaded (2/3): updated.css
2025-02-10 15:00:03 - INFO - Uploaded (3/3): image.png
2025-02-10 15:00:03 - INFO - Sync complete
2025-02-10 15:00:03 - INFO - Uploaded=3, Skipped=12, Deleted=1
```

---

## Skills Demonstrated

✅ **AWS Account Management** - Secure setup with MFA and billing alerts  
✅ **IAM Security** - Users, groups, policies, least privilege principle  
✅ **S3 Operations** - Bucket creation, uploads, downloads, deletion, policies  
✅ **Static Website Hosting** - S3 website configuration and bucket policies  
✅ **boto3 Programming** - Programmatic AWS access with Python  
✅ **Checksum Verification** - Data integrity with MD5 and SHA256  
✅ **Sync Algorithms** - Diff-based file synchronization  
✅ **Error Classification** - AWS error handling and retry strategies  
✅ **S3 Pagination** - Handling large buckets (>1000 objects)  
✅ **Cloud Storage Patterns** - Date-based organization, metadata storage  

---

## Technical Highlights

### 1. Intelligent Deployment with Checksum Comparison

```python
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
```

**Why this matters:**
- Uses pagination (handles buckets with >1000 objects)
- Builds ETag map for comparison
- Only uploads files that changed
- Production-grade approach

### 2. S3 Metadata for Checksums

```python
# Store checksum during upload
s3.upload_file(
    str(archive),
    bucket,
    s3_key,
    ExtraArgs={"Metadata": {"sha256": checksum}}
)

# Verify upload
head = s3.head_object(Bucket=bucket, Key=s3_key)
s3_checksum = head["Metadata"]["sha256"]

if checksum == s3_checksum:
    logger.info("Upload verified!")
```

**Why this matters:**
- Stores integrity information with file
- Enables future verification
- Standard practice in production backups
- No separate manifest needed

### 3. Date-Organized S3 Structure

```python
def build_s3_key(prefix, archive, dt):
    date_path = f"{dt.year}/{dt.month:02d}/{dt.day:02d}/"
    return f"{prefix}{date_path}{archive.name}"

# Creates: backups/2025/02/10/backup_143022.tar.gz
```

**Why this matters:**
- Easy to navigate backups by date
- Standard cloud storage pattern
- Supports lifecycle policies
- Scalable organization

### 4. Three-Phase Sync Algorithm

```python
# Phase 1: Build local state
local_manifest = build_local_manifest(source_dir)

# Phase 2: Build remote state  
s3_manifest = build_s3_manifest(s3, bucket)

# Phase 3: Calculate diff
to_upload, to_skip, to_delete = build_sync_plan(
    local_manifest, s3_manifest
)
```

**Why this matters:**
- Separates scanning from execution
- Efficient (one pass through files)
- Enables dry-run mode
- How professional sync tools work

### 5. AWS Error Classification

```python
except ClientError as e:
    code = e.response["Error"]["Code"]
    
    if code in ["AccessDenied", "NoSuchBucket"]:
        logger.error(f"Permanent error ({code}) → not retrying")
        return False
    
    # Retry transient errors
    if attempt < max_retries:
        time.sleep(2 ** attempt)
```

**Why this matters:**
- Distinguishes permanent vs transient errors
- Saves time (don't retry impossible operations)
- Pattern applies to all AWS services
- Production-ready error handling

---

## Project Structure

```
week10-s3-portfolio/
│
├── website/                    # Portfolio website files
│   ├── index.html
│   ├── style.css
│   └── assets/
│
├── scripts/                    # Automation scripts
│   ├── deploy_website.py      # Website deployment
│   └── s3_sync.py             # S3 sync utility
│
├── backup_with_s3.py          # Enhanced backup (Week 8 + S3)
├── config.py                  # Backup configuration
├── .env                       # Environment variables
├── requirements.txt           # boto3 dependency
├── .gitignore                # Exclude secrets
│
├── logs/                      # Log files
│   └── backup.log
│
└── README.md                  # This file
```

---

## Setup & Configuration

### Prerequisites

- AWS account with free tier
- AWS CLI configured
- Python 3.10+
- boto3 installed

### Installation

```bash
# Install dependencies
pip install boto3 python-dotenv

# Configure AWS credentials
aws configure
```

### Environment Variables

Create `.env` file:

```
# Backup Configuration (Week 8)
BACKUP_SOURCES=/path/to/folder1,/path/to/folder2
BACKUP_DESTINATION=/path/to/backups
RETENTION_DAYS=7
MIN_BACKUPS_TO_KEEP=3
LOG_LEVEL=INFO

# S3 Configuration (Week 10)
UPLOAD_TO_S3=true
S3_BACKUP_BUCKET=your-backups-bucket
S3_PREFIX=backups/
S3_RETENTION_DAYS=30
DELETE_LOCAL_AFTER_UPLOAD=false
```

---

## Testing

All scripts tested with:
- ✅ Multiple file uploads/downloads
- ✅ Large files (>100MB)
- ✅ Network failures (retry logic)
- ✅ Permission errors
- ✅ Bucket pagination (>1000 objects)
- ✅ Checksum mismatches
- ✅ Dry-run modes

---

## Cost Management

**Free Tier Usage:**
- S3: 5GB storage, 20,000 GET, 2,000 PUT
- All Week 10 activities: **$0** (within free tier)

**Monitoring:**
- Billing alerts configured ($1 threshold)
- Weekly cost review in AWS Console

---

## Security

✅ Root account has MFA enabled  
✅ IAM user for daily work (not root)  
✅ Bucket policies limit public access  
✅ AWS credentials not committed to Git  
✅ Least privilege IAM policies  

---

## What I Learned

**AWS Fundamentals:**
- Setting up secure AWS account
- IAM users, roles, and policies
- AWS security best practices

**S3 Mastery:**
- Bucket creation and configuration
- Static website hosting
- Bucket policies and access control
- boto3 S3 operations
- S3 pagination for large buckets

**Cloud Automation:**
- Intelligent deployment (checksum comparison)
- Data integrity verification
- Cloud backup strategies
- Sync algorithms
- Error handling patterns

**Production Patterns:**
- Date-based storage organization
- Metadata for checksums
- Dual retention policies
- Verification before deletion
- Comprehensive logging

---

## Challenges & Solutions

**Challenge 1: MD5 vs ETag Mismatch**
- **Problem:** ETag doesn't always equal MD5 (multipart uploads)
- **Solution:** Used MD5 for local files, ETag for S3 (consistent comparison)

**Challenge 2: S3 Pagination**
- **Problem:** list_objects_v2 only returns 1000 objects
- **Solution:** Used paginator to handle large buckets

**Challenge 3: Integration Complexity**
- **Problem:** Adding S3 to existing backup script broke logic
- **Solution:** Careful step-by-step integration with testing at each stage

**Challenge 4: Upload Verification**
- **Problem:** How to verify S3 upload succeeded?
- **Solution:** Store checksum in S3 metadata, compare after upload

---

## Future Enhancements

- [ ] CloudFront CDN for faster website delivery
- [ ] Custom domain with Route 53
- [ ] S3 lifecycle policies for automatic archival
- [ ] Backup encryption at rest
- [ ] Parallel uploads for large files
- [ ] Email notifications on backup failure
- [ ] Cost tracking and reporting

---

**Week 10 Complete!** This week established foundational AWS skills and cloud automation patterns. The backup system is now production-ready with cloud integration, and the portfolio website is live on AWS. Skills acquired here form the basis for all future AWS work (EC2, VPC, ECS, etc.). Ready for Week 11: EC2 & Networking! 
