# Crown & Chaos — standard Butano 18.1.0 project Makefile.

PROJECT_ROOT := $(patsubst %/,%,$(dir $(realpath $(firstword $(MAKEFILE_LIST)))))

TARGET      := crown_and_chaos
BUILD       := build
PYTHON      := python3
SOURCES     := src
INCLUDES    := include
DATA        :=
GRAPHICS    := $(PROJECT_ROOT)/graphics
AUDIO       := $(PROJECT_ROOT)/audio
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
