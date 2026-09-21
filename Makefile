# Crown & Chaos Butano project configuration.
#
# Keep this file at the repository root: Butano's outer build reinvokes this
# exact Makefile from BUILD, which is required for source compilation and ROM
# linking. Generated binary inputs are prepared before the default build by CI
# or with `make assets` locally.

PYTHON ?= python3

ifneq ($(filter assets verify clean,$(MAKECMDGOALS)),)

.PHONY: assets verify clean

assets:
	$(PYTHON) tools/generate_placeholder_assets.py

verify:
	$(PYTHON) tools/check_project.py
	$(PYTHON) tools/generate_placeholder_assets.py --check
	tools/run_host_tests.sh

clean:
	rm -rf build crown_and_chaos.elf crown_and_chaos.gba crown_and_chaos.map
	rm -f graphics/*.png audio/*.wav

else

TARGET      := crown_and_chaos
BUILD       := build
SOURCES     := src
INCLUDES    := include
DATA        := data
GRAPHICS    := graphics
AUDIO       := audio
DMGAUDIO    := dmg_audio

ROMTITLE    := CROWN CHAOS
ROMCODE     := CRNC
MAKERCODE   := 00

USERFLAGS   := -Wall -Wextra -Wpedantic -Werror

BUTANO      ?= external/butano/butano
LIBBUTANO   := $(BUTANO)
LIBBUTANOABS := $(realpath $(LIBBUTANO))

ifeq ($(strip $(LIBBUTANOABS)),)
$(error Butano SDK not found at '$(LIBBUTANO)')
endif

include $(LIBBUTANO)/butano.mak

endif
