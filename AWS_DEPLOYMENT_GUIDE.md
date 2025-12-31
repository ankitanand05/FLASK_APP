# 🚀 AWS EC2 Deployment Guide - Step by Step

## 📋 Overview

We'll deploy your Flask app to AWS EC2 using **industry-standard practices**:

✅ **EC2 Instance** - Virtual server to run your app  
✅ **Security Groups** - Firewall rules  
✅ **GitHub Actions** - Automated deployment  
✅ **Systemd Service** - Keep app running 24/7  
✅ **Nginx** - Production web server (reverse proxy)  

---

## 🎯 Deployment Steps

### **Phase 1: AWS Setup** (Manual - Do Once)
1. Create EC2 Instance
2. Configure Security Groups
3. Create IAM User for GitHub Actions
4. Generate SSH Key Pair

### **Phase 2: Server Configuration** (Manual - Do Once)
1. Install Python & Dependencies
2. Install Nginx
3. Configure Systemd Service
4. Configure Nginx as Reverse Proxy

### **Phase 3: GitHub Actions** (Automated)
1. Add AWS secrets to GitHub
2. Create deployment workflow
3. Auto-deploy on push to main

---

## 📝 Phase 1: AWS Setup

### Step 1.1: Create EC2 Instance

1. **Login to AWS Console**: https://console.aws.amazon.com/
2. **Navigate to EC2**: Services → EC2
3. **Click "Launch Instance"**

4. **Configure Instance:**
   - **Name**: `flask-task-manager`
   - **AMI**: Ubuntu Server 22.04 LTS (Free tier eligible)
   - **Instance type**: `t2.micro` (Free tier)
   - **Key pair**: Create new key pair
     - Name: `flask-app-key`
     - Type: RSA
     - Format: `.pem` (for SSH)
     - **DOWNLOAD and SAVE IT!** ⚠️ You can't download it again!

5. **Network Settings:**
   - ✅ Allow SSH traffic from: My IP
   - ✅ Allow HTTP traffic from: Internet
   - ✅ Allow HTTPS traffic from: Internet

6. **Storage**: 8 GB (default - Free tier)

7. **Click "Launch Instance"**

### Step 1.2: Configure Security Group

After instance launches:
1. Go to **Security Groups**
2. Find your instance's security group
3. **Edit Inbound Rules** → Add:
   - **Type**: Custom TCP
   - **Port**: 5000 (Flask app port)
   - **Source**: 0.0.0.0/0 (Anywhere)
   - **Description**: Flask App

### Step 1.3: Get Instance Public IP

1. Go to **Instances**
2. Select your instance
3. Copy **Public IPv4 Address** (e.g., 3.15.123.45)
4. **Save this IP** - you'll need it!

### Step 1.4: Create IAM User for GitHub Actions

1. **Go to IAM**: Services → IAM
2. **Users** → **Add users**
3. **User name**: `github-actions-deploy`
4. **Access type**: ✅ Access key - Programmatic access
5. **Permissions**: Attach policies directly
   - Search and add: `AmazonEC2FullAccess`
6. **Create user**
7. **Download credentials** or copy:
   - Access Key ID
   - Secret Access Key
   - **SAVE THESE!** You'll need them for GitHub Secrets

---

## 📝 Phase 2: Server Configuration

### Step 2.1: Connect to EC2

Open terminal (PowerShell):

```powershell
# Navigate to where you saved the .pem file
cd C:\path\to\your\key

# Connect via SSH (replace IP with your instance IP)
ssh -i flask-app-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

If permission error on Windows:
```powershell
icacls flask-app-key.pem /inheritance:r
icacls flask-app-key.pem /grant:r "%username%":"(R)"
```

### Step 2.2: Install Dependencies on EC2

Once connected to EC2, run these commands:

```bash
# Update system
sudo apt update
sudo apt upgrade -y

# Install Python and pip
sudo apt install python3-pip python3-venv nginx -y

# Create app directory
mkdir -p /home/ubuntu/flask-app
cd /home/ubuntu/flask-app

# Clone your repository
git clone https://github.com/ankitanand05/FLASK_APP.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn  # Production WSGI server
```

### Step 2.3: Create Systemd Service

Create service file to keep Flask running:

```bash
sudo nano /etc/systemd/system/flask-app.service
```

Paste this content:

```ini
[Unit]
Description=Flask Task Manager Application
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/flask-app
Environment="PATH=/home/ubuntu/flask-app/venv/bin"
ExecStart=/home/ubuntu/flask-app/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Save: `Ctrl+X` → `Y` → `Enter`

Enable and start service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable flask-app
sudo systemctl start flask-app
sudo systemctl status flask-app  # Should show "active (running)"
```

### Step 2.4: Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/flask-app
```

Paste this:

```nginx
server {
    listen 80;
    server_name YOUR_EC2_PUBLIC_IP;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/flask-app /etc/nginx/sites-enabled/
sudo nginx -t  # Test configuration
sudo systemctl restart nginx
```

### Step 2.5: Test Deployment

Open browser: `http://YOUR_EC2_PUBLIC_IP`

You should see your Flask app! 🎉

---

## 📝 Phase 3: GitHub Actions Auto-Deployment

### Step 3.1: Add Secrets to GitHub

1. Go to: https://github.com/ankitanand05/FLASK_APP/settings/secrets/actions
2. Click **"New repository secret"**
3. Add these secrets:

| Name | Value |
|------|-------|
| `EC2_HOST` | Your EC2 Public IP |
| `EC2_USERNAME` | `ubuntu` |
| `EC2_SSH_KEY` | Contents of your `.pem` file |
| `AWS_ACCESS_KEY_ID` | From IAM user |
| `AWS_SECRET_ACCESS_KEY` | From IAM user |

### Step 3.2: Update GitHub Actions Workflow

We'll modify the main.yml workflow to include deployment.

---

## 🎓 What You're Learning

- ✅ AWS EC2 instance management
- ✅ Linux server administration
- ✅ Nginx reverse proxy setup
- ✅ Systemd service configuration
- ✅ SSH key management
- ✅ Security groups and IAM
- ✅ Automated deployment pipelines

**These are real DevOps engineer skills!** 🚀

---

## 📊 Final Architecture

```
GitHub (Code Push)
    ↓
GitHub Actions (CI/CD)
    ↓
    ├─→ Run Tests
    └─→ Deploy to EC2 via SSH
        ↓
EC2 Instance
    ├─→ Nginx (Port 80) ← Users
    └─→ Flask App (Port 5000)
```

---

## ⚠️ Important Notes

1. **Free Tier Limits**: 750 hours/month of t2.micro (enough for 1 instance 24/7)
2. **Stop instance** when not using to save hours
3. **Elastic IP** costs money if not attached - we're using Public IP instead
4. **Keep .pem file safe** - it's your server key!
5. **Never commit secrets** to GitHub - use GitHub Secrets

---

Ready to start? Let's begin with **Phase 1: AWS Setup**! 🚀
