.PHONY: cross
cross: cclibs binutils gcc0

# get number or CPU cores for build system
BUILD_CPU_NUMBER = $(shell grep processor /proc/cpuinfo | wc -l)
# parallel make
MAKE = $(XPATH) make -j$(BUILD_CPU_NUMBER)

WITH_CCLIBS = --with-gmp=$(CROSS) --with-mpfr=$(CROSS) --with-mpc=$(CROSS)  
CROSS_CFG = --target=$(TARGET) $(WITH_CCLIBS) \
	--with-sysroot=$(ROOT) --with-native-system-header-dir=/include  

.PHONY: binutils
binutils: $(CROSS)/bin/$(TARGET)-as
$(CROSS)/bin/$(TARGET)-as: $(SRC)/$(BINUTILS)/README
	rm -rf $(TMP)/$(BINUTILS) ; mkdir $(TMP)/$(BINUTILS) ;\
	cd $(TMP)/$(BINUTILS) ; $(SRC)/$(BINUTILS)/$(CFG) $(CROSS_CFG) &&\
	$(MAKE) && make install-strip

GCC0_CFG = --disable-shared --disable-threads \
			--without-headers --with-newlib \
			--enable-languages="c"
.PHONY: gcc0
gcc0: $(SRC)/$(GCC)/README
	# configure
	rm -rf $(TMP)/$(GCC) ; mkdir $(TMP)/$(GCC) ;\
	cd $(TMP)/$(GCC) ; $(SRC)/$(GCC)/$(CFG) $(CROSS_CFG) $(GCC0_CFG)
	# build
	cd $(TMP)/$(GCC) ; $(MAKE) all-gcc && make install-gcc
	cd $(TMP)/$(GCC) ; $(MAKE) all-target-libgcc && make install-target-libgcc 

GCC_CFG = --enable-languages="c,c++,fortran" \
		--enable-shared --enable-threads --enable-libgomp
.PHONY: gcc
gcc: $(SRC)/$(GCC)/README $(CROSS)/bin/$(TARGET)-gcc
	# configure
	rm -rf $(TMP)/$(GCC) ; mkdir $(TMP)/$(GCC) ;\
	cd $(TMP)/$(GCC) ; $(SRC)/$(GCC)/$(CFG) $(CROSS_CFG) $(GCC_CFG)
	# build
	## gcc/g++
	cd $(TMP)/$(GCC) && $(MAKE) all-gcc
	cd $(TMP)/$(GCC) && $(MAKE) install-gcc
	## gcc libs
	cd $(TMP)/$(GCC) && $(MAKE) all-target-libgcc
	cd $(TMP)/$(GCC) && $(MAKE) install-target-libgcc
	## g++ libs
	cd $(TMP)/$(GCC) && $(MAKE) all-target-libstdc++-v3
	cd $(TMP)/$(GCC) && $(MAKE) install-target-libstdc++-v3
	## fortran (need for for some numerical libs build)
	cd $(TMP)/$(GCC) && $(MAKE) all-target-libgfortran
	cd $(TMP)/$(GCC) && $(MAKE) install-target-libgfortran	
	
.PHONY: cclibs
cclibs: gmp mpfr mpc

GCCLIBS_CFG = --disable-shared $(WITH_CCLIBS)

.PHONY: gmp
gmp: $(CROSS)/lib/libgmp.a
$(CROSS)/lib/libgmp.a: $(SRC)/$(GMP)/README
	rm -rf $(TMP)/$(GMP) ; mkdir $(TMP)/$(GMP) ;\
	cd $(TMP)/$(GMP) ; $(SRC)/$(GMP)/$(CFG) $(GCCLIBS_CFG) &&\
	$(MAKE) && make install-strip
 
.PHONY: mpfr
mpfr: $(CROSS)/lib/libmpfr.a
$(CROSS)/lib/libmpfr.a: $(SRC)/$(MPFR)/README
	rm -rf $(TMP)/$(MPFR) ; mkdir $(TMP)/$(MPFR) ;\
	cd $(TMP)/$(MPFR) ; $(SRC)/$(MPFR)/$(CFG) $(GCCLIBS_CFG) &&\
	$(MAKE) && make install-strip

.PHONY: mpc
mpc: $(CROSS)/lib/libmpc.a
$(CROSS)/lib/libmpc.a: $(SRC)/$(MPC)/README
	rm -rf $(TMP)/$(MPC) ; mkdir $(TMP)/$(MPC) ;\
	cd $(TMP)/$(MPC) ; $(SRC)/$(MPC)/$(CFG) $(GCCLIBS_CFG) &&\
	$(MAKE) && make install-strip
