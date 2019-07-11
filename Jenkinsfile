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
    stage("last-changes") {
	steps {
		script {
        		def publisher = LastChanges.getLastChangesPublisher "LAST_SUCCESSFUL_BUILD", "SIDE", "LINE", true, true, "", "", "", "", ""
              		publisher.publishLastChanges()
              		def changes = publisher.getLastChanges()
              		println(changes.getEscapedDiff())
              		for (commit in changes.getCommits()) {
                  		println(commit)
                  		def commitInfo = commit.getCommitInfo()
                  		println(commitInfo)
                  		println(commitInfo.getCommitMessage())
                  		println(commit.getChanges())
             		 }
     		 }
	}
     }
}
