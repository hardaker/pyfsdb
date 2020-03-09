pipeline {
  agent {
    docker {
      image 'docker.io/python:3'
    }
  }
  stages {
    stage('Preparation') {
      steps {
        withEnv(["HOME=${env.WORKSPACE}"]) {
	  sh 'pip install --user pandas'
	}
      }
    }
    stage ('Build') {
      steps {
        sh 'python3 setup.py build'
      }
    }
    stage ('Test') {
      steps {
        withEnv(["HOME=${env.WORKSPACE}"]) {
          sh 'python3 setup.py test'
	}
      }
    }
  }
  post {
    failure {
      emailext(
        subject: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
        body: """<p>FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p>
            <p>Check console output at &QUOT;<a href='${env.BUILD_URL}'>${env.JOB_NAME} [${env.BUILD_NUMBER}]</a>&QUOT;</p>""",
        recipientProviders: [[$class: 'DevelopersRecipientProvider']]
      )
    }
  }
}
