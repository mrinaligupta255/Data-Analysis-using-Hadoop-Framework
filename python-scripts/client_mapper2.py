#!/usr/bin/python2

import cgi
import commands
print "content-type: text/html"
print 
print '<a href="../client_mapper.html" >Click here to go back <a/>'
print '<br/>'
print '<br/>'
print "OUTPUT:\n"
fileName="mapper_db"
commands.getstatusoutput("sudo sshpass -p 12345 scp /webcontent/scripts/{0}.py 192.168.43.84:/webcontent/upload/{0}.py ".format(fileName))
fileName="reducer_lang"

commands.getstatusoutput("sudo sshpass -p 12345 scp /webcontent/scripts/{0}.py 192.168.43.84:/webcontent/upload/{0}.py ".format(fileName))
commands.getstatusoutput("sudo sshpass -p 12345 ssh -o stricthostkeychecking=no -l root 192.168.43.84 chmod +x /webcontent/upload/mapper_db.py")
commands.getstatusoutput("sudo sshpass -p 12345 ssh -o stricthostkeychecking=no -l root 192.168.43.84 chmod +x /webcontent/upload/reducer_lang.py")

commands.getstatusoutput("sudo sshpass -p 12345 ssh -o stricthostkeychecking=no -l root 192.168.43.84 hadoop jar  /usr/share/hadoop/contrib/streaming/hadoop-streaming-1.2.1.jar  -input /data.csv -mapper ./mapper_db.py  -file /webcontent/upload/mapper_db.py   -reducer ./reducer_lang.py -file /webcontent/upload/reducer_lang.py   -output /output2")
commands.getstatusoutput(" sudo sshpass -p 12345 ssh -o stricthostkeychecking=no -l root 192.168.43.84 rm /webcontent/upload/part-00000")
commands.getstatusoutput(" sudo sshpass -p 12345 ssh -o stricthostkeychecking=no -l root 192.168.43.84 hadoop fs -copyToLocal /output2/part-00000  /webcontent/upload/")
commands.getstatusoutput(" sudo  rm /webcontent/upload/part-00000")
commands.getstatusoutput(" sudo sshpass -p 12345 scp 192.168.43.84:/webcontent/upload/part-00000 /webcontent/upload/")
print '<pre>'+  commands.getoutput("sudo cat /webcontent/upload/part-00000") +'</pre>'
#print commands.getstatusoutput(" sudo cat /webcontent/upload/part-00000 | /webcontent/scripts/newplot.py")


print " Analysis Completed successfully"

