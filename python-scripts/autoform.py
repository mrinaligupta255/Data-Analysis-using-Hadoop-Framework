#!/usr/bin/python2

import cgi
print"content-type: text/html"

x=cgi.FormContent()['auto'][0]

#print"set-cookie: setup={}".format(x)

print "location: ../{}auto.html".format(x)
print

