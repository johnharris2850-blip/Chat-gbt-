PYTHON ?= python3

.PHONY: assets verify clean

assets:
	$(PYTHON) tools/generate_placeholder_assets.py

verify:
	$(PYTHON) tools/check_project.py
	$(PYTHON) tools/generate_placeholder_assets.py --check
	tools/run_host_tests.sh

clean:
	rm -rf build crown_and_chaos.elf crown_and_chaos.gba crown_and_chaos.map
	rm -f graphics/*.bmp graphics/*.png audio/*.wav
