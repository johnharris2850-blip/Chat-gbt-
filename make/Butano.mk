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

BUTANO      ?= external/butano/butano

# Butano 18.1.0's public project makefile expects LIBBUTANO to name the SDK
# directory. The root Makefile passes it explicitly to this recursive make,
# following Butano's project Makefile contract instead of relying on a
# make-local alias to survive recursion.
LIBBUTANO   ?= $(BUTANO)

$(info Crown & Chaos BUTANO=$(BUTANO))
$(info Crown & Chaos LIBBUTANO=$(LIBBUTANO))
$(info Crown & Chaos butano_dka=$(LIBBUTANO)/butano_dka.mak)

ifeq ($(wildcard $(LIBBUTANO)/butano.mak),)
$(error Butano not found at '$(LIBBUTANO)'. Run tools/bootstrap_butano.sh or set BUTANO=/absolute/path/to/butano)
endif

ifeq ($(wildcard $(LIBBUTANO)/butano_dka.mak),)
$(error Butano devkitARM makefile not found at '$(LIBBUTANO)/butano_dka.mak')
endif

include $(LIBBUTANO)/butano.mak
