# Web interface to visualize Curry computations based in ICurry

## Installation

The implementation of the web interface requires python 3.7, pip3 and Flask.
These can be installed as follows (Ubuntu, Debian):

    > sudo apt install python3 python3-pip
    > pip3 install Flask==2.3.1

Furthermore, an installation of the ICurry package (version 3.2.0 or newer)
is required, i.e., the executable `icurry` must be in the path.
This can be achieved by the Curry Package Manager as follows:

    > cypm update
    > cypm install icurry

After this installation, one can start the server for the web interface
as follows:

    > cd webapp
    > python3 icurry_web.py

Now it can be accessed on <http://localhost:5000>
