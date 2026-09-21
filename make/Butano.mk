# Butano project configuration. Invoke through the root Makefile so generated
# binary inputs exist before Butano's asset dependency graph is evaluated.

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

BUTANO      ?= external/butano

ifeq ($(wildcard $(BUTANO)/butano.mak),)
$(error Butano not found at '$(BUTANO)'. Run tools/bootstrap_butano.sh or set BUTANO=/absolute/path/to/butano)
endif

include $(BUTANO)/butano.mak
