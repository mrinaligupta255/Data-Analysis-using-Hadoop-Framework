#!/usr/bin/python2

import cgi
import commands
print "content-type: text/html"
print

mapp=cgi.FormContent()['mapper'][0]
red=cgi.FormContent()['reducer'][0]
#print mapp 
#print red
print commands.getstatusoutput("sudo touch /webcontent/tempdata/custommapper.py")
print commands.getstatusoutput("sudo chown apache /webcontent/tempdata/custommapper.py")
fhmap=open('/webcontent/tempdata/custommapper.py','w')
fhmap.write(mapp)
fhmap.close()
commands.getstatusoutput("sudo chmod +x /webcontent/tempdata/custommapper.py")
commands.getstatusoutput("sudo sshpass -p 12345 scp /webcontent/tempdata/custommapper.py 192.168.43.84:/webcontent/scripts/")



commands.getstatusoutput("sudo touch /webcontent/tempdata/customreducer.py")
commands.getstatusoutput("sudo chown apache /webcontent/tempdata/customreducer.py")
fhred=open('/webcontent/tempdata/customreducer.py','w')
fhred.write(red)
fhred.close()
commands.getstatusoutput("sudo chmod +x /webcontent/tempdata/customreducer.py")
commands.getstatusoutput("sudo sshpass -p 12345 scp /webcontent/tempdata/customreducer.py 192.168.43.84:/webcontent/scripts/")
