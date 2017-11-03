none: 

html:
	cd doc ; latex2html -dir $(CURDIR)/docs -no_footnode \
		-address "GNU Dynamic Language Runtime" \
			manual.tex
