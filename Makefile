# Crown & Chaos build wrapper.
# Generates all binary inputs from reviewed text/code before invoking Butano.

.DEFAULT_GOAL := all

PYTHON ?= python3
BUTANO ?= external/butano/butano

.PHONY: all assets verify clean

all: assets
	$(MAKE) -f make/Butano.mk BUTANO="$(BUTANO)" LIBBUTANO="$(BUTANO)" LIBBUTANOABS="$(realpath $(BUTANO))"

assets:
	$(PYTHON) tools/generate_placeholder_assets.py

verify:
	$(PYTHON) tools/check_project.py
	$(PYTHON) tools/generate_placeholder_assets.py --check
	tools/run_host_tests.sh

clean:
	rm -rf build crown_and_chaos.elf crown_and_chaos.gba crown_and_chaos.map
	rm -f graphics/*.png audio/*.wav
