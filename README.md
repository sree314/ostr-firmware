This firmware is intended for use with the [Open Source Turtle
Robot](https://github.com/aspro648/OSTR/) v2.2 Hardware. It is based
on the original firmware by Ken Olsen which is used under the
conditions of the CC-BY-SA 3.0 US license. It is not intended to be
compatible with the original firmware and has been updated to work
with CircuitPython 7.3.0.

Building from Source
--------------------

This assumes you have a Linux system and you have `mpy-cross` installed.

In the downloaded repository:

```
  mkdir build
  make
```

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
