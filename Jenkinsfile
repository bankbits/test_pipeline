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
      steps {
	git diff --name-only $GIT_PREVIOUS_COMMIT $GIT_COMMIT
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
			files = code.getChangedFilesList()
			println "files list is $files"
			
		}
	}
    }
  }
}
