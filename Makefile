log.log: VM.py
	python $< > $@

DPANS94 = FORTH/doc/DPANS94.pdf
TEXIMPL = Eijkhout/Victor\ Eijkhout\ LaTeX\ implementation.pdf
PDFs = $(DPANS94) $(TEXIMPL)

doc: manual $(PDFs) forth Eijkhout/pdf.pdf

WGET = wget -c

$(DPANS94):
	$(WGET) -O "$@" https://www.openfirmware.info/data/docs/dpans94.pdf
$(TEXIMPL):
	$(WGET) -O "$@" http://bitbucket.org/VictorEijkhout/the-science-of-tex-and-latex/downloads/TeXLaTeXcourse.pdf

manual:
	cd doc ; $(MAKE)

html:
	python latex2html.py

forth: FORTH/bin.bin
FORTH/bin.bin:
	cd FORTH ; $(MAKE)

packages:
	sudo apt install make build-essential graphviz python2.7 texlive-latex-extra latex2html
	sudo pip install yattag

Eijkhout/pdf.pdf: 
	cd Eijkhout ; $(MAKE)
