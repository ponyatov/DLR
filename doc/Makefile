TEX = manual.tex header.tex bib.tex
TEX += intro.tex tutor.tex terminology.tex whylanguage.tex
TEX += reference.tex
TEX += Forth.tex

LATEX = pdflatex -halt-on-error -output-directory ../tmp
manual.pdf: $(TEX)
	$(LATEX) manual && $(LATEX) manual && mv ../tmp/manual.pdf $@
