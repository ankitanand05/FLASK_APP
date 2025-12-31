# 🚀 EC2 Docker Deployment - Step by Step Commands

## ✅ Prerequisites (Already Done)
- EC2 instance running
- Docker installed on EC2

---

## 📋 STEP 1: Deploy Your App on EC2

### Connect to your EC2 instance (if not already connected):
```bash
ssh -i your-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

### Once connected, run these commands:

#### 1. Clone your repository
```bash
cd ~
git clone https://github.com/ankitanand05/FLASK_APP.git
cd FLASK_APP
```

#### 2. Build Docker image
```bash
sudo docker build -t flask-task-manager .
```

#### 3. Run Docker container
```bash
sudo docker run -d \
  --name flask-app \
  -p 80:5000 \
  --restart unless-stopped \
  flask-task-manager
```

**Explanation:**
- `-d` = Run in background (detached mode)
- `--name flask-app` = Name the container
- `-p 80:5000` = Map port 80 (web) to container port 5000
- `--restart unless-stopped` = Auto-restart if crashes
- `flask-task-manager` = Your image name

#### 4. Verify it's running
```bash
sudo docker ps
```
You should see your container running!

#### 5. Test the app
```bash
curl http://localhost:5000/health
```
Should return: `{"status":"healthy","tasks_count":0}`

#### 6. Test from your browser
Open: `http://YOUR_EC2_PUBLIC_IP`

You should see your Flask app! 🎉

---

## 📋 STEP 2: Useful Docker Commands

### Check logs
```bash
sudo docker logs flask-app
```

### Stop container
```bash
sudo docker stop flask-app
```

### Start container
```bash
sudo docker start flask-app
```

### Restart container
```bash
sudo docker restart flask-app
```

### Remove container (to redeploy)
```bash
sudo docker stop flask-app
sudo docker rm flask-app
```

### Remove old images (cleanup)
```bash
sudo docker image prune -a
```

---

## 📋 STEP 3: Update/Redeploy Your App

When you make code changes and want to deploy:

```bash
# SSH to EC2
ssh -i your-key.pem ubuntu@YOUR_EC2_PUBLIC_IP

# Navigate to app directory
cd ~/FLASK_APP

# Pull latest code
git pull origin main

# Stop and remove old container
sudo docker stop flask-app
sudo docker rm flask-app

# Remove old image
sudo docker rmi flask-task-manager

# Build new image
sudo docker build -t flask-task-manager .

# Run new container
sudo docker run -d \
  --name flask-app \
  -p 80:5000 \
  --restart unless-stopped \
  flask-task-manager

# Verify
sudo docker ps
curl http://localhost:5000/health
```

---

## 📋 STEP 4: Setup Automated Deployment (Next)

We'll add to GitHub Actions so when you push to `main`:
1. GitHub Actions builds Docker image
2. Connects to your EC2 via SSH
3. Pulls latest code
4. Rebuilds and restarts container
5. **Zero downtime deployment!** 🚀

---

## 🔒 Security Note

Current setup exposes port 80. For production, you should:
- ✅ Use HTTPS with SSL certificate
- ✅ Set up a domain name
- ✅ Use environment variables for secrets
- ✅ Configure firewall rules properly

---

## 🎯 Quick Reference

| Task | Command |
|------|---------|
| View logs | `sudo docker logs flask-app` |
| Check status | `sudo docker ps` |
| Restart app | `sudo docker restart flask-app` |
| Access container shell | `sudo docker exec -it flask-app bash` |
| Check disk usage | `sudo docker system df` |
| Clean up | `sudo docker system prune -a` |

---

## 🐛 Troubleshooting

### Container won't start?
```bash
sudo docker logs flask-app  # Check error logs
sudo docker ps -a  # See all containers
```

### Port already in use?
```bash
sudo lsof -i :80  # Check what's using port 80
sudo docker stop flask-app  # Stop your container
```

### Out of disk space?
```bash
df -h  # Check disk usage
sudo docker system prune -a  # Clean up
```

---

**Ready for automated deployment?** Let me know when your app is running and we'll set up GitHub Actions! 🚀
