.PHONY: sync
sync: $(HOME)/.unison/$(APP).prf doc
	unison $(APP)
$(HOME)/.unison/$(APP).prf: $(CWD)/.unison
	ln -fs $< $@
