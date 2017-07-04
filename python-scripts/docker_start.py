#!/usr/bin/python2

import commands
import cgi

print "content-type: text/html"


cName=cgi.FormContent()['x'][0]
login=" sshpass -p 12345 ssh -o stricthostkeychecking=no -l root 192.168.43.84"

dockerstartstatus=commands.getstatusoutput("sudo {} docker start {}".format(login,cName))

if dockerstartstatus[0]  == 0:
	print "location:  docker_manage.py"
	print
else:
	print "not removed"








