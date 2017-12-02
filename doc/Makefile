TEX = manual.tex header.tex bib.tex
TEX += intro.tex tutor.tex terminology.tex whylanguage.tex pypy.tex pyvm.tex
TEX += LLVM.tex SSA.tex
TEX += reference.tex
TEX += parsing.tex plyass.tex calc.tex
TEX += GUI.tex TUI.tex
TEX += Forth.tex asmforth.tex Forth.sty
TEX += PLC.tex
TEX += vim.tex

SRC += ../tmp/calc.mk

FIG = ../tmp/lexer.pdf

LATEX = pdflatex -halt-on-error -output-directory ../tmp
../tmp/manual.pdf: $(TEX) $(SRC) $(FIG)
	$(LATEX) manual

pdf: $(TEX) $(SRC) $(FIG)
	$(LATEX) manual && $(LATEX) manual && cp ../tmp/manual.pdf $@

../tmp/%.pdf: %.dot Makefile
	dot -Tpdf -o $@ $<
#	&& pdfcrop $@t $@
	inkscape $@ --export-area-drawing --export-pdf=$@

../tmp/calc.mk: ../calc/Makefile
	cp $< $@
