# Week 11 — Key Learnings (EC2, Nginx, Automation)

## 1. EC2 Lifecycle & Automation

* Learned how to fully automate EC2 provisioning using AWS CLI (`run-instances`)
* Understood the importance of **waiting for resource states** using:

  * `aws ec2 wait instance-running`
  * `aws ec2 wait instance-status-ok`
* Built a complete lifecycle:

  * **Deploy → Configure → Extend → Snapshot → Teardown**
* Realized that automation must be **idempotent** (safe to run multiple times)

---

## 2. User Data & Cloud-Init

* Understood that **user data scripts run automatically at first boot**
* Learned that AWS does NOT execute the file itself — it passes it to **cloud-init**
* Implemented:

  * `set -euo pipefail` for strict error handling
  * Output redirection:

    ```bash
    exec > /var/log/userdata.log 2>&1
    ```
* Used **heredoc (`cat <<EOF`)** to generate files dynamically inside EC2
* Learned that user data runs **only once**, not on every reboot

---

## 3. Nginx Configuration & Web Serving

* Understood how Nginx serves static content from:

  * `/var/www/html`
* Learned the role of:

  * `root` → directory to serve files from
  * `index` → default file
* Differentiated between:

  * Static serving (HTML files)
  * Reverse proxy (forwarding to backend apps)
* Practiced reloading safely:

  ```bash
  sudo nginx -t && sudo systemctl reload nginx
  ```

---

## 4. Networking Fundamentals (EC2)

* Learned difference between:

  * **Public IP** → used from browser / SSH
  * **Private IP** → used inside AWS network
* Understood why SSH failed when using private IP externally
* Security Groups act as:

  ```text
  Stateful firewalls attached to EC2 instances
  ```
* Observed real-time effects:

  * Removing HTTP rule → site inaccessible
  * Adding it back → site instantly available

---

## 5. Instance Metadata Service (IMDS)

* Used IMDS to query instance data without credentials:

  ```bash
  curl http://169.254.169.254/latest/meta-data/instance-id
  ```
* Learned IMDS is:

  * Only accessible **inside EC2**
  * Useful for dynamic scripts
* Faced and debugged issues when IMDS returned empty (timing / syntax)

---

## 6. EBS Volumes — Storage Lifecycle

* Understood EBS as:

  ```text
  Persistent block storage attached to EC2
  ```
* Practiced:

  * Creating volume
  * Attaching to instance
  * Formatting (`mkfs.ext4`)
  * Mounting (`mount`)
* Learned:

  ```text
  Formatting = preparing filesystem
  Mounting = making it accessible in Linux
  ```
* Ensured persistence using `/etc/fstab`
* Verified data survives stop/start cycles

---

## 7. AMI & Snapshot Relationship

* Learned:

  ```text
  AMI = metadata
  Snapshot = actual disk data
  ```
* Created AMIs using:

  ```bash
  aws ec2 create-image --no-reboot
  ```
* Discovered important dependency:

  ```text
  Must extract snapshot IDs BEFORE deregistering AMI
  ```
* Understood that:

  * AMI references snapshots
  * Snapshots do NOT reference AMI

---

## 8. State Management in Scripts

* Used `.deploy_state` file to track:

  * Instance ID
  * Security Group ID
  * AMI ID
* Learned that:

  ```text
  Overwriting state = losing track of old resources
  ```
* Designed scripts assuming:

  ```text
  One active deployment at a time
  ```
* Realized this is a simplified version of:

  * Terraform state management

---

## 9. Bash Scripting Best Practices

* Used:

  ```bash
  set -euo pipefail
  ```
* Learned importance of:

  * Checking command success
  * Validating variables (`set -u`)
* Implemented:

  * Temporary file pattern (`.tmp`) for safe writes
  * Conditional logic for idempotency
* Handled edge cases:

  * Empty values
  * "None" from AWS CLI
* Built interactive prompts for safer execution

---

## 10. Key Pair Management

* Understood that:

  ```text
  AWS stores only the public key
  Private key (.pem) is generated once and must be kept locally!
  ```
* Implemented logic to:

  * Detect missing local key
  * Prompt user for recreation
  * Safely regenerate key pairs
* Learned that deleting a key:

  ```text
  Breaks SSH access to existing instances
  ```

---

## 11. Debugging & Real-World Issues

* Debugged:

  * SSH connection refused (wrong IP, security group)
  * Broken pipe (idle SSH session)
  * IMDS returning empty values
  * Nginx not accessible (network vs service issue)
* Learned to systematically check:

  ```text
  Instance → Network → Service → Logs
  ```

---

## 12. Separation of Concerns

* Clearly understood separation between:

  * **Local machine (AWS CLI)** → infrastructure control
  * **EC2 instance** → OS-level configuration
* Learned why:

  ```text
  Some actions must happen locally (AWS API)
  Others must happen inside EC2 (Linux commands)
  ```

---

## 13. Project Design Thinking

* Built a structured automation project:

  ```text
  deploy.sh → provision
  userdata.sh → configure
  ebs_setup.sh → extend storage
  snapshot.sh → backup
  teardown.sh → destroy
  ```
* Practiced:

  * Modular scripting
  * Reusability
  * Clear separation of responsibilities

---

## 🚀 Final Takeaways

* Infrastructure can be fully automated without using the AWS Console
* State management is critical to avoid resource leaks and unexpected costs
* Order of operations matters in cloud environments
* Defensive scripting (validation, checks, prompts) is essential
* This project mirrors real-world DevOps workflows and prepares for tools like Terraform

---
