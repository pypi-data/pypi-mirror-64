Python Dev Utils
===

A collection of commands and functions used for building modules and developing python code.

Provides the following commands: 

* bump_package_patch_version - when run inside a module with setup.py, it will update the VERSION. 

Test
---

    make test

You can also test with a specific version of Python:

    make PYTHON_VERSION=2.7.11 test
