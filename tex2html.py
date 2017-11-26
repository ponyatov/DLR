# latex2html dows not works for me,
# this is homebrew "crutches and bicycles" converter

# implemented using Victor Eijkhout's LaTeX implementation manual: 
# https://bitbucket.org/VictorEijkhout/the-science-of-tex-and-latex/downloads/TeXLaTeXcourse.pdf

# using http://www.yattag.org/
import yattag
doc,tag,text,line = yattag.Doc().ttl()

pre = ''

import os,sys,re

os.chdir('doc')

# import PLY parser library

import ply.lex  as lex
import ply.yacc as yacc

class DOM:
	pre = ''

class T2H:
	def __init__(self,src):
		DOM.pre += '\n<!-- %s -->\n\n'%src
		# lexer
		tokens = ['CHAR']
 		t_ignore = ''
 		def t_ignore_COMMENT(t): r'%.*'
 		def t_INPUT(t):
 			r'\\input{([a-z]+)}'
 			T2H(t.value.split('{')[-1][:-1]+'.tex') # recurse
 		def t_TITLE(t):
 			r'\\title{.+?}'
 			DOM.title = re.findall(r'{(.+)}',t.value)[0]
 			DOM.pre += t.value
 		def t_CHAR(t):
 			r'.|\n'
 			return t
		def t_error(t): raise SyntaxError(t)
		lexer = lex.lex()
		# parser
		def p_tex_none(p): ' tex : '
		def p_tex_CHAR(p):
			' tex : tex CHAR '
			DOM.pre += p[2]
		def p_error(p): raise SyntaxError(p)
		parser = yacc.yacc(debug=False,write_tables=False)
		# process
		parser.parse(open(src).read(),lexer)

T2H('manual.tex')

os.chdir('..')

with tag('html'):
	with tag('head'):
 		with tag('title'):
 			text(DOM.title)
	with tag('body'):
		with tag('h1'):
			text(DOM.title)
		doc.asis('<hr>')
		with tag('pre'):
			text(DOM.pre)

print >>open('docs/index.html','w'),yattag.indent(doc.getvalue())
