# ☁️ Week 11 — EC2 & Networking: `cloud-nginx-deployer`

> **Cloud Engineering Roadmap** · Week 11 of 24

A fully scripted EC2 deployment tool that launches a production-like Ubuntu server, auto-configures it on boot via user data, serves a custom Nginx page, manages an attached EBS volume, creates an AMI snapshot, and tears everything down cleanly — **zero console clicking, pure CLI**.

---

## 📋 Overview

This project automates the full lifecycle of an EC2 instance using Bash and the AWS CLI. Instead of clicking through the AWS console, every resource — key pair, security group, EC2 instance, EBS volume, AMI snapshot — is created, managed, and destroyed programmatically.

The goal: if you can't script it, you don't fully understand it.

---

## 📁 Project Structure

```
cloud-nginx-deployer/
├── deploy.sh                # Main launcher — spins up all resources from scratch
├── teardown.sh              # Destroys all created resources cleanly and in order
├── userdata.sh              # Injected into EC2 at boot — installs & configures Nginx
├── ebs_setup.sh             # Local script — creates and attaches EBS volume
├── ebs_setup_inside.sh      # EC2-side script — formats, mounts, and persists the volume
├── snapshot.sh              # Creates an AMI backup of the running instance
├── config.env               # Your environment config (not committed)
├── html/
│   └── index.html           # Custom page served by Nginx
└── README.md
```

---

## ✨ Features

- 🚀 **One-command deploy** — `./deploy.sh` handles everything: key pair, security group, instance launch, tagging, and waits
- 🔒 **Secure by default** — SSH locked to your current IP only, HTTP open to the world
- ⚡ **Automated boot config** — Nginx installed and serving your custom page before you even SSH in
- 🔑 **Safe key management** — atomic write with temp file + move to prevent corrupt `.pem` files
- 💾 **EBS volume lifecycle** — create, attach, format, mount, persist across reboots via `/etc/fstab`
- 📸 **AMI snapshot** — full instance backup with timestamp, waits for availability
- 🧹 **Clean teardown** — destroys resources in the correct dependency order (instance → volume → AMI → snapshots → SG → key pair)
- 📋 **State tracking** — `.deploy_state` file tracks all resource IDs across scripts
- 🛡️ **IMDSv2** — uses token-based instance metadata (secure modern standard, not deprecated v1)

---

## 🛠️ Skills Demonstrated

| Area | Details |
|------|---------|
| **AWS EC2** | Launch, tag, wait, describe, terminate instances via CLI |
| **Networking** | Security Groups, inbound/outbound rules, port management |
| **SSH** | Key pair creation, `.pem` handling, remote access |
| **Nginx** | Install, configure, serve static content, enable on boot |
| **User Data** | Automated boot scripting with full logging and IMDSv2 metadata |
| **EBS** | Volume create, attach, format (ext4), mount, fstab persistence |
| **AMI Snapshots** | Image creation, availability wait, snapshot cleanup |
| **Bash Scripting** | `set -euo pipefail`, heredocs, atomic writes, state files, error handling |
| **AWS CLI** | `--query`, `--output text`, `wait` commands, resource filtering |

---

## ⚙️ Technical Highlights

### IMDSv2 Token-Based Metadata
Uses the secure modern metadata approach — token-based, not the deprecated v1:
```bash
TOKEN=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" \
  -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
INSTANCE_ID=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" \
  http://169.254.169.254/latest/meta-data/instance-id)
```

### Atomic Key File Write
Prevents a corrupt half-written `.pem` if the process is interrupted:
```bash
aws ec2 create-key-pair --key-name "$KEY_NAME" \
  --query 'KeyMaterial' --output text > "$TMP_KEY"
mv "$TMP_KEY" "$KEY_PATH"
chmod 400 "$KEY_PATH"
```

### Double-Wait Pattern
Waits for both AWS provisioning AND instance health checks — not just `running`:
```bash
aws ec2 wait instance-running --instance-ids "$INSTANCE_ID"
aws ec2 wait instance-status-ok --instance-ids "$INSTANCE_ID"
```

### Correct Teardown Order
Respects AWS resource dependencies — deletes in the right sequence to avoid errors:
```
instance terminated → EBS volume deleted → AMI deregistered → snapshots deleted → SG deleted → key pair deleted
```

### Snapshot IDs Captured Before AMI Deregistration
Once an AMI is deregistered, you can no longer query its snapshots. The script captures snapshot IDs first:
```bash
SNAPSHOT_IDS=$(aws ec2 describe-images --image-ids "$AMI_ID" \
  --query 'Images[0].BlockDeviceMappings[*].Ebs.SnapshotId' --output text)
aws ec2 deregister-image --image-id "$AMI_ID"
# then delete snapshots
```

---

## 🚀 Setup & Configuration

### Prerequisites
- AWS CLI installed and configured (`aws configure`)
- An active AWS account with EC2/IAM permissions
- Bash shell (Linux / macOS / WSL)

### 1. Clone the repo
```bash
git clone https://github.com/<your-username>/cloud-nginx-deployer.git
cd cloud-nginx-deployer
```

### 2. Create `config.env`
```bash
cp config.env.example config.env
```

Edit `config.env`:
```bash
KEY_NAME="week11-key"
SG_NAME="week11-sg"
INSTANCE_TYPE="t2.micro"
REGION="eu-west-1"               # your AWS region
AMI_ID="ami-xxxxxxxxxxxxxxxxx"   # Ubuntu 22.04 LTS in your region
PROJECT_TAG="cloudpath"
WEEK_TAG="11"
```

> Find the correct Ubuntu 22.04 AMI ID for your region at [Ubuntu EC2 AMI Finder](https://cloud-images.ubuntu.com/locator/ec2/)

### 3. Make scripts executable
```bash
chmod +x deploy.sh teardown.sh ebs_setup.sh snapshot.sh
```

---

## 📖 Usage

### Deploy
```bash
./deploy.sh
```
Outputs the public IP, browser URL, and SSH command when done.

### Verify
```bash
# Open in browser
http://<public-ip>

# SSH in
ssh -i week11-key.pem ubuntu@<public-ip>

# Check boot log on EC2
cat /var/log/cloud-init-output.log
cat /var/log/deploy_info.txt
```

### Attach & Mount EBS Volume
```bash
# Local — creates and attaches the volume
./ebs_setup.sh

# On EC2 — formats, mounts, and persists
scp -i week11-key.pem ebs_setup_inside.sh ubuntu@<public-ip>:~/
ssh -i week11-key.pem ubuntu@<public-ip>
bash ebs_setup_inside.sh
```

### Create AMI Snapshot
```bash
./snapshot.sh
```

### Tear Down Everything
```bash
./teardown.sh
```

> ⚠️ Always run teardown when done. A running EC2 instance continues to incur charges.

---

## 🔐 Security Notes

- `config.env`, `.pem` files, and `.deploy_state` are in `.gitignore` — never committed
- SSH access is restricted to your current public IP (`/32`) at deploy time
- IMDSv2 enforced in all metadata calls

---

## 📚 What I Learned

- How EC2, security groups, key pairs, and EBS volumes fit together as a system
- The difference between `instance-running` and `instance-status-ok` and why it matters
- Why IMDSv2 exists and how token-based metadata fetch works
- How `user data` enables fully hands-free server configuration at boot
- The correct resource deletion order in AWS to avoid dependency errors
- How EBS volumes persist across stop/start but not across termination
- Defensive bash scripting: `set -euo pipefail`, atomic writes, state files

---

## 🗺️ Roadmap Context

This project is part of a structured 24-week Cloud Engineering roadmap:

| Week | Topic |
|------|-------|
| 1–4 | Linux, Bash, Networking |
| 5–8 | Python, Automation, APIs |
| 9 | Git & Collaborative Workflows |
| 10 | AWS IAM & S3 |
| **11** | **EC2 & Networking** |
| 12 | VPC & Mini Project |
| 13–14 | Load Balancing, Auto Scaling, RDS |
| 15–16 | Terraform |
| 17–19 | Docker, ECS, CI/CD |
| 20–24 | Monitoring, Security, Serverless, Final Project |

---

*Part of the [Cloud Engineering Roadmap](https://github.com/<your-username>/cloud-engineering-roadmap) — 24 weeks from Linux to production-grade AWS infrastructure.*
