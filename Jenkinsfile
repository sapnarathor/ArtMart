pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git branch: 'master',
                    url: 'https://github.com/sapnarathor/ArtMart.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t artmart:latest .'
            }
        }

        stage('Stop Old Container') {
            steps {
                sh 'docker stop artmart || true'
                sh 'docker rm artmart || true'
            }
        }

        stage('Run New Container') {
            steps {
                sh 'docker run -d --name artmart -p 5000:5000 artmart:latest'
            }
        }
    }
}
