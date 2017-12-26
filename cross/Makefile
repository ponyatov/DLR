HW ?= i486sx

include hw/$(HW)
include cpu/$(CPU)

						# current directory (full path)
CWD = $(CURDIR)
						# software packages source tarballs
GZ = $(CWD)/gz
						# temp directory
TMP = $(CWD)/tmp
						# directory list must be created
DIRS = $(GZ) $(TMP) 

PHONY: dirs
dirs:
	mkdir -p $(DIRS)