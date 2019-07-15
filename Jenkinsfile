import groovy.json.JsonOutput;

def json_files
def script_output
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
    stage('Execute script') {
      steps {
        script {
         
            
            // sh 'python -u ConvertReport.py bfmongodb IPV6_000000_allSite_daily 5cc2006d016c58023e9d76dc'
            script_output = sh(returnStdout: true, script: 'python ConvertReport.py bfmongodb IPV6_000000_allSite_daily 5cc2006d016c58023e9d76dc')
            def json = JsonOutput.toJson(script_output)
            new File("output.json").write(json)
            echo " ${script_output}"
            def outJson = readJSON text: script_output
            //groovy.json.JsonOutput.toJson(script_output)
            writeJSON file: 'test_json.json', json: outJson
        }
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
