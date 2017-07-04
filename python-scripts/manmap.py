#!/usr/bin/python2

import cgi

print "content-type: text/html"

count=cgi.FormContent()['mannomap'][0]
#size=cgi.FormContent()['lvsize'][0]
#print count
print"set-cookie: t={}".format(count)
#print"set-cookie: s={}".format(size)
print

i=1
print "<form action='mapmanfinal.py'>"
while i<=int(count):
 print"<b><i>Enter ip of task tracker {0}</b></i><input type='text' name='tip{0}' />".format(i)
 print"<b><i>Enter the pass of task tracker{0}</b></i><input type='text' name='tpass{0}' />".format(i)
 print"<br />"
 print "</br>"
 i=i+1
print"<b><i>Enter the ip of JOB TRACKER</b></i><input type='text' name='jip' />"
print"<b><i>Enter the password of JOB TRACKER</b></i><input type='text' name='jpass' />"
print "</br>"
print "</br>"
#print"Enter the directory of name node<input type='text' name=ndir />"
#print"Enter the directory of data node<input type='text' name='ddir' />"
print"<b><i>Enter the ip of Client</b></i><input type='text' name='cip' />"
print"<b><i>Enter the password of Client</b></i><input type='text' name='cpass' />"
print "</br>"
print "</br>"
print "<input type='submit' value='Submit' />"

print"</form>"

