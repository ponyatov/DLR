log.log bin.bin: src.src ./FVM.exe
	./FVM.exe < $< > $@ ; hexdump -C bin.bin >> $@ ; tail $(TAIL) $@
C = cpp.cpp ypp.tab.cpp lex.yy.c
H = hpp.hpp ypp.tab.hpp
CXXFLAGS += -std=gnu++11
./FVM.exe: $(C) $(H)
	$(CXX) $(CXXFLAGS) -o $@ $(C) $(L)
ypp.tab.cpp ypp.tab.hpp: ypp.ypp
	bison $<
lex.yy.c: lpp.lpp
	flex $<	
