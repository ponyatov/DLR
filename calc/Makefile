log.log: src.src ./exe.exe
	/exe.exe < $< > $@ && tail $(TAIL) $@
C = cpp.cpp ypp.tab.cpp lex.yy.c
H = hpp.hpp ypp.tab.hpp lex.yy.h
L = -lreadline
./exe.exe: $(C) $(H)
	(CXX) $(CXXFLAGS) -o $@ $(C) $(L)
ypp.tab.cpp ypp.tab.hpp: ypp.ypp
	bison $<
lex.yy.c lex.yy.h: lpp.lpp
	flex $<
