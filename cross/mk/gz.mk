WGET = wget -P $(GZ) -c	
PHONY: gz gz_cross gz_core
gz: gz_cross gz_core

gz_cross:
#	exit -1
	$(WGET) ftp://ftp.gmplib.org/pub/gmp/$(GMP_GZ)
	$(WGET) http://www.mpfr.org/mpfr-$(MPFR_VER)/$(MPFR).tar.bz2
	$(WGET) http://www.multiprecision.org/mpc/download/$(MPC_GZ)
	$(WGET) http://ftp.gnu.org/gnu/binutils/$(BINUTILS_GZ)
	$(WGET) http://gcc.skazkaforyou.com/releases/$(GCC)/$(GCC_GZ)

gz_core:
	$(WGET) http://www.kernel.org/pub/linux/kernel/v4.x/$(KERNEL_GZ)
