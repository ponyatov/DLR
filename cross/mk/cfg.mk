CFG = configure --disable-nls \
	--prefix=$(CROSS) --target=$(TARGET) \
	--docdir=$(TMP)/doc --mandir=$(TMP)/man --infodir=$(TMP)/info
	