#!/usr/bin/env python3
#=============================================================================
#
# Web Media Server
#
#=============================================================================

"""
Web Media Server
================
"""


import os
import sys
import wsgiref.simple_server


#=============================================================================
def application( environ, start_response ):
    """
    WSGI Application Entry Point
    """
    content = 'Hello World'
    headers = [
        ( 'Content-Type', 'text/plain' ),
        ( 'Content-Length', str( len( content ) ) ),
    ]
    start_response( '200 Ok', headers )
    yield bytes( content, 'utf-8' )


#=============================================================================
def run( address = '', port = 80 ):
    """
    Run the web server until finished or interrupted.
    """

    # Construct a server.
    server = wsgiref.simple_server.make_server( address, port, application )

    # Run the server.
    server.serve_forever()

    # Return result.
    return 0


#=============================================================================
def main( argv ):
    """
    Script execution entry point

    @param argv List of arguments passed to the script
    @return     Shell exit code (0 = success)
    """

    # Import argparse when using this module as a script.
    import argparse

    # Create and configure an argument parser.
    parser = argparse.ArgumentParser(
        description = 'Web Media Server',
        add_help    = False
    )
    parser.add_argument(
        '-a',
        '--address',
        default = '',
        help    = 'Bind server to specific address.'
    )
    parser.add_argument(
        '-h',
        '--help',
        default = False,
        help    = 'Display this help message and exit.',
        action  = 'help'
    )
    parser.add_argument(
        '-p',
        '--port',
        default = 80,
        type    = int,
        help    = 'Bind server to specified port.'
    )

    # Parse the arguments.
    args = parser.parse_args( argv[ 1 : ] )

    # Try to run the server forever.
    try:

        # Run the server.
        result = run( args.address, args.port )

    # Handle keyboard event.
    except KeyboardInterrupt:

        # Attempt to exit gracefully.
        try:
            sys.exit( 0 )

        # Handle exit collapsing.
        except SystemExit:
            os._exit( 0 )

    # Return result.
    return result


#=============================================================================
if __name__ == '__main__':
    sys.exit( main( sys.argv ) )

