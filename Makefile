
# mpy-cross cross-compiler
MC=mpy-cross

# build directory
TARGET=build

JSLOGO2PY=../jslogo2py

OBJS=$(TARGET)/lib/turtle.mpy $(TARGET)/calibration.py $(TARGET)/code.py $(TARGET)/run_calibration.py $(TARGET)/test.py $(TARGET)/lib/jslogort.mpy $(TARGET)/wheel_calibration.py

ifeq ("$(wildcard $(JSLOGO2PY)/)","")
  $(error JSLOGO2PY=${JSLOGO2PY} does not exist)
endif


all: $(OBJS) bundle

$(TARGET)/lib:
	mkdir -p $@

$(TARGET)/lib/turtle.mpy: src/lib/turtle.py $(TARGET)/lib
	$(MC) -o $@ $<

$(TARGET)/lib/jslogort.mpy: $(JSLOGO2PY)/jslogort.py $(TARGET)/lib
	$(MC) -o $@ $<

$(TARGET)/%.py: src/%.py
	cp $< $@


.PHONY: bundle

bundle:
	$(MAKE) -C bundle

.PHONY: zip

# this deposits in the zip in $(TARGET)/..
zip: $(TARGET)
	cd $(TARGET) && zip -r ../ostr.zip *
