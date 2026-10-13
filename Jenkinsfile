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
                script {
                    catchError(
                        buildResult: 'FAILURE',
                        stageResult: 'FAILURE'
                    ) {
                        sh 'python3 -m pytest tests/ -v'
                    }
                }
            }
        }

        stage('Docker Build') {
            when {
                expression {
                    currentBuild.currentResult == 'SUCCESS'
                }
            }

            steps {
                sh '''
                    set -eu

                    if docker image inspect ${IMAGE_NAME}:latest \
                        >/dev/null 2>&1; then
                        docker tag ${IMAGE_NAME}:latest \
                            ${IMAGE_NAME}:previous
                    fi

                    docker build \
                        -t ${IMAGE_NAME}:candidate .
                '''
            }
        }

        stage('Quality Gate') {
            when {
                expression {
                    currentBuild.currentResult == 'SUCCESS'
                }
            }

            steps {
                sh 'docker run --rm ${IMAGE_NAME}:candidate'
            }
        }

        stage('Promote Image') {
            when {
                expression {
                    currentBuild.currentResult == 'SUCCESS'
                }
            }

            steps {
                sh '''
                    docker tag ${IMAGE_NAME}:candidate \
                        ${IMAGE_NAME}:latest
                '''
            }
        }

        stage('Rollback') {
            when {
                expression {
                    currentBuild.currentResult == 'FAILURE'
                }
            }

            steps {
                script {
                    sh '''
                        if docker image inspect ${IMAGE_NAME}:previous \
                            >/dev/null 2>&1; then

                            docker tag ${IMAGE_NAME}:previous \
                                ${IMAGE_NAME}:latest

                            echo "Rollback successful: previous image restored."

                        else

                            echo "No previous image exists."
                            echo "Nothing can be restored on this first build."

                        fi
                    '''
                }
            }
        }
    }

    post {
        always {
            echo 'ACEest CI pipeline execution completed.'
        }

        failure {
            echo 'Pipeline failed. Check the stage logs and rollback result.'
        }

        success {
            echo 'Pipeline completed successfully.'
        }
    }
}