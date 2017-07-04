#!/usr/bin/python2

import cgi
import os
import commands
print "content-type: text/html"
print

#print os.environ
data= os.environ['HTTP_COOKIE']


#print data
clientIP=cgi.FormContent()['cip'][0]
clientPass=cgi.FormContent()['cpass'][0]
#print clientIP
#print clientPass
count=(int(data.split(";")[2].split("=")[1]))
#print count
#count=int(data.split("=")[1])

#print"set-cookie: cip={}".format(clientIP)
#print"set-cookie: cpass={}".format(clientPass)

jIP=cgi.FormContent()['jip'][0]
jPass=cgi.FormContent()['jpass'][0]
#NDir=cgi.FormContent()['ndir'][0]
#print jIP
#print jPass
#print nIP
#print nPass
#print nDir

tIP=[]
tPass=[]
#dDir=cgi.FormContent()['ddir'][0]

i=1
while i <= int(count):
 tIP.append(cgi.FormContent()['tip{}'.format(i)][0])
 tPass.append(cgi.FormContent()['tpass{}'.format(i)][0])
# dDir.append(cgi.FormContent()['ddir{}'.format(i)][0])
#print i
 i=i+1


commands.getstatusoutput("sudo chown apache /etc/ansible/hosts")
fhhosts=open('/etc/ansible/hosts','w')
fhhosts.write('\n[job]\n{}\tansible_ssh_user=root\tansible_ssh_pass={}\n'.format(jIP,jPass))
fhhosts.write('\n[client]\n{}\tansible_ssh_user=root\tansible_ssh_pass={}\n'.format(clientIP,clientPass))
fhhosts.write('[task]\n')

j=1
while j <= count:
 fhhosts.write('{}\tansible_ssh_user=root\tansible_ssh_pass={}\n'.format(tIP[j-1],tPass[j-1]))
# print j
 j=j+1
fhhosts.close()
#print dIP[]
#print dPass
#print dDir

#nameIP="192.168.43.97"
#dataIP="1"
#nameDir="/name"
#dataDir="/test"

#core=('<?xml version="1.0"?>\n <?xml-stylesheet type="text/xsl" href="configuration.xsl"?>\n<configuration>\n<property>\n<name>fs.default.name</name>\n<value>hdfs://{0}:10001</value>\n</property>\n</configuration>'.format(nIP))

#commands.getstatusoutput("sudo touch /webcontent/tempdata/core.xml")
#commands.getstatusoutput("sudo chown apache /webcontent/tempdata/core.xml")
#corefh=open('/webcontent/tempdata/core.xml','w')
#corefh.write(core)
#corefh.close()

mapred=('<?xml version="1.0"?>\n<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>\n<configuration>\n<property>\n<name>mapred.job.tracker</name>\n<value>{}:9001</value>\n</property>\n</configuration>'.format(jIP))

commands.getstatusoutput("sudo touch /webcontent/tempdata/mapred.xml")
commands.getstatusoutput("sudo chown apache /webcontent/tempdata/mapred.xml")
mapredfh=open('/webcontent/tempdata/mapred.xml','w')
mapredfh.write(mapred)
mapredfh.close()





#hdfsdata=('<?xml version="1.0"?>\n<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>\n<configuration>\n<property>\n<name>dfs.data.dir</name>\n<value>{}</value>\n</property>\n</configuration>'.format(dDir))



#commands.getstatusoutput("sudo touch /webcontent/tempdata/hdfsdata.xml")
#commands.getstatusoutput("sudo chown apache /webcontent/tempdata/hdfsdata.xml")
#hdfsdatafh=open('/webcontent/tempdata/hdfsdata.xml','w')
#hdfsdatafh.write(hdfsdata)
#hdfsdatafh.close()






MapRed=("""---
 - hosts: all
   tasks:
    - name: "setting up core config files"
      copy:
        src: "/webcontent/tempdata/mapred.xml"
        dest: "/etc/hadoop/mapred-site.xml"


 - hosts: job
   tasks:
    - name: "setting up core config files"
      copy:
        src: "/webcontent/tempdata/core.xml"
        dest: "/etc/hadoop/core-site.xml"
    - name: "Starting job tracker service"
      command: "hadoop-daemon.sh start jobtracker"



 - hosts: task
   tasks:
    - name: "starting task tracker service"
      command: "hadoop-daemon.sh start tasktracker"
 
""")
commands.getstatusoutput("sudo touch /webcontent/ansible/mapred.yml")
commands.getstatusoutput("sudo chown apache /webcontent/ansible/mapred.yml")
hdfsAllfh=open('/webcontent/ansible/mapred.yml','w')
hdfsAllfh.write(MapRed)
hdfsAllfh.close()


commands.getstatusoutput("sudo ansible-playbook /webcontent/ansible/mapred.yml")

