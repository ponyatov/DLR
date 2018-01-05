JASMIN_VER = 2.4
JASMIN = jasmin-$(JASMIN_VER)
JASMIN_GZ = $(JASMIN).zip

JAS = $(JASMIN)/jasmin.jar

WGET = wget -c

go: latex Hello.class jHello.class 
	java Hello

latex:
	cd .. ; $(MAKE) # latex
	
JAVAP = javap -c -s -verbose
	
jHello.class: jHello.java
	javac $< && $(JAVAP) $@ > $@.dis

Hello.class: Hello.j $(JAS)
	java -jar $(JAS) $< && $(JAVAP) $@ > $@.dis

.PHONY: install
install: $(JAS) jasper/jasper.jar
$(JAS): $(JASMIN_GZ)
	unzip $< && touch $@
$(JASMIN_GZ):
	$(WGET) http://downloads.sourceforge.net/project/jasmin/jasmin/$(JASMIN)/$(JASMIN_GZ) && touch $@
	
jasper/jasper.jar: jasper/META-INF/MANIFEST.MF jasper/jasper/Jasper.class
	cd jasper ; jar -cf jasper.jar META-INF/MANIFEST.MF jasper/*
jasper/jasper/Jasper.class: jasper/pom.xml
	cd jasper ; javac -d . src/main/java/jasper/*.java && 
jasper/pom.xml:
	git clone --depth=1 https://github.com/kohsuke/jasper.git