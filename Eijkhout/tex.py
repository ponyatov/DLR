# full size TeX translator using Eijkhout's manual @ doc/

# using http://www.yattag.org/ html template generator
import yattag
doc,tag,text,line = yattag.Doc().ttl()

import os,sys,re

with tag('html'):
	with tag('head'):
		with tag('style',media="all",type="text/css"):
			# https://stackoverflow.com/questions/3341485/how-to-make-a-html-page-in-a4-paper-size-pages
			text('''
				@page { /* e-book optimized for mobile phone reading */
	    			size: 118.8mm 68.2mm;
    				margin: 2mm 2mm 2mm 2mm;
				}
			''')
	with tag('body'):
		text('Hello')

open('html.html','w').write(yattag.indent(doc.getvalue()))