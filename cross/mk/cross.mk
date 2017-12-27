.PHONY: cross
cross: binutils

# get number or CPU cores for build system
BUILD_CPU_NUMBER = $(shell grep processor /proc/cpuinfo | wc -l)
# parallel make
MAKE = make -j$(BUILD_CPU_NUMBER)

CROSS_CFG = --target=$(TARGET)
WITH_CCLIBS = --with-gmp=$(CROSS) --with-mpfr=$(CROSS) --with-mpc=$(CROSS)  

.PHONY: binutils
binutils: $(CROSS)/bin/$(TARGET)-as
$(CROSS)/bin/$(TARGET)-as: $(SRC)/$(BINUTILS)/README
	rm -rf $(BLD)/$(BINUTILS) ; mkdir $(BLD)/$(BINUTILS) ;\
	cd $(BLD)/$(BINUTILS) ; $(SRC)/$(BINUTILS)/$(CFG) \
		$(CROSS_CFG) --with-sysroot=$(ROOT) &&\
	$(MAKE) && make install-strip

.PHONY: gcc
gcc: $(CROSS)/bin/$(TARGET)-gcc
$(CROSS)/bin/$(TARGET)-gcc: $(SRC)/$(GCC)/README
	rm -rf $(BLD)/$(GCC) ; mkdir $(BLD)/$(GCC) ;\
	cd $(BLD)/$(GCC) ; $(SRC)/$(GCC)/$(CFG) \
		$(CROSS_CFG) $(WITH_CCLIBS)

.PHONY: gcclibs
gcclibs: gmp mpfr mpc

CCLIBS_CFG = --disable-shared $(WITH_CCLIBS)

.PHONY: gmp
gmp: $(CROSS)/lib/libgmp.a
$(CROSS)/lib/libgmp.a: $(SRC)/$(GMP)/README
	rm -rf $(BLD)/$(GMP) ; mkdir $(BLD)/$(GMP) ;\
	cd $(BLD)/$(GMP) ; $(SRC)/$(GMP)/$(CFG) $(CCLIBS_CFG) &&\
	$(MAKE) && make install-strip
 
.PHONY: mpfr
mpfr: $(CROSS)/lib/libmpfr.a
$(CROSS)/lib/libmpfr.a: $(SRC)/$(MPFR)/README
	rm -rf $(BLD)/$(MPFR) ; mkdir $(BLD)/$(MPFR) ;\
	cd $(BLD)/$(MPFR) ; $(SRC)/$(MPFR)/$(CFG) $(CCLIBS_CFG) &&\
	$(MAKE) && make install-strip

.PHONY: mpc
mpc: $(CROSS)/lib/libmpc.a
$(CROSS)/lib/libmpc.a: $(SRC)/$(MPC)/README
	rm -rf $(BLD)/$(MPC) ; mkdir $(BLD)/$(MPC) ;\
	cd $(BLD)/$(MPC) ; $(SRC)/$(MPC)/$(CFG) $(CCLIBS_CFG) &&\
	$(MAKE) && make install-strip
