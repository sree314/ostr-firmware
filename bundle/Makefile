TARGET=../build
BUNDLE=$(lastword $(wildcard adafruit-circuitpython-bundle-7.x-mpy-*.zip))

ifeq ($(BUNDLE),)
$(error "No adafruit-circuitpython-bundle-7.x-mpy-*.zip file found in current directory. Download from: <https://circuitpython.org/libraries>")
else
$(info "Using $(BUNDLE)")
endif

BUNDLE_DIR=$(basename $(BUNDLE))

$(info $(BUNDLE_DIR))

all: $(BUNDLE_DIR) \
	$(TARGET)/lib/adafruit_dotstar.mpy \
	$(TARGET)/lib/adafruit_motor \
	$(TARGET)/lib/adafruit_waveform \
	$(TARGET)/lib/simpleio.mpy \
	$(TARGET)/lib/adafruit_hid \
	$(TARGET)/lib/adafruit_register  \
	$(TARGET)/lib/neopixel.mpy


$(BUNDLE_DIR): $(BUNDLE)
	unzip $(BUNDLE)

$(TARGET)/lib/%: $(BUNDLE_DIR)/lib/%
	cp -a $< $@
