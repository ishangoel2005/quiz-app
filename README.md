# Quiz App – CI/CD with Jenkins, Docker and AWS EC2

A Flask-based quiz application that automatically deploys to AWS EC2 whenever code is pushed to GitHub using an automated CI/CD pipeline.

**Pipeline:** GitHub Push → Webhook → Jenkins → Docker Build → Container Restart → Live Application

---

## Project Overview

The project demonstrates the implementation of an automated Continuous Integration and Continuous Deployment (CI/CD) pipeline using GitHub, Jenkins, Docker and AWS EC2.

The Flask Quiz Application is hosted on an AWS EC2 Ubuntu virtual machine. Whenever a developer pushes code changes to GitHub, a webhook triggers Jenkins, which builds a new Docker image, replaces the existing container and deploys the updated application automatically.

This eliminates the need for manual deployment after every code update.

---

## 1. Tool Introduction – AWS Cloud Platform

Amazon Web Services (AWS) is a cloud computing platform provided by Amazon that offers computing, storage, networking and other IT resources over the internet.

This project uses **Amazon EC2 (Elastic Compute Cloud)** to launch an Ubuntu-based virtual machine and host the Flask Quiz Application. It provides the required cloud infrastructure without needing to maintain a physical server.

**Cloud Service Used:** AWS EC2 (Infrastructure as a Service – IaaS).

---

## 2. Service Exploration – AWS Cloud Service Models

AWS supports different cloud service models that provide computing resources at different levels of management.

- **IaaS (Infrastructure as a Service):** Provides virtual machines, storage and networking. AWS EC2 is used in this project to launch an Ubuntu server and host the application.
- **PaaS (Platform as a Service):** Provides a managed environment for application development and deployment. AWS Elastic Beanstalk is an example that simplifies application deployment without requiring users to manage the underlying infrastructure manually.
- **SaaS (Software as a Service):** Provides ready-to-use software over the internet. Amazon QuickSight is an example used for business intelligence and data visualization.

**Implementation:** This project primarily uses the IaaS model through AWS EC2, while Jenkins and Docker handle automation and application deployment.

---

## 3. Practical Demonstration – AWS EC2

The project demonstrates the practical configuration and use of AWS EC2 through the following operations:

1. Launching an Ubuntu-based EC2 virtual machine through the AWS Management Console.
2. Connecting to the instance remotely using SSH.
3. Installing and configuring Docker, Java and Jenkins.
4. Connecting Jenkins with the GitHub repository.
5. Configuring a GitHub webhook to trigger the Jenkins pipeline automatically.
6. Building and deploying the Flask application inside a Docker container.
7. Accessing the deployed application through the EC2 public IP address.

---

## 4. Feature Identification – AWS EC2

### Important Features

- **On-demand Computing:** Launch virtual machines whenever required.
- **Configurable Resources:** Select instance types with different CPU, memory and computing capacities.
- **Security Groups:** Control incoming and outgoing network traffic through configurable rules.
- **Remote Access:** Connect to virtual machines using SSH.
- **Scalability:** Upgrade or modify computing resources according to application requirements.

### Benefits

- Eliminates the need to maintain physical servers.
- Provides flexible and scalable computing infrastructure.
- Enables remote application hosting and management.
- Supports integration with automation and deployment tools.

### Applications

- Website and web application hosting.
- Software development and testing.
- Cloud-based application deployment.
- Running automated CI/CD pipelines.

---

## 5. Real-Time Application – Automated Quiz Deployment

This project demonstrates a real-world CI/CD workflow by automatically deploying a Flask Quiz Application on AWS EC2.

Whenever code is pushed to GitHub:

1. GitHub sends a notification through the configured webhook.
2. Jenkins automatically triggers the CI/CD pipeline.
3. Docker builds a new image containing the updated application.
4. The existing container is stopped and replaced with the updated container.
5. The latest version of the application becomes accessible through the EC2 public IP address.

This process reduces manual deployment effort and makes application updates faster and more consistent.

---

## File Structure
```text
quiz-app/
├── app.py              # Flask app (quiz logic)
├── requirements.txt    # Python dependencies
├── Dockerfile          # Container recipe
├── Jenkinsfile         # CI/CD pipeline
├── .gitignore
├── README.md
└── templates/
    ├── index.html      # Quiz page
    └── result.html     # Results page
```

---

## Where to Run Each Step

| Environment            | Purpose                                                   |
| ---------------------- | --------------------------------------------------------- |
| Local VS Code Terminal | Running and testing the application locally; Git commands |
| AWS Console            | Creating and configuring the EC2 instance                 |
| EC2 SSH Terminal       | Installing Docker, Java, Jenkins and other tools          |
| Jenkins Web UI         | Configuring and monitoring the CI/CD pipeline             |
| GitHub Website         | Creating the repository and configuring webhooks          |

---

## PART 1 – Local Setup and Push to GitHub

### Step 1: Test the App Locally
```bash
cd quiz-app
pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000` in your browser. You should see the quiz application.

Press `Ctrl+C` to stop the application.

### Step 2: Create a GitHub Repository

1. Visit [https://github.com/new](https://github.com/new)
2. Name the repository `quiz-app`.
3. Set the repository to **Public**.
4. Click **Create Repository**.
5. Copy the repository URL.

Example:
```text
https://github.com/YOUR_USERNAME/quiz-app.git
```

### Step 3: Push Code to GitHub

Run the following commands in your local VS Code terminal:
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

## PART 2 – Launch AWS EC2 Instance

1. Open **AWS Console → EC2 → Launch Instance**.
2. Configure the following settings:
   - **Name:** `quiz-app-server`
   - **AMI:** Ubuntu Server 22.04 LTS
   - **Instance Type:** `t2.micro` (if eligible for the applicable free-tier offer) or `t2.small` if additional resources are required.
   - **Key Pair:** Create a new key pair named `quiz-key`.
   - Download and securely save `quiz-key.pem`.
3. Under **Network Settings → Edit → Security Group**, configure these inbound rules:

| Type       | Port | Source                          |
| ---------- | ---- | ------------------------------- |
| SSH        | 22   | My IP                           |
| Custom TCP | 8080 | My IP (Jenkins UI)              |
| Custom TCP | 5000 | As required for quiz app access |

For a public demonstration, port 5000 can be opened to `0.0.0.0/0`. Restrict access where possible.

4. **Storage:** Configure 16 GB to provide sufficient space for Jenkins and Docker.
5. Click **Launch Instance**.
6. Once the instance is running, copy its **Public IPv4 Address**.

Example:
```text
13.234.56.78
```

---

## PART 3 – SSH into EC2 and Install Tools

### Step 1: SSH into EC2

**On Mac/Linux:**
```bash
chmod 400 ~/Downloads/quiz-key.pem
ssh -i ~/Downloads/quiz-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

**On Windows (PowerShell):**
```powershell
ssh -i C:\Users\YourName\Downloads\quiz-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

You are now connected to the EC2 instance. All subsequent commands in this section should be executed inside the EC2 terminal.

### Step 2: Install Docker
```bash
sudo apt update
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ubuntu
```

### Step 3: Install Java

Jenkins requires Java to run.
```bash
sudo apt install -y openjdk-17-jdk
```

### Step 4: Install Jenkins
```bash
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null

echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null

sudo apt update
sudo apt install -y jenkins
sudo systemctl start jenkins
sudo systemctl enable jenkins
```

### Step 5: Allow Jenkins to Run Docker
```bash
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

### Step 6: Install Git and Curl
```bash
sudo apt install -y git curl
```

### Step 7: Get Jenkins Initial Admin Password
```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

Copy the generated password. It will be required to unlock Jenkins.

---

## PART 4 – Configure Jenkins

### Step 1: Open Jenkins

Open the following URL in your browser:
```text
http://YOUR_EC2_PUBLIC_IP:8080
```

### Step 2: Unlock Jenkins

- Enter the initial admin password obtained in Part 3.
- Click **Install Suggested Plugins**.
- Create an administrator account.
- Click **Save and Finish**.
- Select **Start using Jenkins**.

### Step 3: Install GitHub Plugin

Navigate to:

**Manage Jenkins → Plugins → Available Plugins**

Search for the GitHub plugin and install it if it is not already installed.

### Step 4: Create the Pipeline Job

1. Open the Jenkins Dashboard.
2. Click **New Item**.
3. Enter the name `quiz-app-pipeline`.
4. Select **Pipeline** and click **OK**.
5. Under **Build Triggers**, enable:

   `GitHub hook trigger for GITScm polling`
6. Under the **Pipeline** section, configure:
   - **Definition:** Pipeline script from SCM
   - **SCM:** Git
   - **Repository URL:** `https://github.com/YOUR_USERNAME/quiz-app.git`
   - **Branch:** `*/main`
   - **Script Path:** `Jenkinsfile`
7. Click **Save**.

### Step 5: Run the Pipeline Manually

1. Open the `quiz-app-pipeline` job.
2. Click **Build Now**.
3. Wait for the pipeline to complete successfully.
4. Open the build number and select **Console Output** to inspect execution logs if required.

Once the build succeeds, open:
```text
http://YOUR_EC2_PUBLIC_IP:5000
```

Your Quiz Application should now be live.

---

## PART 5 – Configure GitHub Webhook

The GitHub webhook automatically notifies Jenkins whenever new code is pushed to the repository.

### Step 1: Open GitHub Webhook Settings

Navigate to:

**GitHub Repository → Settings → Webhooks → Add Webhook**

### Step 2: Configure the Webhook

Enter the following details:

| Field        | Configuration                                    |
| ------------ | ------------------------------------------------ |
| Payload URL  | `http://YOUR_EC2_PUBLIC_IP:8080/github-webhook/` |
| Content Type | `application/json`                               |
| Events       | Just the push event                              |
| Active       | Enabled                                          |

**Note:** Keep the trailing slash in the webhook URL.

Click **Add Webhook**.

GitHub will send an initial test notification. Check the webhook's recent deliveries to verify that it is reaching Jenkins successfully.

---

## PART 6 – Test the Complete CI/CD Pipeline

Once the application and webhook are configured, test the complete automated deployment process.

On your local laptop, make a small change to a quiz question in `app.py`.

Run:
```bash
git add .
git commit -m "Update quiz question"
git push
```

### Expected Workflow

After the GitHub push:

1. GitHub sends a webhook notification to Jenkins.
2. Jenkins automatically starts a new pipeline build.
3. Docker builds a new image with the updated application.
4. The previous container is stopped and replaced.
5. The updated application starts running on EC2.

Refresh the application:
```text
http://YOUR_EC2_PUBLIC_IP:5000
```

The updated quiz question should now be visible.

**Result:** The Flask Quiz Application is automatically updated on AWS EC2 whenever new code is pushed to GitHub.

---

## Troubleshooting

| Problem                                          | Solution                                                                                                       |
| ------------------------------------------------ | -------------------------------------------------------------------------------------------------------------- |
| Jenkins build fails: `docker: permission denied` | Run `sudo usermod -aG docker jenkins` and restart Jenkins.                                                     |
| Cannot access Jenkins UI                         | Check whether the EC2 Security Group allows inbound traffic on port 8080.                                      |
| Cannot access the Quiz App                       | Check whether the Security Group allows inbound traffic on port 5000 and verify that the container is running. |
| GitHub webhook is not triggering Jenkins         | Check GitHub → Settings → Webhooks → Recent Deliveries and try Redeliver.                                      |
| Git push asks for a password                     | Use a GitHub Personal Access Token or configure SSH authentication.                                            |
| Docker build takes too long                      | Check available EC2 resources. A `t2.micro` instance may be slow when running Jenkins and Docker together.     |

---

## Project Outcome

The project successfully demonstrates how cloud infrastructure and DevOps tools can be integrated to automate application deployment.

By combining AWS EC2, GitHub, Jenkins and Docker, the Flask Quiz Application can be updated and deployed automatically without manually rebuilding or restarting the application after every code change.

**Key Learning Outcomes:**

- Understanding AWS cloud infrastructure and EC2 instance management.
- Exploring IaaS, PaaS and SaaS cloud service models.
- Configuring Linux-based cloud servers using SSH.
- Containerizing applications using Docker.
- Implementing automated CI/CD pipelines using Jenkins.
- Integrating GitHub webhooks for automated build triggers.
- Deploying and managing web applications on cloud infrastructure.

---

## Technologies Used

| Category           | Technology     |
| ------------------ | -------------- |
| Cloud Platform     | AWS            |
| Cloud Service      | Amazon EC2     |
| Operating System   | Ubuntu 22.04   |
| Backend Framework  | Flask (Python) |
| Version Control    | Git and GitHub |
| CI/CD Tool         | Jenkins        |
| Containerization   | Docker         |
| Automation Trigger | GitHub Webhook |
| Deployment         | AWS EC2        |

---

**Project:** Flask Quiz Application with Automated CI/CD Deployment  
**Cloud Platform:** Amazon Web Services (AWS)  
**Deployment Architecture:** GitHub → Jenkins → Docker → AWS EC2
