import sys
from jinja2 import Template
import os
import webbrowser
import urllib2
try:
	import simplejson as json
except ImportError:
	import json
from Crypto.Cipher import AES
def get_from_query(stuff,sec_key):
	try:
		if stuff=="":
			u = urllib2.urlopen("http://content.guardianapis.com/search?api-key={}&page-size=20".format(sec_key).replace(" ","+"))
		else:
			u = urllib2.urlopen("http://content.guardianapis.com/search?q={0}&api-key={1}&page-size=20".format(stuff,sec_key).replace(" ","+"))
		d = json.loads(u.read())
		u.close()
		r = d["response"]
		'''
		res= r["results"]
		for i, r in enumerate(res):
			print i,  r["webTitle"]
			print r["sectionName"]
			art={}
			art["title"]=r["webTitle"]
			print r["thumbnail"]
		'''
		all_articles=[]
		for a in r["results"]:
			info_url=a["apiUrl"]+"?show-fields=headline,thumbnail&api-key={}".format(sec_key)
			if 1==1:
				i = urllib2.urlopen(info_url)
				d=json.loads(i.read())
				i.close()
				art={}
				art["title"]=d["response"]["content"]["fields"]["headline"]
				try:
					art["thumbnail"]=d["response"]["content"]["fields"]["thumbnail"]
				except KeyError:
					art["thumnail"]=""
				try:
					art["section"]=d["response"]["content"]["sectionName"]
				except KeyError:
					art["section"]="Unknown"
				try:
					art["url"]=d["response"]["content"]["webUrl"]
				except KeyError:
					art["url"]="theguardian.com"
				try:
					date = d["response"]["content"]["webPublicationDate"]
					art["date"]=date
				except KeyError:
					art["date"]="Not now"
				all_articles.append(art)
		return all_articles
	except urllib2.URLError:
		print sys.exc_info()[0]
		return None
	except urllib2.HTTPError:
		print sys.exc_info()[0]
		return None
	#returns [{'title':'..', 'url':'..','thumbnail':'..','section':'..',}]
def Search(query, color=None,font=None):
	static="/usr/share/duck-launcher/plugins/guardian/"
	pub_key="9seAj(o!>5*m4P19"
	obj2 = AES.new(pub_key, AES.MODE_CBC, 'This is an IV456')
	ciphertext=open("{}sec_key.txt".format(static),"r")
	sec_key= obj2.decrypt(ciphertext.read()).replace("87654321","")
	ciphertext.close()
	s = str(open("{}guardian.html".format(static),"r").read())
	q=get_from_query(query,sec_key)
	t=Template(s)
	return t.render(articles=q,color=color,font=font,static="file://{}".format(static))
