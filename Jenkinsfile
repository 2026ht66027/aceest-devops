pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python3 -m pip install -r requirements.txt'
            }
        }

        stage('Syntax Validation') {
            steps {
                sh 'python3 -m py_compile app.py'
                sh 'python3 -m compileall -q source_versions'
            }
        }

        stage('Automated Tests') {
            steps {
                sh 'python3 -m pytest -v'
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t aceest-fitness:latest .'
            }
        }

        stage('Quality Gate') {
            steps {
                sh 'docker run --rm aceest-fitness:latest'
            }
        }
    }

    post {
        always {
            echo 'ACEest CI pipeline execution completed.'
        }
    }
}