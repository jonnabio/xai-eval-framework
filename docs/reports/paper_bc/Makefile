TECTONIC ?= ../../../tools/tectonic-portable/tectonic

MAIN = paper_bc_tmlr
SUPPLEMENT = paper_bc_tmlr_supplementary
PEERJ = paper_bc_peerjcs
PEERJ_S1 = paper_bc_peerjcs_supplemental_S1

.PHONY: all main supplement peerj clean check-tectonic

all: main supplement

main: check-tectonic
	$(TECTONIC) $(MAIN).tex

supplement: check-tectonic
	$(TECTONIC) $(SUPPLEMENT).tex

# PeerJ Computer Science edition (review build, line numbers on).
peerj: check-tectonic
	$(TECTONIC) $(PEERJ).tex
	$(TECTONIC) $(PEERJ_S1).tex

check-tectonic:
	@test -x "$(TECTONIC)" || { echo "Tectonic not found or not executable: $(TECTONIC)"; exit 1; }

clean:
	rm -f $(MAIN).aux $(MAIN).log $(MAIN).out $(MAIN).toc $(MAIN).synctex.gz
	rm -f $(SUPPLEMENT).aux $(SUPPLEMENT).log $(SUPPLEMENT).out $(SUPPLEMENT).toc $(SUPPLEMENT).synctex.gz
