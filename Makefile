none: pdf

pdf:
	cd doc ; $(MAKE)

html:
	cd doc ; latex2html -dir $(CURDIR)/docs -no_footnode -local_icons \
		-address "GNU Dynamic Language Runtime" \
			manual.tex
