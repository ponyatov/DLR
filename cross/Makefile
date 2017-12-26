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
							# temp directory
TMP = $(CWD)/tmp
							
							# cross compiler tools						
CROSS = $(CWD)/$(TARGET).cross
							# target filesystem
ROOT = $(CWD)/$(TARGET)
							# source code
SRC = $(TMP)/src
							# off-tree build
BLD = $(TMP)/build

							# directory list must be created
DIRS = $(GZ) $(TMP) $(SRC) $(BLD) $(CROSS) $(ROOT)

PHONY: dirs
dirs:
	mkdir -p $(DIRS)

include mk/gz.mk

include mk/cross.mk

include mk/unpack.mk
