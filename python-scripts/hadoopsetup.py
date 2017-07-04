#!/usr/bin/python2

import commands


def javaInstall(login):
 a=commands.getstatusoutput(login +" rpm -q jdk")
 print a
 if a[0]==0:
   print " java installed"
 else:
   print " java not installed"

def hadoopInstall(login):
 a=commands.getstatusoutput(login +" rpm -q hadoop")
 print a
 if a[0]==0:
   print " hadoop installed"
 else:
   print " hadoop not installed"
def stopFirewall(login):
 a=commands.getstatusoutput(login+" systemctl stop firewalld")
 print a
###############mapreduce---jobtracker###########

def configJobTracker(master_ip , jobtracker_ip):
  
  login="sudo docker exec jobtracker"
  #javaInstall(login)
  # hadoopInstall(login)
  
  u=commands.getstatusoutput(login + " hadoop-daemon.sh start jobtracker")
  #print " jobtracker configured"

#############mapred Tasktracker###########
def configTaskTracker(i):
  
  login="sudo docker exec tasktracker{} ".format(i)
  #javaInstall(login)
  #hadoopInstall(login) 
  v=commands.getstatusoutput(login + " hadoop-daemon.sh start tasktracker")
 # print "tasktracker{} configured".format(i)
  
#####################hdfs-datanode################

def configDataNode(i,l):
  login="sudo {} docker exec datanode{} ".format(l,i)
 # javaInstall(login)
 # hadoopInstall(login)
  e=commands.getstatusoutput(login + "mkdir /pop")
  c=commands.getstatusoutput(login + " hadoop-daemon.sh start datanode")  
  #print " datanode{} is configured".format(i)


######## hadoop-namenode #############################
def configNameNode(l):
   
  login="sudo {} docker exec namenode ".format(l)
  #javaInstall(login)
  #hadoopInstall(login)
  e=commands.getstatusoutput(login + "mkdir /pop")
  d=commands.getstatusoutput(login + " hadoop namenode -format -force ")  
  c=commands.getstatusoutput(login + " hadoop-daemon.sh start namenode")
 # print "namenode configured"
 









