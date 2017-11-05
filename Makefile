doc: manual FORTH/doc/dpans94.pdf forth

WGET = wget -c

FORTH/doc/dpans94.pdf:
	$(WGET) -O $@ https://www.openfirmware.info/data/docs/dpans94.pdf

manual:
	cd doc ; $(MAKE)

html:
	cd doc ; latex2html -dir $(CURDIR)/docs -no_footnode -local_icons \
		-address "GNU Dynamic Language Runtime" \
			manual.tex

forth: FORTH/bin.bin
	cd FORTH ; $(MAKE)
