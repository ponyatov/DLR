QEMU_CFG = -cpu $(QEMU_CPU) -m 512M -net none -localtime 
QEMU_SERIAL = -serial file:ttyS0.log -append "console=ttyS0,115200" 
#QEMU_CFG += $(QEMU_SERIAL)
.PHONY: emu
emu: $(BOOT)/$(HW)_$(APP).kernel $(BOOT)/$(HW)_$(APP).rootfs
	qemu-system-$(ARCH) $(QEMU_CFG) \
		-kernel $(BOOT)/$(HW)_$(APP).kernel \
		-initrd $(BOOT)/$(HW)_$(APP).rootfs
#	 -append "noquiet vga=current loglevel=11"

ROOTREX = "./(boot|include|lib/.+\.a)"
LDCONFIG = $(XPATH) $(TARGET)-ldconfig
.PHONY: root
root:
	# /etc
	rm -rf $(ROOT)/etc ; cp -r etc $(ROOT)/
	# update shared libs
	$(LDCONFIG) -v -r $(ROOT)
	# build initrd 
	cd $(ROOT) && find . | egrep -v $(ROOTREX) | cpio -o -H newc > $(BOOT)/$(HW)_$(APP).cpio
	cat $(BOOT)/$(HW)_$(APP).cpio | gzip -9 > $(BOOT)/$(HW)_$(APP).rootfs

KVM_CFG = 
.PHONY: kvm
kvm: $(BOOT)/$(HW)_$(APP).kernel $(BOOT)/$(HW)_$(APP).rootfs
	qemu-kvm $(KVM_CFG) \ 
		-kernel $(BOOT)/$(HW)_$(APP).kernel \
		-initrd $(BOOT)/$(HW)_$(APP).rootfs
	