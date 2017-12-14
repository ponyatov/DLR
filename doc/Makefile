TEX = manual.tex header.tex bib.tex
TEX += intro.tex tutor.tex terminology.tex whylanguage.tex pypy.tex pyvm.tex
TEX += LLVM.tex SSA.tex
TEX += reference.tex
TEX += parsing.tex plyass.tex calc.tex
TEX += GUI.tex TUI.tex
TEX += java.tex
TEX += Forth.tex asmforth.tex Forth.sty
TEX += PLC.tex
TEX += vim.tex

SRC += ../tmp/calc.mk ../inher.py

FIG = ../tmp/lexer.pdf

BRANCH = $(shell git symbolic-ref -q HEAD | sed -r -e "s|refs/heads/||")
NOW = $(shell date +%d%m%y)
RELEASE = DLR_$(NOW)_$(BRANCH)

LATEX = pdflatex -halt-on-error -output-directory ../tmp
../tmp/manual.pdf: $(TEX) $(SRC) $(FIG) ../tmp/tex.tex
	$(LATEX) manual
	
../tmp/tex.tex: $(TEX) ../.git/HEAD Makefile
#	echo "\date{\scriptsize $(RELEASE)}" | sed -r "s|\_|\\\_|g" > ../tmp/tex.tex
	echo "\date{DLR\_$(NOW)}" > ../tmp/tex.tex

pdf: ../$(RELEASE).pdf
../$(RELEASE).pdf: manual.pdf
	cp $< $@
manual.pdf: $(TEX) $(SRC) $(FIG)
	$(LATEX) manual && $(LATEX) manual && cp ../tmp/manual.pdf $@

../tmp/%.pdf: %.dot
	dot -Tpdf -o $@ $<
#	&& pdfcrop $@t $@
	inkscape $@ --export-area-drawing --export-pdf=$@

../tmp/calc.mk: ../calc/Makefile
	cp $< $@
