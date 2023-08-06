#from distutils.core import setup, Extension
from setuptools import setup, Extension
from glob import glob
import tempfile
import os

PYTHON_TEMPLATE = """#!/bin/sh

# The python version we're executing.
PYTHON=$(basename $0)
# The location of this wrapper, which must be in the path.
FUNCTIONTRACE_WRAPPER_PATH=$(dirname $(which $PYTHON))

# Remove the wrapper directory from PATH, allowing us to find the real Python.
PATH=$(echo "$PATH" | sed -e "s#$FUNCTIONTRACE_WRAPPER_PATH:##")

exec $(which $PYTHON) -m functiontrace "$@"
"""

def main():
    # Generate wrappers for the various Python versions we support to ensure
    # they're included in our PATH.
    wrap_pythons = ["python", "python3", "python3.6", "python3.7", "python3.8"]

    with tempfile.TemporaryDirectory() as tmp:
        wrappers = []
        for python in wrap_pythons:
            with open(os.path.join(tmp, python), "w") as f:
                f.write(PYTHON_TEMPLATE)
                os.chmod(f.name, 0o655)
                wrappers.append(f.name)

        setup(
            py_modules=["functiontrace"],
            ext_modules=[
                Extension("_functiontrace", ["_functiontrace.c", "mpack/mpack.c"])
            ],
            data_files=[("path", wrappers)],
            include_package_data=True
        )

if __name__ == "__main__":
    main()
