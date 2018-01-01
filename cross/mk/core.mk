.PHONY: core kernel ulibc busybox
core: kernel ulibc busybox

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
	cat hw/$(HW).kernel >> $(SRC)/$(KERNEL)/.config
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
	# cross config
	echo "KERNEL_HEADERS=\"$(ROOT)/include\"" >> $(SRC)/$(ULIBC)/.config
	# load predefined ulibc config
	cat all.ulibc >> $(SRC)/$(ULIBC)/.config
	cat arch/$(ARCH).ulibc >> $(SRC)/$(ULIBC)/.config
	cat cpu/$(CPU).ulibc >> $(SRC)/$(ULIBC)/.config
	# run menu config
	cd $(SRC)/$(ULIBC) ; $(MAKE) $(ULIBC_CFG) menuconfig
	# run make & install
	cd $(SRC)/$(ULIBC) ; $(MAKE) $(ULIBC_CFG)
	cd $(SRC)/$(ULIBC) ; $(MAKE) $(ULIBC_CFG) install
	cd $(SRC)/$(ULIBC) ; $(MAKE) $(ULIBC_CFG) install_utils
	cd $(SRC)/$(ULIBC) ; $(MAKE) $(ULIBC_CFG) hostutils
	cp $(SRC)/$(ULIBC)/utils/ldd.host      $(CROSS)/bin/$(TARGET)-ldd
	cp $(SRC)/$(ULIBC)/utils/ldconfig.host $(CROSS)/bin/$(TARGET)-ldconfig
	cp $(SRC)/$(ULIBC)/utils/getconf.host  $(CROSS)/bin/$(TARGET)-getconf

BUSYBOX_CFG =  CROSS_COMPILE=$(TARGET)- SYSROOT=$(ROOT) \
				CONFIG_PREFIX=$(ROOT)
			
busybox: $(SRC)/$(BUSYBOX)/README
	# empty config
	cd $(SRC)/$(BUSYBOX) ; $(MAKE) $(BUSYBOX_CFG) distclean
	cd $(SRC)/$(BUSYBOX) ; $(MAKE) $(BUSYBOX_CFG) allnoconfig
	# load predefined ulibc config via regexp patcher (python)
	./all.busybox $(SRC)/$(BUSYBOX)/.config $(TARGET)- $(ROOT)
	# run menu config
	cd $(SRC)/$(BUSYBOX) ; $(MAKE) $(BUSYBOX_CFG) menuconfig
	# run make
	cd $(SRC)/$(BUSYBOX) ; $(MAKE) $(BUSYBOX_CFG) install
