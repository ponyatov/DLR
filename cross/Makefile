APP = dynamic

HW ?= i486sx

include hw/$(HW).mk
include cpu/$(CPU).mk
include arch/$(ARCH).mk

include mk/version.mk
include mk/package.mk

							# current directory (full path)
CWD = $(CURDIR)
							# software packages source tarballs
GZ = $(CWD)/gz
							# temp directory for off-tree build
TMP = $(CWD)/tmp
							# temp directory for source code
SRC = $(CWD)/src
							
							# cross compiler tools						
CROSS = $(CWD)/$(TARGET).cross
							# target filesystem
ROOT = $(CWD)/$(TARGET)
							# bootloader images
BOOT = $(ROOT)/boot

							# directory list must be created
DIRS = $(GZ) $(TMP) $(SRC) $(TMP) $(CROSS) $(ROOT) $(BOOT)

							# set path search
XPATH = PATH=$(CROSS)/bin:$(PATH)

PHONY: dirs
dirs:
	mkdir -p $(DIRS)

include mk/gz.mk

include mk/cfg.mk

include mk/cross.mk
include mk/core.mk

include mk/emu.mk

include mk/unpack.mk

.PHONY: ramclean
ramclean:
	rm -rf $(SRC)/* $(TMP)/*
