pipeline {
    agent any

    environment {
        ENV_FILE = "${params.DEPLOY_ENV == 'qa' ? '.env.qa' : '.env.prod'}"
    }

    parameters {
        choice(name: 'DEPLOY_ENV', choices: ['qa', 'prod'], description: 'choose ur env')
    }

    stages {
        stage('Clone Repository') {
            steps {
                // 從 GitHub 拉取代碼
                git branch: 'main', url: 'https://github.com/w94vu06/flyway_test.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                // 建置 Docker 映像檔
                sh 'docker-compose --env-file ${ENV_FILE} build'
            }
        }

        stage('Run Database Migrations') {
            steps {
                // 使用 Flyway 執行資料庫變更
                sh '''
                flyway -url=jdbc:postgresql://db:5432/testdb \
                       -user=postgres -password=root migrate
                '''
            }
        }

        stage('Deploy Application') {
            steps {
                // 啟動容器
                sh 'docker-compose --env-file ${ENV_FILE} up -d'
            }
        }
    }
}
