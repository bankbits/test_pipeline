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
            /* File file1 = new File(build.workspace.toString() + "/output2.json")
            file1.createNewFile()

            boolean exists = file1.exists();
            if(exists == true)
            {
                // printing the permissions associated with the file
                println "Executable: " + file1.canExecute();
                println "Readable: " + file1.canRead();
                println "Writable: "+ file1.canWrite();
            }
            else
            {
                println "File not found.";
            } */
           
            // sh 'python -u ConvertReport.py bfmongodb IPV6_000000_allSite_daily 5cc2006d016c58023e9d76dc'
            // script_output = sh(returnStdout: true, script: 'python ConvertReport.py bfmongodb IPV6_000000_allSite_daily 5cc2006d016c58023e9d76dc')
            // def json = JsonOutput.toJson(script_output)
            //jsonSlurper = new JsonSlurper()

            //File config_file = new File('/Users/dianabank/Desktop/test_pipeline/config.json')
            //config_data = jsonSlurper.parse(config_file)
            config_data = readJSON file: '/Users/dianabank/Desktop/test_pipeline/config.json'
            def reports = config_data.reports
            reports.each { 

              jsonSlurper = new JsonSlurperClassic()
              def server = it["server"]
              def col = it["collection"]
              def object = it["object"] 
              println (server + " " + col + " " + object)

              script_str = 'python ConvertReport.py ' + server + ' ' + col + ' ' + object
              script_output = sh(returnStdout: true, script: script_str)
              def output_test = jsonSlurper.parseText(script_output) 
              echo "${output_test}"
              // json = jsonSlurper2.parseText(script_output)
              // echo "${script_output}"
              /* File file = new File('/Users/dianabank/Desktop/test_pipeline/reports.json')
              data = jsonSlurper.parse(file)
              data.bfa_reports = data.bfa_reports << json
              String newJson = new JsonBuilder(data).toPrettyString()
              
              file.write(newJson)
              echo "OUTPUT NEW JSON ${newJson}"

              script_output = null
              json = null
              newJson = null */
            }
            // echo "${config_data['reports']}"

            //writeJSON file: '/Users/dianabank/Desktop/test_pipeline/reports.json', json: json_str, pretty: 4
            // file.write(json_str)
            
            
            // def outJson = readJSON text: script_output
            
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
