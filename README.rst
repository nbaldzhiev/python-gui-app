GUI Application written in Python (2020 project)
==================================

**Please note, this project is from 2020, but its commit history was deleted for privacy reasons, hence its empty commit history and single commit from 2022.**

A GUI application written in Python using wxPython as a project for a past company I've worked for. The goal was to make it easier to make POST requests to a configurable environment using configurable parameters, which are then added as payload to the POST request.
The application was product-specific, so the repository here is public for the sake of showing a project for a GUI application with Python.

The tool has standalone executable versions for MacOS and Linux, which is the preferred way to use the tool.

Installing
----------
As already mentioned above, the preferred way to use the tool is as a standalone executable application.
However, if one desires to use it from source, it needs to be installed first.

It is meant to be used in a virtual environment (I've used venv) and this is going to be example here.
It has currently been tested on MacOS 10.15.4 and Ubuntu 18.04, both on Python 3.6.8 and 3.8.3.
It is likely that the tool would work on many other combinations of OS version/Python version,
but those are the ones, which have been tested with.

The instructions below use Python 3.8.3 as an example. After activating the virtual environment,
specifying the python version might not be necessary, but I've included it in the example nevertheless.

1. Clone the repository:

.. code-block:: text

    $ git clone https://github.com/nbaldzhiev/python-gui-app.git

2. Create a virtual environment (with venv, preferably) within it:

.. code-block:: text

    $ cd python-gui-app/
    $ python3.8 -m venv venv

3. Activate the virtual environment:

.. code-block:: text

    $ source venv/bin/activate

4. Install the required packages:

.. code-block:: text

    $ python3.8 -m pip install -r requirements.txt

.. note::
    Regarding Linux, on Ubuntu 18.04 I always have an error when trying to install the wxPython
    package via the requirements.txt file. In order to install wxPython
    on Ubuntu, if you have the same problem, run the fhe following command in the virtual environment:

.. code-block:: text

    $ python3.8 -m pip install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-<version> wxPython

... where <version> is the Ubuntu version, i.e. /ubuntu-18.04 for 18.04, /ubuntu-16.04 for 16.04, and so on.

5. Run the application to verify that installation has been successful.

.. code-block:: text

    $ python3.8 app.py
