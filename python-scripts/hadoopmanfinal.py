#!/usr/bin/python2

import cgi
import os
import commands

print "content-type: text/html"
print



#cookie=[]
#print os.environ
data= os.environ["HTTP_COOKIE"]		##solve cip cpass issue
print data

#x=data.split(";")
#print x
#for i in x:
# print a
# print i,x
# print b
# cookie.append(x[i].split("="))
#print c 
#print cookie






clientIP=cgi.FormContent()['cip'][0]
clientPass=cgi.FormContent()['cpass'][0]




size=(1024*int(data.split("=")[2]))
count=int(data.split("=")[1].split(";")[0])
#print size	
#print count

#print"set-cookie: cip={}".format(clientIP)
#print"set-cookie: cpass={}".format(clientPass)

#print clientIP
#print clientPass


nIP=cgi.FormContent()['nip'][0]
nPass=cgi.FormContent()['npass'][0]
nDir=cgi.FormContent()['ndir'][0]

#print nIP
#print nPass
#print nDir

dIP=[]
dPass=[]
dDir=cgi.FormContent()['ddir'][0]

i=1
while i <= int(count):
 dIP.append(cgi.FormContent()['dip{}'.format(i)][0])
 dPass.append(cgi.FormContent()['dpass{}'.format(i)][0])
# dDir.append(cgi.FormContent()['ddir{}'.format(i)][0])
#print i
 i=i+1

commands.getstatusoutput("sudo chown apache /etc/ansible/hosts")
fhhosts=open('/etc/ansible/hosts','w')
fhhosts.write('\n[name]\n{}\tansible_ssh_user=root\tansible_ssh_pass={}\n'.format(nIP,nPass))
fhhosts.write('\n[client]\n{}\tansible_ssh_user=root\tansible_ssh_pass={}\n'.format(clientIP,clientPass))
fhhosts.write('[data]\n')

j=1
while j <= count:
 fhhosts.write('{}\tansible_ssh_user=root\tansible_ssh_pass={}\n'.format(dIP[j-1],dPass[j-1]))
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

core=('<?xml version="1.0"?>\n <?xml-stylesheet type="text/xsl" href="configuration.xsl"?>\n<configuration>\n<property>\n<name>fs.default.name</name>\n<value>hdfs://{0}:10001</value>\n</property>\n</configuration>'.format(nIP))

commands.getstatusoutput("sudo touch /webcontent/tempdata/core.xml")
commands.getstatusoutput("sudo chown apache /webcontent/tempdata/core.xml")
corefh=open('/webcontent/tempdata/core.xml','w')
corefh.write(core)
corefh.close()

hdfsname=('<?xml version="1.0"?>\n<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>\n<configuration>\n<property>\n<name>dfs.name.dir</name>\n<value>{}</value>\n</property>\n</configuration>'.format(nDir))

commands.getstatusoutput("sudo touch /webcontent/tempdata/hdfsname.xml")
commands.getstatusoutput("sudo chown apache /webcontent/tempdata/hdfsname.xml")
hdfsnamefh=open('/webcontent/tempdata/hdfsname.xml','w')
hdfsnamefh.write(hdfsname)
hdfsnamefh.close()





hdfsdata=('<?xml version="1.0"?>\n<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>\n<configuration>\n<property>\n<name>dfs.data.dir</name>\n<value>{}</value>\n</property>\n</configuration>'.format(dDir))



commands.getstatusoutput("sudo touch /webcontent/tempdata/hdfsdata.xml")
commands.getstatusoutput("sudo chown apache /webcontent/tempdata/hdfsdata.xml")
hdfsdatafh=open('/webcontent/tempdata/hdfsdata.xml','w')
hdfsdatafh.write(hdfsdata)
hdfsdatafh.close()






HdfsAll=("""
---
 - hosts: all
   tasks:
    - name: "setting up core config files"
      copy:
        src: "/webcontent/tempdata/core.xml"
        dest: "/etc/hadoop/core-site.xml"



 - hosts: name
   tasks:
    - name: "setting up config files"
      copy:
        src: "/webcontent/tempdata/hdfsname.xml"
        dest: "/etc/hadoop/hdfs-site.xml"
      
    
    - name: "making directory"
      file:
        state: directory
        path: "{0}"

    - name: "Starting name node service"
      shell: "echo Y | hadoop namenode -format"

    - name: "Starting name node service"
      command: "hadoop-daemon.sh start namenode"


 - hosts: data
   tasks:
    - name: "setting up config files"
      copy:
        src: "/webcontent/tempdata/hdfsdata.xml"
        dest: "/etc/hadoop/hdfs-site.xml"
      
    - name: "making directory"
      file:
        state: directory
        path: "{1}"
    - name: "making lv"
      lvol:
        vg: myvg
        lv: projectlv
        size: {2}
        active: yes

    - filesystem:
       fstype: ext4
       dev: /dev/myvg/projectlv
    
    - name: mounting lv to data node
      mount:
       path: {3}
       src: /dev/myvg/projectlv
       fstype: ext4
       state: mounted

    - name: "Starting data node service"
      command: "hadoop-daemon.sh start datanode"
""".format(nDir,dDir,size,dDir))
commands.getstatusoutput("sudo touch /webcontent/ansible/hdfsAll.yml")
commands.getstatusoutput("sudo chown apache /webcontent/ansible/hdfsAll.yml")
hdfsAllfh=open('/webcontent/ansible/hdfsAll.yml','w')
hdfsAllfh.write(HdfsAll)
hdfsAllfh.close()


commands.getstatusoutput("sudo ansible-playbook /webcontent/ansible/hdfsAll.yml")
print"<h1>HDFS CLUSTER DEPLOYED SUCCESSFULLY</h1>"
print"<a href=' ../menuhadoop.html'>Click here to go to start page</a>"

