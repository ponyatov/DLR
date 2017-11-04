TEX = manual.tex header.tex bib.tex
TEX += intro.tex tutor.tex terminology.tex whylanguage.tex
TEX += reference.tex
TEX += parsing.tex
TEX += Forth.tex
TEX += PLC.tex

LATEX = pdflatex -halt-on-error -output-directory ../tmp
manual.pdf: $(TEX)
	$(LATEX) manual && $(LATEX) manual && mv ../tmp/manual.pdf $@
