import groovy.json.JsonOutput;
import groovy.json.JsonSlurper;

import groovy.json.JsonSlurperClassic;

import groovy.json.*;
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
    stage('Execute script') {
      steps {
        script {
            
            config_data = readJSON file: '/Users/dianabank/Desktop/test_pipeline/config.json'
            def reports = config_data.reports
            reports.each { 

              def server = it["server"]
              def col = it["collection"]
              def object = it["object"] 
              println (server + " " + col + " " + object)

              script_str = 'python ConvertReport.py ' + server + ' ' + col + ' ' + object
              script_output = sh(returnStdout: true, script: script_str)
             
              def output_test = readJSON text: script_output
              echo "${output_test}"
              
            }
        }
      }
    }
    stage("last changes") {
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
