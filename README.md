This firmware is intended for use with the [Open Source Turtle
Robot](https://github.com/aspro648/OSTR/) v2.2 Hardware. It is based
on the original firmware by Ken Olsen which is used under the
conditions of the CC-BY-SA 3.0 US license. It is not intended to be
compatible with the original firmware and has been updated to work
with CircuitPython 8.2.0.

This 2023 edition of the firmware now contains a Logo interpreter
written in CircuitPython. The interpreter operators on a stream of
parsed tokens produced by the 2023 edition of JavaScript [Logo
interpreter](https://github.com/sree314/jslogo2py/).

The Logo interpreter is an incomplete Python/CircuitPython translation
of the JavaScript logo interpreter. It also contains additional
features. Variables `LED1', `LED2` and `EMITTER` control the two LEDs
and the IR LEDs respectively. The functions `LEFTSENSOR` and
`RIGHTSENSOR` yield IR detector readings. The `BUTTONP` maps to the
button on the OSTR.


Building from Source
--------------------

This assumes you have a Linux system and you have `mpy-cross` installed.

First, download an appropriate [adafruit circuitpython library
bundle](https://circuitpython.org/libraries) in the 8.x series and
store it in the `bundle/` directory.

In the downloaded repository:

```
  mkdir build
  make
```

This will prepare the files in the `build/` directory.

Then assuming the robot is connected to `/run/media/xyz/CIRCUITPYTHON`, do:

```
  cp -av build/* /run/media/xyz/CIRCUITPYTHON
```

Adjust the paths above as necessary.


License
-------

Most contents of this repository are Copyright (C) University of
Rochester. They may be used under the [Attribution-ShareAlike 3.0 United States (CC BY-SA 3.0 US)](https://creativecommons.org/licenses/by-sa/3.0/us/)

You are free to:

- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material

Under the following terms:

- Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.

- ShareAlike — If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.
