import sys
sys.dont_write_bytecode=True
from jinja2 import Template
import os
info = {"name":"mail", #--> this is what defines the app in the search query( "#plugin_name ..." ). 
	"author":"Mark Spurgeon",
	"version":"0.1"
	}

#Search event
def Search(query, color=None, size=None):
	#'query' is search query
	#'color' is the launcher's main color
	#'size' is the web page's size (never know if it's useful)
	
	###Do whatever you like
	#-------
	###like templating, etc...
	home=os.path.expanduser("~")
	s = str(open("{}/.duck-plugins/mail/index.html".format(home),"r").read())
	t=Template(s)
	return t.render(who=query)

#JS function events
def onFormSubmit(elements):
	for e in elements:
		if e.has_key("name") and e["name"]=="who":
			print e["value"]
def onDataSent(object, value):
	print "object '{0}' has changed its value to: {1}".format(object, value)