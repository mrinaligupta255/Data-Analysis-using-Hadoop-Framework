#!/usr/bin/python2
import commands
import cgi

print"content-type: text/html"
print

def config_files(ip_name,jobtracker_ip):
  core=('<?xml version="1.0"?>\n <?xml-stylesheet type="text/xsl" href="configuration.xsl"?>\n<configuration>\n<property>\n<name>fs.default.name</name>\n<value>hdfs://{0}:10001</value>\n</property>\n</configuration>'.format(ip_name))

  commands.getstatusoutput("sudo touch /webcontent/tempdata/core.xml")
  commands.getstatusoutput("sudo chown apache /webcontent/tempdata/core.xml")
  corefh=open('/webcontent/tempdata/core.xml','w')
  corefh.write(core)
  corefh.close()
	
  mapred_config=('<?xml version="1.0"?>\n<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n<property>\n<name>mapred.job.tracker</name>\n<value>{}:9001</value>\n</property>\n</configuration>\n'.format(jobtracker_ip))

  commands.getstatusoutput("sudo touch /webcontent/tempdata/mapred.xml")
  commands.getstatusoutput("sudo chown apache /webcontent/tempdata/mapred.xml")
  mapredfh=open('/webcontent/tempdata/mapred.xml','w')
  mapredfh.write(mapred_config)
  mapredfh.close()


sys_ip=cgi.FormContent()['sys_ip'][0]
passwd=cgi.FormContent()['passwd'][0]
number_of_tasktrackers=cgi.FormContent()['node'][0]

login="sshpass -p {} ssh -o stricthostkeychecking=no -l root {}".format(passwd,sys_ip)

commands.getoutput("sudo {} systemctl start docker".format(login))

#a=commands.getstatusoutput("sudo {} docker inspect namenode".format(login))
#if a[0]==0:

jt=commands.getstatusoutput("sudo {0} docker run -dit -p 1235:50030 --name jobtracker overall:v3".format(login))

 
y=commands.getstatusoutput("sudo {} docker inspect jobtracker | jq '.[].NetworkSettings.Networks.bridge.IPAddress' ".format(login))     
jobtracker_ip=y[1].strip('"')

z=commands.getstatusoutput("sudo {} docker inspect namenode | jq '.[].NetworkSettings.Networks.bridge.IPAddress' ".format(login))     
ip_name=z[1].strip('"')


config_files(ip_name,jobtracker_ip)

commands.getoutput("sudo sshpass -p {} scp /webcontent/tempdata/core.xml {}:/webcontent/tempdata/core.xml".format(passwd,sys_ip))
commands.getoutput("sudo {} docker cp /webcontent/tempdata/core.xml jobtracker:/etc/hadoop/core-site.xml".format(login))
commands.getoutput("sudo sshpass -p {} scp /webcontent/tempdata/mapred.xml {}:/webcontent/tempdata/mapred.xml".format(passwd,sys_ip))
commands.getoutput("sudo {} docker cp /webcontent/tempdata/mapred.xml jobtracker:/etc/hadoop/mapred-site.xml".format(login))
commands.getoutput("sudo {} docker exec jobtracker hadoop-daemon.sh start jobtracker".format(login))

commands.getstatusoutput("sudo sshpass -p {} scp /webcontent/tempdata/mapred.xml {}:/etc/hadoop/mapred-site.xml".format(passwd,sys_ip))


no=int(number_of_tasktrackers)


for i in range(no):
  present=commands.getstatusoutput("sudo {} docker inspect datanode{}".format(login,i))
  if (present[0]==0):
    commands.getoutput("sudo sshpass -p {} scp /webcontent/tempdata/mapred.xml {}:/webcontent/tempdata/mapred.xml".format(passwd,sys_ip))
    commands.getoutput("sudo {} docker cp /webcontent/tempdata/mapred.xml datanode{}:/etc/hadoop/mapred-site.xml".format(login,i))
    commands.getoutput("sudo {} docker exec datanode{} hadoop-daemon.sh start tasktracker".format(login,i))

  else:
    tt=commands.getstatusoutput("sudo {} docker run -dit --name tasktracker{} overall:v3".format(login,i))
    commands.getoutput("sudo sshpass -p {} scp /webcontent/tempdata/mapred.xml {}:/webcontent/tempdata/mapred.xml".format(passwd,sys_ip))
    commands.getoutput("sudo {} docker cp /webcontent/tempdata/mapred.xml  tasktracker{}:/etc/hadoop/mapred-site.xml".format(login,i))
  
    commands.getoutput("sudo {} docker exec tasktracker{} hadoop-daemon.sh start tasktracker".format(login,i))



print "<a href=' ../autoform.html'>Click here to go back</a>"
print "<br/>"
print "<a href=' ../scripts/docker_manage.py'>Click to see conatiners</a>"
print "<br/>"
print "<a href=' http://192.168.43.84:1235'>Click to see MAP/REDUCE Report</a>"
