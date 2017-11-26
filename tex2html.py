# latex2html dows not works for me,
# this is homebrew "crutches and bicycles" converter

import os,sys,re

os.chdir('doc')

src = open('manual.tex')

html = '<html><title><title/></title>\n\n'
html += '<H1><title/></H1><p>\n'
html += '<H1><author/></H1><P>\n'
html += '<hr><pre>\n'

# import PLY parser library

import ply.lex  as lex
import ply.yacc as yacc

class T2H:
	def __init__(self,src):
		def braks(s): return re.findall(r'{(.+)}',s)[0]
		global html ; html += '\n<!-- %s -->\n'%src
		# lexer
		tokens = ['CHAR','INPUT','DROPPED','PART','CHAPTER','SECTION',
				'TITLE','AUTHOR']
		def t_ignore_COMMENT(t): r'\%.*\n'
		def t_INPUT(t):
			r'\\input{.+?}'
			T2H(braks(t.value)+'.tex') # recurse parser
		def t_PART(t):
			r'\\part{.+?}'
			t.value = braks(t.value) ; return t 
		def t_CHAPTER(t):
			r'\\chapter{.+?}'
			t.value = braks(t.value) ; return t 
		def t_SECTION(t):
			r'\\section{.+?}'
			t.value = braks(t.value) ; return t 
		def t_TITLE(t):
			r'\\title{.+?}'
			t.value = braks(t.value) ; return t 
		def t_AUTHOR(t):
			r'\\author{.+?}'
			t.value = braks(t.value) ; return t 
		def t_DROPPED(t): r'\\clearpage'
		def t_CHAR(t):
			r'.|\n'
			return t
		def t_error(t): raise SyntaxError('lexer:%s'%t)
		lexer = lex.lex()
		# parser
		def p_tex_none(p): ' tex : '
		def p_DROPPED(p): ' tex : tex DROPPED'
		def p_INPUT(p):
			' tex : tex INPUT'
			global html ; html += p[2]+'.html'
		def p_PART(p):
			' tex : tex PART '
			global html ; html += '<H1>%s</H1>\n' % p[2]
		def p_CHAPTER(p):
			' tex : tex CHAPTER '
			global html ; html += '<H2>%s</H2>\n' % p[2]
		def p_SECTION(p):
			' tex : tex SECTION '
			global html ; html += '<H3>%s</H3>\n' % p[2]
		def p_TITLE(p):
			' tex : tex TITLE '
			global html ; html = html.replace('<title/>',p[2])
		def p_AUTHOR(p):
			' tex : tex AUTHOR '
			global html ; html = html.replace('<author/>',p[2])
		def p_CHAR(p):
			' tex : tex CHAR'
			global html ; html += p[2]
		def p_error(p): raise SyntaxError('parser:%s'%p)
		parser = yacc.yacc(debug=False,write_tables=False)
		# process
		parser.parse(open(src).read(),lexer)

T2H('manual.tex')

os.chdir('..')

html += '</pre></html>\n'

print >>open('docs/index.html','w'),html
