# Quiz App — CI/CD with Jenkins, Docker, and AWS EC2

Flask quiz app that auto-deploys to EC2 on every `git push`.

**Pipeline:** GitHub push → Webhook → Jenkins → Docker build → Container restart → Live

---

## 📁 File Structure

```
quiz-app/
├── app.py              # Flask app (quiz logic)
├── requirements.txt    # Python deps
├── Dockerfile          # Container recipe
├── Jenkinsfile         # CI/CD pipeline
├── .gitignore
├── README.md
└── templates/
    ├── index.html      # Quiz page
    └── result.html     # Results page
```

---

## 🖥️ Where to run each step

| Symbol | Where |
|--------|-------|
| 💻 | **Local VS Code terminal** (your laptop) |
| ☁️ | **AWS Console** (browser) |
| 🔧 | **EC2 SSH terminal** (inside the EC2 after you SSH in) |
| 🌐 | **Jenkins web UI** (browser, http://EC2_IP:8080) |
| 📦 | **GitHub website** (browser) |

---

## PART 1 — Local setup and push to GitHub

### Step 1: Test the app locally 💻

```bash
cd quiz-app
pip install -r requirements.txt
python app.py
```
Open http://localhost:5000 — you should see the quiz. Press `Ctrl+C` to stop.

### Step 2: Create a GitHub repo 📦

1. Go to https://github.com/new
2. Name it `quiz-app`, make it **Public**, click **Create**
3. Copy the repo URL (e.g. `https://github.com/YOUR_USERNAME/quiz-app.git`)

### Step 3: Push code to GitHub 💻

```bash
cd quiz-app
git init
git add .
git commit -m "Initial quiz app"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/quiz-app.git
git push -u origin main
```

---

## PART 2 — Launch EC2 instance ☁️

1. Go to **AWS Console → EC2 → Launch Instance**
2. Fill in:
   - **Name:** `quiz-app-server`
   - **AMI:** Ubuntu Server 22.04 LTS (free tier eligible)
   - **Instance type:** `t2.micro` (free tier) — or `t2.small` if Jenkins feels slow
   - **Key pair:** Create new → name it `quiz-key` → download `quiz-key.pem` (save it somewhere safe!)
   - **Network settings → Edit → Security Group → Add these inbound rules:**
     | Type | Port | Source |
     |------|------|--------|
     | SSH | 22 | My IP |
     | Custom TCP | 8080 | Anywhere (0.0.0.0/0) — Jenkins |
     | Custom TCP | 5000 | Anywhere (0.0.0.0/0) — Quiz App |
   - **Storage:** 16 GB (default 8 GB is tight for Jenkins + Docker)
3. Click **Launch Instance**
4. Once it says "Running", copy the **Public IPv4 address** (e.g. `13.234.56.78`)

---

## PART 3 — SSH into EC2 and install tools 🔧

### Step 1: SSH into EC2 💻

```bash
# On Mac/Linux:
chmod 400 ~/Downloads/quiz-key.pem
ssh -i ~/Downloads/quiz-key.pem ubuntu@YOUR_EC2_PUBLIC_IP

# On Windows (PowerShell):
ssh -i C:\Users\YourName\Downloads\quiz-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

You're now **inside the EC2**. Every command below runs here (🔧).

### Step 2: Install Docker 🔧

```bash
sudo apt update
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ubuntu
```

### Step 3: Install Java (Jenkins needs it) 🔧

```bash
sudo apt install -y openjdk-17-jdk
```

### Step 4: Install Jenkins 🔧

```bash
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null

echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null

sudo apt update
sudo apt install -y jenkins
sudo systemctl start jenkins
sudo systemctl enable jenkins
```

### Step 5: Let Jenkins run Docker 🔧

```bash
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

### Step 6: Install git and curl (usually already there) 🔧

```bash
sudo apt install -y git curl
```

### Step 7: Get the Jenkins initial admin password 🔧

```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```
**Copy this password** — you'll paste it in a moment.

---

## PART 4 — Configure Jenkins 🌐

### Step 1: Open Jenkins

Go to `http://YOUR_EC2_PUBLIC_IP:8080` in your browser.

### Step 2: Unlock Jenkins

- Paste the admin password from Step 7 above
- Click **Install suggested plugins** (wait ~2 min)
- Create an admin user (username + password — remember these!)
- Click **Save and Finish** → **Start using Jenkins**

### Step 3: Install the GitHub plugin (usually already installed)

**Manage Jenkins → Plugins → Available plugins** → search "GitHub" → install if not there.

### Step 4: Create the pipeline job

1. **Jenkins dashboard → New Item**
2. Name: `quiz-app-pipeline`
3. Type: **Pipeline** → OK
4. Scroll to **Build Triggers** → check ✅ **GitHub hook trigger for GITScm polling**
5. Scroll to **Pipeline** section:
   - **Definition:** Pipeline script from SCM
   - **SCM:** Git
   - **Repository URL:** `https://github.com/YOUR_USERNAME/quiz-app.git`
   - **Branch:** `*/main`
   - **Script Path:** `Jenkinsfile`
6. Click **Save**

### Step 5: Run it manually once

Click **Build Now** on the left. Wait for it to go green ✅. If something breaks, click the build number → **Console Output** to see why.

Once green, open `http://YOUR_EC2_PUBLIC_IP:5000` — **your quiz is LIVE**.

---

## PART 5 — Add the GitHub Webhook 📦

This is what makes it auto-trigger on `git push`.

1. Go to your GitHub repo → **Settings → Webhooks → Add webhook**
2. Fill in:
   - **Payload URL:** `http://YOUR_EC2_PUBLIC_IP:8080/github-webhook/` (keep the trailing slash!)
   - **Content type:** `application/json`
   - **Which events:** Just the push event
   - **Active:** ✅
3. Click **Add webhook**
4. GitHub will ping it immediately — you should see a green ✅ checkmark next to the webhook.

---

## 🎉 PART 6 — Test the full pipeline

On your laptop 💻:

```bash
# Edit a question in app.py (change any question text)
git add .
git commit -m "Update quiz question"
git push
```

Within ~10 seconds:
- GitHub fires the webhook
- Jenkins starts a new build (watch it on the Jenkins dashboard)
- Docker rebuilds, old container stops, new one starts
- Refresh `http://YOUR_EC2_PUBLIC_IP:5000` — you see the change!

---

## 🐛 Troubleshooting

| Problem | Fix |
|---------|-----|
| Jenkins build fails: `docker: permission denied` | Run `sudo usermod -aG docker jenkins && sudo systemctl restart jenkins` on EC2 |
| Can't reach Jenkins UI | Check EC2 Security Group allows port 8080 |
| Can't reach quiz app | Check Security Group allows port 5000 |
| Webhook not firing | Test it in GitHub → Webhooks → Recent Deliveries → Redeliver |
| `git push` asks for password | Use a GitHub Personal Access Token instead of password, or set up SSH keys |
| Build hangs on `docker build` | t2.micro is slow; wait 2-3 min or upgrade to t2.small |

---

## 🛑 Stop paying AWS

When done, **terminate the EC2 instance** in the AWS Console to stop charges.
