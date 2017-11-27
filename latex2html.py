# latex2html dows not works for me,
# this is homebrew "crutches and bicycles" converter

# implemented using Victor Eijkhout's LaTeX implementation manual: 
# https://bitbucket.org/VictorEijkhout/the-science-of-tex-and-latex/downloads/TeXLaTeXcourse.pdf

# using http://www.yattag.org/ html template generator
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
	about = 'Rich manual and support library for writing dynamic script languages'
	author = '(c) Dmitry Ponyatov &lt;<a href="mailto:dponyatov@gmail.com" style="text-decoration: none">dponyatov@gmail.com</a>&gt; , GNU LesserGPL, 2017'
	toc = []
	id = 0

class T2H:
	lst = True
	def __init__(self,src):
		DOM.pre += '\n<!-- %s -->\n\n'%src
		# lexer
		tokens = ['CHAR']
 		t_ignore = ''
 		def t_ignore_COMMENT(t): r'%.*'
 		def t_ignore_notused(t):
 			r'\\(clearpage|tableofcontents|maketitle|noindent|normalfont)\n*'
 		def t_ignore_usepakage(t):
 			r'\\(documentclass|usepackage)(\[[^\]]+\])?{.+?}\n*'
 		def t_ignore_newcommand(t):
 			r'\\(re)?newcommand{.+?}(\[.+\])?{.+?}'
 		def t_INPUT(t):
 			r'\\input{([a-zA-Z]+)}'
 			fname = t.value.split('{')[-1][:-1]+'.tex'
 			if fname != 'header.tex': 
 			 	T2H(fname) # recurse
 		def t_label(t):
 			r'\\label{.+?}'
 			T = re.findall(r'{(.+)}',t.value)[0]
 			DOM.pre += '<A NAME="%s">'%T
 		def t_ref(t):
 			r'\\ref{.+?}'
 			T = re.findall(r'{(.+)}',t.value)[0]
 			DOM.pre += ' /<A HREF="#%s"><sup>%s</sup></A>/'%(T,T)
 		def t_url(t):
 			r'\\url{.+?}'
 			T = re.findall(r'{(.+)}',t.value)[0]
 			DOM.pre += ' <A HREF="%s">%s</A>'%(T,T)
 		def t_href(t):
 			r'\\href{.+?}{.+?}'
  			H,T = re.findall(r'{(.+?)}',t.value)[:2]
  			if T != '#1':
  			 	DOM.pre += ' <A HREF="%s">%s</A>'%(H,T)
 		def t_email(t):
 			r'\\email{.+?}'
 			T = re.findall(r'{(.+)}',t.value)[0]
 			DOM.pre += ' &lt;<A HREF="mailto:%s">%s</A>&gt;'%(T,T)
 		def t_verb(t):
 			r'\\verb\|.+?\|'
 			T = re.findall(r'\|(.+)\|',t.value)[0]
 			DOM.pre += ' <code>%s</code>'%T
 		def t_descr_begin(t):
 			r'\\begin{(description|itemize)}(\[nosep\])?'
 			DOM.pre += '<ul>'
 		def t_descr_end(t):
 			r'\\end{(description|itemize)}'
 			DOM.pre += '</ul>'
 		def t_bib_begin(t):
 		 	r'\\begin{thebibliography}({.+})?\n*'
 			DOM.pre += '<ul>'
 		def t_bib_end(t):
 		 	r'\\end{thebibliography}\n*'
 			DOM.pre += '</ul>'
 		def t_bib_toc(t):
 			r'\\addcontentsline[^\n]+\n*'
 		def t_bib_item(t):
 			r'\\bibitem{.+?}'
 			T = re.findall(r'{(.+)}',t.value)[0]
 			DOM.pre += '<li style="margin-bottom: 10px;">'
 			DOM.pre += '<a name="%s">[<a href="#%s">%s</a>] '%(T,T,T)
 		def t_bib_cite(t):
 			r'\\cite{.+?}'
 			T = re.findall(r'{(.+)}',t.value)[0]
 			DOM.pre += ' [<a href="#%s">%s</a>] '%(T,T)
 		def t_item(t):
 			r'\\item'
 			DOM.pre += '<li> '
 		def t_appendix(t):
 			r'\\(begin|end){appendices}\n*'
		def t_bigskip(t):
			r'\\bigskip'
			DOM.pre += '<p>'
 		def t_emph(t):
 			r'\\emph{.+?}'
 			T = re.findall(r'{(.+)}',t.value)[0]
 			DOM.pre += ' <b>%s</b>'%T 
 		def t_textit(t):
 			r'\\textit{.+?}'
 			T = re.findall(r'{(.+)}',t.value)[0]
 			DOM.pre += ' <i>%s</i>'%T 
 		def t_TITLE(t):
 			r'\\title{.+?}'
 			DOM.title = re.findall(r'{(.+)}',t.value)[0]
#  			DOM.pre += t.value
 		def t_section(t):
 			r'\\(part|chapter|section){.+?}'
 			title = re.findall(r'{(.+)}',t.value)[0]
 			DOM.toc.append('<a href="#%s">%s</a>'%(DOM.id,title))
			DOM.pre += '<H1>%s</H1><A NAME="%s">'%(title,DOM.id)
			DOM.id += 1
 		def t_lst_file(t):
			r'\\lstinputlisting(\[.+?\])?{.+?}'
 			fname = re.findall(r'{(.+)}',t.value)[-1]
			DOM.pre += '<pre  style="border:1px solid Black;">'
			DOM.pre += open(fname).read() 
			DOM.pre += '</pre>'
 		def t_lst_begin(t):
			r'\\begin{lstlisting}(\[.+?\])?'
			DOM.pre += '<pre style="border:1px solid Black;">'
			self.lst = True
 		def t_lst_end(t):
			r'\\end{lstlisting}'
			DOM.pre += "</pre>"
			self.lst = False
 		def t_doc_begin(t):
			r'\\begin{document}'
			self.lst = True
 		def t_doc_end(t):
			r'\\end{document}'
		def t_space(t):
			r'\\\s'
			DOM.pre += ' ' 			
		def t_cr(t):
			r'\\\\'
			DOM.pre += '<br>'
		def t_par(t):
			r'\n{2,}'
			if self.lst:
				DOM.pre += t.value
			else:
				DOM.pre += '\n'
		def t_nl(t):
			r'\n'
			if self.lst:
				DOM.pre += t.value
			else:
				DOM.pre += ' '
		def t_less(t):
			r'\<'
			DOM.pre += '&lt;'
		def t_more(t):
			r'\>'
			DOM.pre += '&gt;'
 		def t_CHAR(t):
 			r'.'
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

with tag('HTML'):
	with tag('HEAD'):
 		with tag('TITLE'):
 			text(DOM.title)
	with tag('BODY'):
		with tag('H1'):
			text(DOM.title)
		with tag('H2'):
			text(DOM.about)
		with tag('P'):
			doc.asis(DOM.author)
		with tag('table'):#,style='list-style: none'):
			with tag('tr'):
				with tag('td'):
					line('b','github:')
				with tag('td'):
					line('a','https://github.com/ponyatov/DLR',href='https://github.com/ponyatov/DLR')
			with tag('tr'):
				with tag('td'):
					line('b','PDF for mobile:')
				with tag('td'):
					line('a','https://github.com/ponyatov/DLR/releases/latest',href='https://github.com/ponyatov/DLR/releases/latest')
			with tag('tr'):
				with tag('td'):
					line('b','online manual (preview):')
				with tag('td'):
					line('a','http://ponyatov.github.io/DLR/',href='http://ponyatov.github.io/DLR/')
		with tag('p'):
			doc.asis('''
I have some troubles with <code>latex2html</code> converter, so HTML version only for
preview, download full .pdf with working links, adapted for reading on mobile
devices and slide projectors.
''')
		doc.stag('HR')
		with tag('ul'):
			for i in DOM.toc:
				doc.asis('<li>%s</li>'%i)
		doc.stag('HR')
# 		with tag('PRE'):
		doc.asis(DOM.pre)

print >>open('docs/index.html','w'),doc.getvalue() # yattag.indent(doc.getvalue())
