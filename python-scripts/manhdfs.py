#!/usr/bin/python2
import cgi

print "content-type: text/html"


count=cgi.FormContent()['mannohdfs'][0]
size=cgi.FormContent()['lvsize'][0]
#print count
print"set-cookie: c={}".format(count)
print"set-cookie: s={}".format(size)
print

i=1
print "<form action='hadoopmanfinal.py'>"
while i<=int(count):
 print"<b><i>Enter the ip of data node {0}</i></b><input type='text' name='dip{0}' />".format(i)
 print"<b><i>Enter the pass of data node{0}</i><b><input type='text' name='dpass{0}' />".format(i)
 print"<br />"
 print "</br>"
 i=i+1
print"<b><i>Enter the ip of NAME NODE</b></i><input type='text' name='nip' />"
print"<b><i>Enter the password of NAME NODE</b></i><input type='text' name='npass' />"
print "</br>"
print "</br>"
print"<b><i>Enter the directory of name node</b></i><input type='text' name=ndir />"
print "</br>"
print "</br>"
print"<b><i>Enter the directory of data node</b></i><input type='text' name='ddir' />"
print "</br>"
print "</br>"
print"<b><i>Enter the ip of Client</b></i><input type='text' name='cip' />"
print"<b><i>Enter the password of Client</b></i><input type='text' name='cpass' />"
print "</br>"
print "</br>"
print "<input type='submit' value='Submit' />"


print"</form>"

