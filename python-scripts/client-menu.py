#!/usr/bin/python2

import cgi
import commands
print "content-type: text/html"
print 


fileData=cgi.FormContent()['f'][0]

print commands.getstatusoutput("sudo touch /webcontent/upload/{}.csv".format('data'))
print commands.getstatusoutput("sudo chown apache /webcontent/upload/{}.csv".format('data'))
fh=open('/webcontent/upload/{}.csv'.format('data'),'w')
fh.write(fileData)
fh.close()


print commands.getstatusoutput("sudo sshpass -p 12345 scp -o stricthostkeychecking=no /webcontent/upload/data.csv  root@192.168.43.84:/webcontent/upload/data.csv ")

print commands.getstatusoutput("sudo sshpass -p 12345 ssh -o stricthostkeychecking=no -l root 192.168.43.84 hadoop fs -put /webcontent/upload/{}.csv  / ".format('data'))
print"File uploaded successfully"

