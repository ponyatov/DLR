none: html

html:
	cd doc ; latex2html -dir $(CURDIR)/docs manual.tex
