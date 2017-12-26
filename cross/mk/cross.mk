.PHONY: cross
cross: binutils

# get number or CPU cores for build system
BUILD_CPU_NUMBER = $(shell grep processor /proc/cpuinfo | wc -l)
# parallel make
MAKE = make -j$(BUILD_CPU_NUMBER)

.PHONY: binutils
binutils: $(CROSS)/bin/$(TARGET)-as
$(CROSS)/bin/$(TARGET)-as: $(SRC)/$(BINUTILS)/README
	rm -rf $(BLD)/$(BINUTILS) ; mkdir $(BLD)/$(BINUTILS) ;\
	cd $(BLD)/$(BINUTILS) ; $(SRC)/$(BINUTILS)/$(CFG) \
		--with-sysroot=$(ROOT) &&\
	$(MAKE) && make install-strip
