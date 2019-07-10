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
    stage('Load') {
	steps {
		script {
			code = load 'readfiles.groovy'
		}
	}
    }
    stage('executeGroovy') {
	steps {
		script {
			code.getChangedFilesList()
		}
	}
    }
  }
}
