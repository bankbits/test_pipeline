import hudson.model.*;
import hudson.util.*;
import hudson.scm.*;
import hudson.plugins.accurev.*

def thr = Thread.currentThread();
def build = thr?.executable;

def changeSet= build.getChangeSet();

changeSet.getItems();