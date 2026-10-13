pipeline {
    agent any

    environment {
        IMAGE_NAME = 'aceest-fitness'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python3 -m pip install -r requirements.txt'
                sh 'python3 -m pip install pytest'
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
                sh 'python3 -m pytest tests/ -v'
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    set -eu

                    # Preserve the last successfully promoted image.
                    if docker image inspect ${IMAGE_NAME}:latest \
                        >/dev/null 2>&1; then
                        docker tag ${IMAGE_NAME}:latest \
                            ${IMAGE_NAME}:previous
                    fi

                    # Build a candidate image without replacing latest.
                    docker build -t ${IMAGE_NAME}:candidate .
                '''
            }
        }

        stage('Quality Gate') {
            steps {
                sh 'docker run --rm ${IMAGE_NAME}:candidate'
            }
        }

        stage('Promote Image') {
            steps {
                sh '''
                    docker tag ${IMAGE_NAME}:candidate \
                        ${IMAGE_NAME}:latest

                    echo "Candidate image promoted to latest."
                '''
            }
        }
    }

    post {
        always {
            echo 'ACEest CI pipeline execution completed.'
        }

        failure {
            echo 'Pipeline failed. Attempting Docker image rollback.'

            sh '''
                if docker image inspect ${IMAGE_NAME}:previous \
                    >/dev/null 2>&1; then

                    docker tag ${IMAGE_NAME}:previous \
                        ${IMAGE_NAME}:latest

                    echo "Rollback successful: previous image restored."

                else
                    echo "No previous image exists; nothing to restore."
                fi
            '''
        }

        success {
            echo 'Pipeline completed successfully.'
        }
    }
}