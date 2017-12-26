WGET = wget -P $(GZ) -c	
PHONY: gz gz_cross
gz: gz_cross

gz_cross:
	exit -1
	$(WGET) http://ftp.gnu.org/gnu/binutils/$(BINUTILS_GZ)
	$(WGET) http://gcc.skazkaforyou.com/releases/$(GCC)/$(GCC_GZ)
	$(WGET) ftp://ftp.gmplib.org/pub/gmp/$(GMP_GZ)
	