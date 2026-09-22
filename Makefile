# Crown & Chaos — standard Butano 18.1.0 project Makefile.

TARGET      := crown_and_chaos
BUILD       := build
SOURCES     := src
INCLUDES    := include
DATA        :=
GRAPHICS    := graphics
AUDIO       := audio
DMGAUDIO    :=

ROMTITLE    := CROWN CHAOS
ROMCODE     := CRNC
MAKERCODE   := 00

USERFLAGS   := -Wall -Wextra -Wpedantic -Werror
USERCXXFLAGS :=
USERASFLAGS :=
USERLDFLAGS :=
USERLIBDIRS :=
USERLIBS    :=

BUTANO      ?= external/butano/butano
LIBBUTANO   := $(BUTANO)
LIBBUTANOABS := $(realpath $(LIBBUTANO))

ifeq ($(strip $(LIBBUTANOABS)),)
$(error Butano SDK not found at '$(LIBBUTANO)')
endif

include $(LIBBUTANOABS)/butano.mak
