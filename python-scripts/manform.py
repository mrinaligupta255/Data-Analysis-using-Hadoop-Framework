#!/usr/bin/python2

import cgi
print"content-type: text/html"

x=cgi.FormContent()['man'][0]

#print"set-cookie: setup={}".format(x)

print "location: ../{}man.html".format(x)
print

