#!/usr/bin/python2

import commands
import cgi

print "content-type: text/html"


cName=cgi.FormContent()['x'][0]
login=" sshpass -p 12345 ssh -o stricthostkeychecking=no -l root 192.168.43.84"

cremovestatus=commands.getstatusoutput("sudo {} docker rm -f {}".format(login,cName))

if cremovestatus[0]  == 0:
	print "location:  docker_manage.py"
	print
else:
	print "not removed"








