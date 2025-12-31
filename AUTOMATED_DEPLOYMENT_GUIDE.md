# 🚀 Automated Deployment Guide - GitHub Actions to EC2

## 📚 What is Automated Deployment?

**Before:** You manually SSH to server, pull code, rebuild, restart  
**After:** Push code to GitHub → GitHub Actions deploys automatically! 🎉

---

## 🎯 How It Works

```
1. You push code to main branch
   ↓
2. GitHub Actions detects the push
   ↓
3. Runs all tests
   ↓
4. Builds Docker image
   ↓
5. SSH into your EC2 server
   ↓
6. Pulls latest code
   ↓
7. Rebuilds Docker container
   ↓
8. Restarts application
   ↓
9. ✅ Your app is live with latest code!
```

**All this happens automatically in ~2-3 minutes!** 🚀

---

## 📋 STEP 1: Prepare EC2 for Automated Access

### 1.1 Create Deployment User (Optional but recommended)

SSH to your EC2 and run:

```bash
# Create a deploy user
sudo useradd -m -s /bin/bash deploy
sudo usermod -aG docker deploy
sudo su - deploy

# Create .ssh directory
mkdir -p ~/.ssh
chmod 700 ~/.ssh
```

### 1.2 Generate SSH Key for GitHub Actions

**On your local computer (PowerShell):**

```powershell
# Generate a new SSH key pair
ssh-keygen -t rsa -b 4096 -f github-actions-key -N ""
```

This creates two files:
- `github-actions-key` (private key) ← Keep secret!
- `github-actions-key.pub` (public key) ← Goes on EC2

### 1.3 Add Public Key to EC2

**Copy the public key content:**
```powershell
cat github-actions-key.pub
```

**SSH to EC2 and add it:**
```bash
# As ubuntu user (or deploy user if you created one)
echo "PASTE_YOUR_PUBLIC_KEY_HERE" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

**Test SSH access with the key:**
```powershell
ssh -i github-actions-key ubuntu@YOUR_EC2_IP
```

Should connect without password! ✅

---

## 📋 STEP 2: Add Secrets to GitHub

### 2.1 Get Your Private Key Content

```powershell
cat github-actions-key
```

Copy **ENTIRE** content including:
```
-----BEGIN OPENSSH PRIVATE KEY-----
...everything...
-----END OPENSSH PRIVATE KEY-----
```

### 2.2 Add Secrets to GitHub Repository

1. **Go to GitHub:**
   👉 https://github.com/ankitanand05/FLASK_APP/settings/secrets/actions

2. **Click "New repository secret"**

3. **Add these secrets one by one:**

| Secret Name | Value | Description |
|-------------|-------|-------------|
| `EC2_HOST` | Your EC2 Public IP (e.g., 3.15.123.45) | Server address |
| `EC2_USERNAME` | `ubuntu` (or `deploy` if you created that user) | SSH username |
| `EC2_SSH_KEY` | Content of `github-actions-key` file | Private SSH key |

**⚠️ IMPORTANT:** 
- Paste the ENTIRE private key including headers
- Make sure no extra spaces or newlines
- Keep the key file safe on your computer

---

## 📋 STEP 3: Create Deployment Script on EC2

### 3.1 SSH to EC2 and create deployment script:

```bash
# Create deployment script
cat > ~/deploy.sh << 'EOF'
#!/bin/bash

# Deployment script for Flask app
set -e  # Exit on any error

echo "🚀 Starting deployment..."

# Navigate to app directory
cd ~/FLASK_APP

# Pull latest code
echo "📥 Pulling latest code..."
git pull origin main

# Stop and remove old container
echo "🛑 Stopping old container..."
sudo docker stop flask-app || true
sudo docker rm flask-app || true

# Remove old image
echo "🗑️ Removing old image..."
sudo docker rmi flask-task-manager || true

# Build new image
echo "🏗️ Building new Docker image..."
sudo docker build -t flask-task-manager .

# Run new container
echo "🐳 Starting new container..."
sudo docker run -d \
  --name flask-app \
  -p 80:5000 \
  --restart unless-stopped \
  flask-task-manager

# Wait for app to start
echo "⏳ Waiting for app to start..."
sleep 10

# Health check
echo "🏥 Running health check..."
if curl -f http://localhost:5000/health; then
    echo "✅ Deployment successful!"
    echo "🎉 App is running at http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)"
else
    echo "❌ Health check failed!"
    exit 1
fi
EOF

# Make it executable
chmod +x ~/deploy.sh

# Test it
~/deploy.sh
```

This creates a script that handles the entire deployment process!

---

## 📋 STEP 4: Update GitHub Actions Workflow

The workflow file will be updated to include the deployment job.

**What the deployment job does:**
1. Waits for tests to pass
2. Waits for Docker build to succeed
3. SSH into your EC2
4. Runs the deployment script
5. Verifies deployment succeeded

---

## 📋 STEP 5: Test Automated Deployment

### 5.1 Make a Small Change

Let's test by making a small change to your app:

**Edit app.py** - Update the health check:
```python
@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy', 
        'tasks_count': len(tasks),
        'version': '2.0'  # Add version
    }), 200
```

### 5.2 Push to Development First

```powershell
cd "d:\Ankit Anand\FLASK-APP"
git checkout development
git add .
git commit -m "test: Add version to health check"
git push origin development
```

**Check GitHub Actions** - Should run tests and Docker build

### 5.3 Merge to Main (Triggers Deployment)

```powershell
git checkout main
git merge development
git push origin main
```

**Watch the magic happen!** 🪄
- Go to: https://github.com/ankitanand05/FLASK_APP/actions
- You'll see the workflow running
- It will deploy to EC2 automatically!

### 5.4 Verify Deployment

Check your app at: `http://YOUR_EC2_IP/health`

Should show:
```json
{
  "status": "healthy",
  "tasks_count": 0,
  "version": "2.0"
}
```

---

## 🎓 What You've Learned

- ✅ SSH key authentication
- ✅ GitHub Secrets management
- ✅ Automated CI/CD pipeline
- ✅ Docker deployment automation
- ✅ Zero-downtime deployment strategies
- ✅ Health check validation

**This is exactly how companies deploy to production!** 🌟

---

## 🔄 Your Complete Workflow Now

```
Developer (You)
    ↓ git push
GitHub Repository
    ↓ triggers
GitHub Actions
    ├─ Run Tests ✅
    ├─ Build Docker Image 🐳
    └─ Deploy to EC2 🚀
        ↓ SSH
EC2 Server
    ├─ Pull latest code
    ├─ Build new container
    ├─ Stop old container
    ├─ Start new container
    └─ Health check ✅
        ↓
Live Application! 🎉
```

---

## 💡 Best Practices You're Using

1. ✅ **Separate branches** - Develop on development, deploy from main
2. ✅ **Automated testing** - No broken code reaches production
3. ✅ **Docker containerization** - Consistent environments
4. ✅ **Health checks** - Verify deployment succeeded
5. ✅ **Secret management** - Secure credential storage
6. ✅ **Deployment script** - Repeatable process

---

## 🐛 Troubleshooting

### Deployment fails with SSH error?
- Check EC2_SSH_KEY secret has full private key
- Verify EC2_HOST is correct IP
- Ensure public key is in `~/.ssh/authorized_keys` on EC2

### Container won't start?
- SSH to EC2: `ssh -i github-actions-key ubuntu@YOUR_EC2_IP`
- Check logs: `sudo docker logs flask-app`
- Run deploy script manually: `~/deploy.sh`

### GitHub Actions stuck?
- Check Actions tab for error messages
- Verify all secrets are set correctly
- Check EC2 security group allows SSH (port 22)

---

## 🚀 Next Level (Optional)

Want to go further? You can add:
- **Blue-Green Deployment** - Zero downtime
- **Rollback Mechanism** - Revert to previous version
- **Environment Variables** - Configuration management
- **Database Migrations** - Handle schema changes
- **Slack Notifications** - Get notified on deployments
- **Custom Domain** - Use your own domain name
- **HTTPS/SSL** - Secure your application

---

**Ready to set it up?** Follow the steps above and let me know when you reach each checkpoint! 🎯
