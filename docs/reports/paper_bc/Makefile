TECTONIC ?= ../../../tools/tectonic-portable/tectonic

MAIN = paper_bc_iberamia

.PHONY: all main clean check-tectonic

all: main

main: check-tectonic
	$(TECTONIC) $(MAIN).tex

check-tectonic:
	@test -x "$(TECTONIC)" || { echo "Tectonic not found or not executable: $(TECTONIC)"; exit 1; }

clean:
	rm -f $(MAIN).aux $(MAIN).log $(MAIN).out $(MAIN).toc $(MAIN).synctex.gz
