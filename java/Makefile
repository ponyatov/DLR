JASMIN_VER = 2.4
JASMIN = jasmin-$(JASMIN_VER)
JASMIN_GZ = $(JASMIN).zip

JAS = $(JASMIN)/jasmin.jar

WGET = wget -c

Hello.class: Hello.j $(JAS)
	java -jar $(JAS) $<

$(JAS): $(JASMIN_GZ)
	unzip $< && touch $@
$(JASMIN_GZ):
	$(WGET) http://downloads.sourceforge.net/project/jasmin/jasmin/$(JASMIN)/$(JASMIN_GZ) && touch $@
	