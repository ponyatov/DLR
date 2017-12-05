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
pdf:
	cd doc ; $(MAKE) pdf

html:
	python latex2html.py

forth: FORTH/bin.bin
FORTH/bin.bin:
	cd FORTH ; $(MAKE)

packages: ply/ply/lex.py
	sudo apt install \
		make build-essential \
		texlive-latex-extra graphviz \
		python2.7 python-wxgtk3.0 python-ply
	sudo pip install yattag
	
ply/ply/lex.py:
	git clone -o gh --depth=1 git@github.com:ponyatov/ply.git

Eijkhout/pdf.pdf: 
	cd Eijkhout ; $(MAKE)
