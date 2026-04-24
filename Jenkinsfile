pipeline {
    agent any

    environment {
        IMAGE_NAME = "quiz-app"
        CONTAINER_NAME = "quiz-app-container"
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Pulling latest code from GitHub...'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t $IMAGE_NAME:latest .'
            }
        }

        stage('Stop Old Container') {
            steps {
                echo 'Stopping old container if it exists...'
                sh '''
                    docker stop $CONTAINER_NAME || true
                    docker rm $CONTAINER_NAME || true
                '''
            }
        }

        stage('Deploy New Container') {
            steps {
                echo 'Starting new container on port 5000...'
                sh 'docker run -d --name $CONTAINER_NAME -p 5000:5000 --restart unless-stopped $IMAGE_NAME:latest'
            }
        }

        stage('Health Check') {
            steps {
                echo 'Waiting for app to be ready...'
                sh 'sleep 5 && curl -f http://localhost:5000/health'
            }
        }
    }

    post {
        success {
            echo '✅ Deployment successful! App is live on port 5000.'
        }
        failure {
            echo '❌ Deployment failed. Check logs above.'
        }
    }
}
