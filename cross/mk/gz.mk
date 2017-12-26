WGET = wget -P $(GZ) -c	
PHONY: gz gz_cross
gz: gz_cross

gz_cross:
	$(WGET) http://ftp.gnu.org/gnu/binutils/$(BINUTILS_GZ)
