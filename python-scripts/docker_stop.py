#!/usr/bin/python2

import commands
import cgi

print "content-type: text/html"


cName=cgi.FormContent()['x'][0]
login=" sshpass -p 12345 ssh -o stricthostkeychecking=no -l root 192.168.43.84"

dockerstopstatus=commands.getstatusoutput("sudo {} docker stop {}".format(login,cName))

if dockerstopstatus[0]  == 0:
	print "location:  docker_manage.py"
	print
else:
	print "Docker not stopped"








