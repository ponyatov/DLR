TEX = manual.tex header.tex bib.tex
TEX += intro.tex tutor.tex terminology.tex whylanguage.tex pypy.tex pyvm.tex
TEX += LLVM.tex SSA.tex
TEX += reference.tex
TEX += parsing.tex
TEX += Forth.tex
TEX += PLC.tex

SRC += *.py

FIG = ../tmp/lexer.pdf

LATEX = pdflatex -halt-on-error -output-directory ../tmp
manual.pdf: $(TEX) $(SRC) $(FIG)
	$(LATEX) manual && $(LATEX) manual && mv ../tmp/manual.pdf $@

../tmp/%.pdf: %.dot Makefile
	dot -Tpdf -o $@ $<
#	&& pdfcrop $@t $@
	inkscape $@ --export-area-drawing --export-pdf=$@
