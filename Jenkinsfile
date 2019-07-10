pipeline {
  agent any
  stages {
    stage('myStage'){
      steps {
        sh 'ls -la' 
      }
    }
    stage('Build') {
      steps { 
        sh 'ls' 
      }
    }
    stage('nextStage') {
        steps {
            sh 'python ./test1.py'
        }
    }
    stage('readFiles') {

	steps {
		script {
			def rootDir = pwd()
			println("Current Directory: " + rootDir)
			def example = load "/readfiles.groovy"
			readfiles.getChangedFilesList()
		}
	}
    }
  }
}
