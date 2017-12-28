QEMU_CFG = -cpu $(QEMU_CPU) -m 64M -net none -localtime 
QEMU_SERIAL = -serial file:ttyS0.log -append "console=ttyS0,115200" 
#QEMU_CFG += $(QEMU_SERIAL)
.PHONY: emu
emu: $(BOOT)/$(HW)_$(APP).kernel
	qemu-system-$(ARCH) $(QEMU_CFG) -kernel $<
