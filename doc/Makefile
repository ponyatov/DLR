TEX = manual.tex header.tex bib.tex
TEX += intro.tex tutor.tex terminology.tex whylanguage.tex pypy.tex pyvm.tex
TEX += LLVM.tex SSA.tex
TEX += reference.tex
TEX += inference.tex
TEX += parsing.tex plyass.tex calc.tex
TEX += GUI.tex TUI.tex
TEX += java.tex
TEX += Forth.tex asmforth.tex Forth.sty
TEX += PLC.tex
TEX += vim.tex cross.tex

SRC += ../tmp/calc.mk ../inher.py

FIG = ../tmp/lexer.pdf
FIG += ../tmp/cross_00.pdf ../tmp/cross_01.pdf ../tmp/cross_02.pdf
FIG += ../tmp/cross_03.pdf ../tmp/cross_04.pdf 
FIG += ../tmp/cross_05.pdf ../tmp/cross_06.pdf
FIG += ../tmp/cross_07.pdf ../tmp/cross_08.pdf ../tmp/cross_09.pdf
FIG += ../tmp/cross_10.pdf

TEX += generics.tex
FIG += ../tmp/sym_00.pdf ../tmp/sym_01.pdf ../tmp/sym_02.pdf
FIG += ../tmp/sym_03.pdf ../tmp/sym_04.pdf ../tmp/sym_05.pdf

#BRANCH = $(shell git symbolic-ref -q HEAD | sed -r -e "s|refs/heads/||")
NOW = $(shell date +%y%m%d)
RELEASE = DLR_$(NOW)
#_$(BRANCH)

LATEX = pdflatex -halt-on-error -output-directory ../tmp
../tmp/work.pdf: work.tex $(TEX) $(SRC) $(FIG) ../tmp/tex.tex
	$(LATEX) $< && $(LATEX) $< 
	
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

../tmp/cross_%.pdf: cross/%.dot
	dot -Tpdf -o $@ $<
#	&& pdfcrop $@t $@
	inkscape $@ --export-area-drawing --export-pdf=$@

../tmp/sym_%.pdf: sym/%.dot
	dot -Tpdf -o $@ $<
#	&& pdfcrop $@t $@
	inkscape $@ --export-area-drawing --export-pdf=$@

../tmp/calc.mk: ../calc/Makefile
	cp $< $@
