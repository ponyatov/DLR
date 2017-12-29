.PHONY: core kernel ulibc
core: kernel

KERNEL_ARCH ?= $(ARCH)
KERNEL_CFG = ARCH=$(KERNEL_ARCH) \
	INSTALL_HDR_PATH=$(ROOT) INSTALL_MOD_PATH=$(ROOT)
 
kernel: $(SRC)/$(KERNEL)/README
	# empty config
	cd $(SRC)/$(KERNEL) ; make $(KERNEL_CFG) distclean
	cd $(SRC)/$(KERNEL) ; make $(KERNEL_CFG) allnoconfig
	# HW/APP config
	echo "CONFIG_CROSS_COMPILE=\"$(TARGET)-\"" >> $(SRC)/$(KERNEL)/.config
	echo "CONFIG_LOCALVERSION=\"-$(HW)_$(APP)\"" >> $(SRC)/$(KERNEL)/.config
	echo "CONFIG_DEFAULT_HOSTNAME=\"$(APP)\"" >> $(SRC)/$(KERNEL)/.config
	# load predefined kernel config
	cat all.kernel >> $(SRC)/$(KERNEL)/.config
	cat arch/$(ARCH).kernel >> $(SRC)/$(KERNEL)/.config
	cat cpu/$(CPU).kernel >> $(SRC)/$(KERNEL)/.config
	# run menu config
	cd $(SRC)/$(KERNEL) ; make $(KERNEL_CFG) menuconfig
	# run build
	cd $(SRC)/$(KERNEL) ; $(MAKE) $(KERNEL_CFG)
	# copy to BOOT
	cp $(SRC)/$(KERNEL)/arch/$(KERNEL_ARCH)/boot/bzImage $(BOOT)/$(HW)_$(APP).kernel
	# inclall headers to ROOT
	cd $(SRC)/$(KERNEL) ; $(MAKE) $(KERNEL_CFG) headers_install

ULIBC_CFG = CROSS=$(TARGET)- ARCH=$(ARCH) PREFIX=$(ROOT)
ulibc: $(SRC)/$(ULIBC)/README
	# empty config
	cd $(SRC)/$(ULIBC) ; $(MAKE) $(ULIBC_CFG) distclean
	cd $(SRC)/$(ULIBC) ; $(MAKE) $(ULIBC_CFG) allnoconfig
	# load predefined ulibc config
	cat all.ulibc >> $(SRC)/$(ULIBC)/.config
	cat cpu/$(CPU).ulibc >> $(SRC)/$(ULIBC)/.config
	cat arch/$(ARCH).ulibc >> $(SRC)/$(ULIBC)/.config
	# run menu config
	cd $(SRC)/$(ULIBC) ; $(MAKE) $(ULIBC_CFG) menuconfig
	