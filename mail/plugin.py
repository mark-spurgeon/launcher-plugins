import sys
sys.dont_write_bytecode=True
from jinja2 import Template
import os
def Search(query, color=None,font=None):
	cwd="/usr/share/duck-launcher/plugins/mail/"
	s = str(open("{}mail.html".format(cwd),"r").read())
	t=Template(s)
	return t.render(who=query)
