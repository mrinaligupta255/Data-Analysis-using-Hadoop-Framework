#!/usr/bin/python2
import commands
import hadoopsetup
import cgi

print"content-type: text/html"
print

def config_files(ip_name):
	core=('<?xml version="1.0"?>\n <?xml-stylesheet type="text/xsl" href="configuration.xsl"?>\n<configuration>\n<property>\n<name>fs.default.name</name>\n<value>hdfs://{0}:10001</value>\n</property>\n</configuration>'.format(ip_name))

	commands.getstatusoutput("sudo touch /webcontent/tempdata/core.xml")
	commands.getstatusoutput("sudo chown apache /webcontent/tempdata/core.xml")
	corefh=open('/webcontent/tempdata/core.xml','w')
	corefh.write(core)
	corefh.close()

	hdfsname=('<?xml version="1.0"?>\n<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>\n<configuration>\n<property>\n<name>dfs.name.dir</name>\n<value>{}</value>\n</property>\n</configuration>'.format("/pop"))

	commands.getstatusoutput("sudo touch /webcontent/tempdata/hdfsname.xml")
	commands.getstatusoutput("sudo chown apache /webcontent/tempdata/hdfsname.xml")
	hdfsnamefh=open('/webcontent/tempdata/hdfsname.xml','w')
	hdfsnamefh.write(hdfsname)
	hdfsnamefh.close()

	hdfsdata=('<?xml version="1.0"?>\n<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>\n<configuration>\n<property>\n<name>dfs.data.dir</name>\n<value>{}</value>\n</property>\n</configuration>'.format("/pop"))

	commands.getstatusoutput("sudo touch /webcontent/tempdata/hdfsdata.xml")
	commands.getstatusoutput("sudo chown apache /webcontent/tempdata/hdfsdata.xml")
	hdfsdatafh=open('/webcontent/tempdata/hdfsdata.xml','w')
	hdfsdatafh.write(hdfsdata)
	hdfsdatafh.close()  


ip_data=[]
sys_ip=cgi.FormContent()['sys_ip'][0]
passwd=cgi.FormContent()['passwd'][0]
node=cgi.FormContent()['node'][0]
size=cgi.FormContent()['size'][0]
login="sshpass -p {} ssh -o stricthostkeychecking=no -l root {}".format(passwd,sys_ip)

print commands.getoutput("sudo {} systemctl start docker".format(login))
print commands.getstatusoutput("sudo {} docker rm -f $(docker ps -qa) ".format(login))
print commands.getstatusoutput("sudo {} docker run -dit  -p 1234:50070 --privileged=true  --name namenode  overall:v3".format(login))
y=commands.getstatusoutput("sudo {} docker inspect namenode | jq '.[].NetworkSettings.Networks.bridge.IPAddress' ".format(login))     
ip_name=y[1].strip('"')
  
config_files(ip_name)
commands.getoutput("sudo sshpass -p {} scp /webcontent/tempdata/core.xml {}:/webcontent/tempdata/core.xml".format(passwd,sys_ip))
commands.getoutput("sudo sshpass -p {} scp /webcontent/tempdata/core.xml {}:/etc/hadoop/core-site.xml".format(passwd,sys_ip))
commands.getoutput("sudo {} docker cp /webcontent/tempdata/core.xml namenode:/etc/hadoop/core-site.xml".format(login))
commands.getoutput("sudo sshpass -p {} scp /webcontent/tempdata/hdfsname.xml {}:/webcontent/tempdata/hdfsname.xml".format(passwd,sys_ip))
commands.getoutput("sudo {} docker cp /webcontent/tempdata/hdfsname.xml namenode:/etc/hadoop/hdfs-site.xml".format(login))
hadoopsetup.configNameNode(login)
node=int(node)
for i in range(node):
  commands.getoutput("sudo {} lvcreate --size {}G --name lv{} myvg ".format(login,size,i))
  commands.getoutput("sudo {} mkfs.ext4 /dev/myvg/lv{} ".format(login,i))
  commands.getstatusoutput("sudo {} mkdir -p /dockermount/lv{}".format(login,i))
  commands.getstatusoutput("sudo {0} mount /dev/myvg/lv{1} /dockermount/lv{1} ".format(login,i))
  
  c=commands.getstatusoutput("sudo {0} docker run -dit  -v /dockermount/lv{1}:/pop  --privileged=true --name datanode{1}  overall:v3".format(login,i))
  commands.getoutput("sudo sshpass -p {} scp /webcontent/tempdata/core.xml {}:/webcontent/tempdata/core.xml".format(passwd,sys_ip))
  commands.getoutput("sudo {} docker cp /webcontent/tempdata/core.xml datanode{}:/etc/hadoop/core-site.xml".format(login,i))
  commands.getoutput("sudo sshpass -p {} scp /webcontent/tempdata/hdfsdata.xml {}:/webcontent/tempdata/hdfsdata.xml".format(passwd,sys_ip))
  commands.getoutput("sudo {} docker cp /webcontent/tempdata/hdfsdata.xml datanode{}:/etc/hadoop/hdfs-site.xml".format(login,i))
  y=commands.getstatusoutput(" sudo {} docker inspect datanode{} | jq '.[].NetworkSettings.Networks.bridge.IPAddress' ".format(login,i)) 
  ip_data.append(y[1].strip('"')) 
  
  hadoopsetup.configDataNode(i,login)


print "<a href=' ../autoform.html'>Click here to go back</a>"
print "<br/>"
print "<a href=' ../scripts/docker_manage.py'>Click to see conatiners</a>"
print "<br/>"
print "<a href=' http://192.168.43.84:1234'>Click to see HDFS Report</a>"
