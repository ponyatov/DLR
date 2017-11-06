TEX = manual.tex header.tex bib.tex
TEX += intro.tex tutor.tex terminology.tex whylanguage.tex pypy.tex pyvm.tex
TEX += reference.tex
TEX += parsing.tex
TEX += Forth.tex
TEX += PLC.tex

SRC += py*.py

LATEX = pdflatex -halt-on-error -output-directory ../tmp
manual.pdf: $(TEX) $(SRC)
	$(LATEX) manual && $(LATEX) manual && mv ../tmp/manual.pdf $@
