
# mpy-cross cross-compiler
MC=mpy-cross

# build directory
TARGET=build

OBJS=$(TARGET)/lib/turtle.mpy $(TARGET)/calibration.py $(TARGET)/test.py

all: $(OBJS) bundle

$(TARGET)/lib:
	mkdir -p $@

$(TARGET)/lib/turtle.mpy: src/lib/turtle.py $(TARGET)/lib
	$(MC) -o $@ $<

$(TARGET)/%.py: src/%.py
	cp $< $@


.PHONY: bundle

bundle:
	$(MAKE) -C bundle
