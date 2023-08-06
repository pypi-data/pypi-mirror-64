﻿jk_version
==========

Introduction
------------

This python module provides a version class. Instances of this class may be used in representing and version numbers and compare them.

Information about this module can be found here:

* [github.org](https://github.com/jkpubsrc/....)
* [pypi.python.org](https://pypi.python.org/pypi/jk_version)

Why this module?
----------------

...

Limitations of this module
--------------------------

...

How to use this module
----------------------

### Import this module

Please include this module into your application using the following code:

```python
import jk_version
```

### Parse a version number

Version numbers can either be specified as lists of integers or as a string. Examples:

* `Version([ 1, 7, 51 ])`
* `Version(( 1, 7, 51 ))`
* `Version("1.7.51")`

### Version numbering schema

For compatibility reasons the version number parser is designed to accept the following schema:

*[ epoch ":" ] version_data*

Where *epoch* is optional and - if present - must be an integer, and *version_data* is a regular version string consisting of decimal numbers separated by full stops.

Examples for valid version numbers:

* `0`
* `0.1`
* `0.1.2`
* `2020.12.24`
* `2:0.1.2`

### Comparing version numbers

Version numbers can be compared. Example:

```python
v1 = Version("0.1.2")
v2 = Version("0.2.0")
print(v2 > v1)
```

This will print: `True`

Contact Information
-------------------

This work is Open Source. This enables you to use this work for free.

Please have in mind this also enables you to contribute. We, the subspecies of software developers, can create great things. But the more collaborate, the more fantastic these things can become. Therefore Feel free to contact the author(s) listed below, either for giving feedback, providing comments, hints, indicate possible collaborations, ideas, improvements. Or maybe for "only" reporting some bugs:

* Jürgen Knauth: jknauth@uni-goettingen.de, pubsrc@binary-overflow.de

License
-------

This software is provided under the following license:

* Apache Software License 2.0



