# 🐳 Docker Guide for Flask App

## 📚 What is Docker?

**Docker** = A way to package your app with everything it needs into a **container**

Think of it like:
- 📦 A shipping container for your code
- 🎒 A backpack with your app + Python + all dependencies
- 🏠 A mini computer that runs your app the same way everywhere

---

## 🎯 Why Use Docker?

### **Without Docker** ❌
```
Your Computer: Works! ✅
Your Friend's Computer: Error! ❌
AWS Server: Missing Python! ❌
Different OS: Won't run! ❌
```

### **With Docker** ✅
```
Your Computer: Works! ✅
Your Friend's Computer: Works! ✅
AWS Server: Works! ✅
Any OS: Works! ✅
```

**"It works on my machine" → "It works everywhere!"**

---

## 🏗️ Docker Concepts

### **1. Dockerfile**
- Recipe to build your container
- Lists all steps to set up your app
- Like a cooking recipe for your app environment

### **2. Docker Image**
- Built from Dockerfile
- A snapshot/template of your app
- Can be shared and reused

### **3. Docker Container**
- Running instance of an image
- Your actual app running
- Like launching a program from an .exe

---

## 📝 Your Dockerfile Explained

```dockerfile
# Start with Python already installed
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy your app code
COPY . .

# Run your app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

**What each line does:**
- `FROM` - Start with a base (Python pre-installed)
- `WORKDIR` - Create and enter /app folder
- `COPY` - Copy files from your computer to container
- `RUN` - Execute commands (install packages)
- `CMD` - Command to run when container starts

---

## 🚀 Docker Commands (Quick Reference)

### **Build an image:**
```bash
docker build -t flask-task-manager .
```
- `-t` = tag/name your image
- `.` = use current directory's Dockerfile

### **Run a container:**
```bash
docker run -p 5000:5000 flask-task-manager
```
- `-p 5000:5000` = map port 5000 (host:container)
- `-d` = run in background (detached)

### **List running containers:**
```bash
docker ps
```

### **Stop a container:**
```bash
docker stop <container-id>
```

### **Remove containers:**
```bash
docker rm <container-id>
```

### **List images:**
```bash
docker images
```

### **Remove images:**
```bash
docker rmi flask-task-manager
```

---

## 🔧 Docker in GitHub Actions

### **What We Added:**

#### **Development Workflow:**
```yaml
docker-build:
  - Build Docker image
  - Test it works
  - Validate health endpoint
```

#### **Production Workflow:**
```yaml
docker-build-push:
  - Build Docker image
  - Test it works
  - (Optional) Push to Docker Hub
```

### **How It Works:**

```
1. Code pushed to GitHub
   ↓
2. GitHub Actions triggers
   ↓
3. Build Docker image
   ↓
4. Run container
   ↓
5. Test /health endpoint
   ↓
6. ✅ Pass = Image is good!
   ❌ Fail = Image broken, don't deploy
```

---

## 📦 Docker Hub (Optional)

**Docker Hub** = GitHub for Docker images

### **To Enable Push to Docker Hub:**

1. **Create Docker Hub account**: https://hub.docker.com/

2. **Create Access Token:**
   - Docker Hub → Account Settings → Security → New Access Token
   - Name it: `github-actions`
   - Copy the token

3. **Add to GitHub Secrets:**
   - Go to: https://github.com/ankitanand05/FLASK_APP/settings/secrets/actions
   - Add secrets:
     - `DOCKER_USERNAME` = Your Docker Hub username
     - `DOCKER_PASSWORD` = Your access token

4. **Push & Done!**
   - Next push to main will upload to Docker Hub
   - Anyone can pull your image: `docker pull yourusername/flask-task-manager`

---

## 🎓 Key Benefits

### **1. Consistency**
- Same environment everywhere
- No "works on my machine" problems

### **2. Isolation**
- App runs in its own bubble
- Won't conflict with other apps

### **3. Portability**
- Run anywhere Docker is installed
- Move between local, AWS, Azure, anywhere

### **4. Scalability**
- Easy to run multiple containers
- Load balancing made simple

### **5. Version Control**
- Tag images with versions
- Easy rollback if needed

---

## 🔄 Docker + GitHub Actions Flow

```
Developer pushes code
        ↓
GitHub Actions runs
        ↓
    Builds Docker image
        ↓
    Tests in container
        ↓
    ✅ Tests pass?
        ↓
    Push to Docker Hub (optional)
        ↓
    Deploy to AWS EC2
        ↓
    Pull image on server
        ↓
    Run container
        ↓
    App is live! 🎉
```

---

## 💡 Industry Standard Practices

✅ **Multi-stage builds** - Smaller images  
✅ **Non-root user** - Security (we use `flaskuser`)  
✅ **Health checks** - Monitor container health  
✅ **.dockerignore** - Exclude unnecessary files  
✅ **Caching layers** - Faster builds  
✅ **Gunicorn** - Production-ready WSGI server  

**You're building production-grade containers!** 🚀

---

## 🧪 Test Docker Locally

Want to test Docker on your computer?

### **1. Install Docker Desktop:**
- Windows: https://docs.docker.com/desktop/install/windows-install/
- Download and install

### **2. Build your image:**
```bash
cd "d:\Ankit Anand\FLASK-APP"
docker build -t flask-task-manager .
```

### **3. Run it:**
```bash
docker run -d -p 5000:5000 --name my-flask-app flask-task-manager
```

### **4. Test:**
- Open: http://localhost:5000
- Your app is running in Docker! 🐳

### **5. Stop it:**
```bash
docker stop my-flask-app
docker rm my-flask-app
```

---

## 📊 What You've Learned

- ✅ What Docker is and why it matters
- ✅ How to write a Dockerfile
- ✅ Docker images vs containers
- ✅ Building and running containers
- ✅ Docker in CI/CD pipelines
- ✅ Production-ready container practices
- ✅ Docker Hub integration

**These are professional DevOps skills!** 🎓

---

## 🚀 Next Steps

Now when you deploy to AWS:
- Pull your Docker image
- Run container on EC2
- Consistent deployment every time
- Easy to scale and update

**Docker + GitHub Actions + AWS = Industry Standard Deployment!** 🌟
