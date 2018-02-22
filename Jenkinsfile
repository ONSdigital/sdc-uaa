pipeline {
    agent any

    triggers {
        pollSCM('* * * * *')
    }

    stages {
        stage('build') {
            agent {
                docker {
                    image 'maven:latest'
                }

            }
            steps {
                sh 'mvn clean install'
            }
        }
        stage('snapshot') {
            agent {
                docker {
                    image 'maven:latest'
                }

            }
            environment {
                ARTIFACTORY = credentials('ARTIFACTORY')
            }
            steps {
                sh 'mvn  --settings .maven.settings.xml deploy'
            }
        }

        stage('dev') {
            agent {
                docker {
                    image 'governmentpaas/cf-cli'
                    args '-u root'
                }

            }

            environment {
                CLOUDFOUNDRY_API = credentials('CLOUDFOUNDRY_API')
                CF_DOMAIN = credentials('CF_DOMAIN')
                CF_USER = credentials('CF_USER')
                UAA_PRIVATE_KEY_PASSWORD = credentials('UAA_PRIVATE_KEY_PASSWORD')
                UAA_PRIVATE_KEY = credentials('UAA_PRIVATE_KEY')
                UAA_CERTIFICATE = credentials('UAA_CERTIFICATE')
                UAA_JWT_SIGNING_KEY = credentials('UAA_JWT_SIGNING_KEY')
                UAA_JWT_VERIFICATION_KEY = credentials('UAA_JWT_VERIFICATION_KEY')
                UAA_ID = 'sdx'
                UAA_SECRET = 'cakes'
                ORG = 'rmras'
                SPACE = 'dev'
            }
            steps {
                sh 'sh deploy-uaa-pre-steps.sh'
                sh 'cat uaa-cf-application.yml'
                sh 'cf push -f uaa-cf-application.yml'
                sh 'git reset --hard'
            }
        }
    }

    post {
        always {
            cleanWs()
            dir('${env.WORKSPACE}@tmp') {
                deleteDir()
            }
            dir('${env.WORKSPACE}@script') {
                deleteDir()
            }
            dir('${env.WORKSPACE}@script@tmp') {
                deleteDir()
            }
        }
    }
}