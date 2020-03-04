pipeline {
  agent {
    docker {
      image 'docker.io/python:current'
    }
  }
  stages {
    stage('Preparation') {
      steps {
        sh 'rm -rf build'
      }
    }
    stage ('Build') {
      steps {
        sh 'python3 setup.py build'
      }
    }
    stage ('Test') {
      steps {
        sh 'python3 setup.py test'
      }
    }
  }
}
