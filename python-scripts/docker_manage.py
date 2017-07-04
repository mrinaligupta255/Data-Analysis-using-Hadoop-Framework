#!/usr/bin/python2


import commands

print "content-type: text/html"
print

print """
<script>
function start(mycname)
{
document.location='docker_start.py?x=' + mycname;
}
function stop(mycname)
{
document.location='docker_stop.py?x=' + mycname;
}
function lw(mycname)
{

document.location='docker_remove.py?x=' + mycname;

}
</script>
"""


print "<table border='5'>"
print "<tr><th>Image Name</th><th>ContainerName</th><th>Status</th><th>Stop</th><th>Start</th><th>Remove</th></tr>"

z=1
login=" sshpass -p 12345 ssh -o stricthostkeychecking=no -l root 192.168.43.84"
for i in commands.getoutput("sudo {} docker ps -a".format(login)).split('\n'):
	if z == 1:
		z+=1
		pass
	else:
		j=i.split()
		cStatus=commands.getoutput("sudo {} docker inspect {} | jq '.[].State.Status'".format(login,j[-1]))

		print "<tr><td>" + j[1] + "</td><td>" + j[-1] + "</td><td>" + cStatus +  "</td><td> <button  value="+j[-1]+" onclick=stop(this.value)>Stop</button>  </td><td> <button  value="+j[-1]+"  onclick=start(this.value) >Start</button></td><td>  <button value="+j[-1]+" onclick=lw(this.value)>Remove</button> </td></tr>"
	
print "</table>"











