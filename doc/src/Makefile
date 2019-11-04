

MAKEFLAGS += --no-builtin-rules
MAKEFLAGS += --no-builtin-variables
SHELL := /bin/bash

.ONESHELL:
.SHELLFLAGS: -c
.SILENT:

SCRIPT=build_image.py


define TEMPLATE_IMAGE = 

.PHONY: image-all # build all images
image-all: image-$(1)

.PHONY: image-$(1) # build image X
image-$(1): ../$(1).png

../$(1).png: $(1).json
	pipenv run python $(SCRIPT) $$< $$@ 

endef


.PHONY: help # [default] print this message
help:
	@grep -h '^\.PHONY: .* #' $(MAKEFILE_LIST) | sed 's/\.PHONY: \(.*\) # \(.*\)/\1\t\2/' | sed -E 's/\$$\(1\)/X/'| sed -E 's/\$$\(2\)/Y/' | sed -E 's/\$$\(3\)/Z/' | sort | expand -t20

.PHONY: list_target # list all target of this Makefile
list_target:
	@$(MAKE) -pRrq -f $(MAKEFILE_LIST) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

GRAPH_CONF=$(wildcard *.json)
GRAPH_IMG := $(patsubst %.json,%,$(GRAPH_CONF))

test:
	echo $(GRAPH_CONF)
	echo $(GRAPH_IMG)

$(foreach img_name,$(GRAPH_IMG),$(eval $(call TEMPLATE_IMAGE,$(img_name))))

