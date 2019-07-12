def json_files
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
            sh 'python ConvertReport.py bfmongodb IPV6_000000_allSite_daily 5cc2006d016c58023e9d76dc'
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
        script {
          json_files = []
          def changeLogSets = currentBuild.changeSets
          for (int i = 0; i < changeLogSets.size(); i++) {
              def entries = changeLogSets[i].items
              for (int j = 0; j < entries.length; j++) {
                  def entry = entries[j]
                  echo "${entry.commitId} by ${entry.author} on ${new Date(entry.timestamp)}: ${entry.msg}"
                  def files = new ArrayList(entry.affectedFiles)
                  for (int k = 0; k < files.size(); k++) {
                      def file = files[k]
                      echo "  ${file.editType.name} ${file.path}"

                      def isJSON = file.path =~ /(.*?)\.(json)$/
                      def fileAdded = file.editType.name =~ /(.*?)(add)$/
                      
                      if (isJSON) {
                        json_files << file.path
                      }
                  }
              }
          }
          echo " ${json_files}"
        }
	    }
     }
  }
}
