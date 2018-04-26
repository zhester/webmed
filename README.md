# webmed

Web Interface to Media Files

Implements an interface to media files that are accessible to the host.
Instead of implementing a complicated "application," this runs its own server
(which can be placed behind a WSGI server, if needed) to provide a simple
browser-based interface to viewing the media files.

Requires Python 3 on the server and a web browser.

    # Bind to all addresses on port 80
    webmed.py

    # Bind to specified address on port 8000
    webmed.py --address 192.168.0.2 --port 8000

