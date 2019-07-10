import com.tikal.jenkins.plugins.multijob.*
import hudson.*
import hudson.model.*
import hudson.plugins.git.*
import hudson.slaves.*
import hudson.tasks.*

jenkins = Jenkins.instance

def ln = System.getProperty('line.separator')
println "---------------Groovy Changelog script Started---------------$ln"

def lastSuccesfulBuild = build.previousNotFailedBuild
def failed = build.result != hudson.model.Result.SUCCESS

println "Last Succesful Build: ${lastSuccesfulBuild}"
println "Current Build Result, is failed?: ${failed}"


def currResult = build.result
def prevResult = build.previousBuild?.result ?: null

def consecutiveSuccess = currResult == hudson.model.Result.SUCCESS && prevResult == hudson.model.Result.SUCCESS

def builds = []
def changes = []
def count = 0

def getChangedFilesList() {

    if (consecutiveSuccess) {
        println "Last Build was sucessful, getting latest changes$ln"

        builds << build
        def changeItems = build.changeSet.items
        println "Change Items: ${changeItems}$ln"

        count += changeItems.length
        changes += changeItems as List
    } else {
        println "Last Build was not sucessful, getting changes from all failed build as well$ln"

        println "BUILD: $build$ln"

        println "Hudson version: $build.hudsonVersion$ln"

        println "Change set: $build.changeSet$ln"

        println "Change set items: $build.changeSet.items$ln"

        while (lastSuccesfulBuild) {
            builds << lastSuccesfulBuild
            def changeSet = lastSuccesfulBuild.changeSet
            if (!changeSet.emptySet) {
                def changeItems = lastSuccesfulBuild.changeSet.items
                count += changeItems.length
                changes += changeItems as List
            }
            lastSuccesfulBuild = lastSuccesfulBuild.nextBuild
        }
    }
}

return this