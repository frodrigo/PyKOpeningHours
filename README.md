PyKOpeningHours
===============

Python wrapper for KOpeningHours

KOpeningHours is a Qt-based C++ library for parsing and evaluating opening hours expressions from OpenStreetMap.
See https://invent.kde.org/libraries/kopeninghours

This python wrapper, developed using boost::python, makes that library available to python.

Building
========

To build it the python way:

`python3 setup.py build`
or
`pip install .`

Or to build it the usually way for any cmake project:

```
mkdir build
cd build
cmake ..
make
```

And for testing:

PYTHONPATH=$PWD python3 ../test.py

should print `Fr 11:00-23:00`

