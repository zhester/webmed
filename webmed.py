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


import logging
import mimetypes
import os
import sys
import urllib
import wsgiref.simple_server

try:
    from http.client import responses as http_responses
except ImportError:
    from httplib import responses as http_responses

logging.basicConfig(
    format = '%(asctime); %(message)',
    level  = logging.INFO
)


#=============================================================================
_config = {
    'address' : '',
    'docroot' : os.getcwd(),
    'port'    : 80,
}


#=============================================================================
_html = '''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{title}</title>
  {head}
  <link rel="icon" type="image/png" href="/assets/spartan.png">
  <link rel="stylesheet" href="/assets/styles.css">
  <script src="/assets/client.js"></script>
</head>
<body>
{body}
</body>
</html>'''


#=============================================================================
def handle_assets( environ ):
    """
    Handle application asset requests.
    """
    qpath = environ[ 'request.path' ]
    if len( qpath ) == 0:
        return 403, [], make_error( 'Forbidden', environ[ 'PATH_INFO' ] )
    rpath = os.path.sep.join( qpath )
    fpath = os.path.join( _config[ 'docroot' ], rpath )
    if os.path.isfile( fpath ) is False:
        return 404, [], make_error( 'Not Found', environ[ 'PATH_INFO' ] )
    mtype = mimetypes.guess_type( fpath )
    if mtype[ 1 ] is None:
        ctype = mtype[ 0 ]
    else:
        ctype = '; '.join( mtype )
    headers = [
        ( 'Content-Type', ctype )
    ]
    with open( fpath, 'rb' ) as fh:
        content = fh.read()
    return 200, headers, content


#=============================================================================
def handle_default( environ ):
    """
    Default request handler (indexes).
    """
    # TODO: implement me
    return 200, [], _html.format(
        title = 'DEFAULT',
        head  = '',
        body  = 'DEFAULT'
    )


#=============================================================================
def handle_media( environ ):
    """
    Handle requests for media files.
    """
    # TODO: implement me
    return 200, [], _html.format(
        title = 'MEDIA',
        head  = '',
        body  = 'MEDIA'
    )


#=============================================================================
def handle_notfound( environ ):
    """
    Handle missing content requests.
    """
    return 404, [], make_error( 'Not Found', environ[ 'PATH_INFO' ] )


#=============================================================================
_handlers = {
    '?'      : handle_notfound,
    'assets' : handle_assets,
    'media'  : handle_media,
    None     : handle_default,
}


#=============================================================================
def make_error( title, *args, **kwargs ):
    """
    Makes an error document.
    """
    blocks = list()
    blocks.append( '<h1>{}</h1>'.format( title ) )
    if args:
        blocks.append( '<h4>{}</h4>'.format( args[ 0 ] ) )
        for arg in args[ 1 : ]:
            blocks.append( '<p>{}</p>'.format( arg ) )
    if kwargs:
        dl = list()
        for key, value in kwargs.items():
            dl.append( '<dt>{}</dt><dd>{}</dd>'.format( key, value ) )
        blocks.append( '<dl>\n{}\n</dl>'.format( '\n'.join( dl ) ) )
    return _html.format(
        title = title,
        head = '',
        body = '\n'.join( blocks )
    )


#=============================================================================
class RequestHandler( wsgiref.simple_server.WSGIRequestHandler ):
    """
    Custom request handler for the WSGI server.
    """


    #=========================================================================
    def log_message( self, format, *args ):
        """
        Handles logging messages.
        """

        # TODO: Determine what information comes in args for logging.
        #logging.info(
        #    '{REQUEST_METHOD}; {PATH_INFO}; {status}; {length}'.format(
        #        status = 
        #        length = 
        #        **environ
        #    )
        #)

        # Log the request.
        logging.info( format, args )


#=============================================================================
def application( environ, start_response ):
    """
    WSGI Application Entry Point
    """

    # Set the default request handler.
    handler = _handlers[ None ]

    # Get request path.
    path = environ.get( 'PATH_INFO', '' )

    # Expand request information for handlers.
    environ[ 'request.path' ]  = path.lstrip( '/' ).split( '/' )
    environ[ 'request.query' ] = urllib.parse.parse_qs(
        environ[ 'QUERY_STRING' ]
    )

    # Handler is specified.
    if environ[ 'request.path' ] and ( environ[ 'request.path' ][ 0 ] != '' ):

        # See if a handler is available.
        handler = _handlers.get(
            environ[ 'request.path' ][ 0 ],
            _handlers[ '?' ]
        )

    # Delegate to the request handler.
    status, headers, content = handler( environ )

    # Define default headers.
    default_headers = {
        'Content-Type'   : 'text/html',
        'Content-Length' : str( len( content ) ),
    }

    # Merge headers from handler.
    handler_headers = dict( headers )
    default_headers.update( handler_headers )
    merged_headers = [ ( k, v ) for k, v in default_headers.items() ]

    # Set the status string.
    status_string = '{} {}'.format( status, http_responses[ status ] )

    # Start the response.
    start_response( status_string, merged_headers )

    # Produce the content.
    if isinstance( content, bytes ):
        yield content
    else:
        yield bytes( content, 'utf-8' )


#=============================================================================
def run():
    """
    Run the web server until finished or interrupted.
    """

    # Construct a server.
    server = wsgiref.simple_server.make_server(
        _config[ 'address' ],
        _config[ 'port' ],
        application
    )

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
        default = _config[ 'address' ],
        help    = 'Bind server to specific address.'
    )
    parser.add_argument(
        '-d',
        '--docroot',
        default = _config[ 'docroot' ],
        help    = 'Set the root for serving content.'
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
        default = _config[ 'port' ],
        type    = int,
        help    = 'Bind server to specified port.'
    )

    # Parse the arguments.
    args = parser.parse_args( argv[ 1 : ] )

    # Update server configuration.
    _config.update( vars( args ) )

    # Try to run the server forever.
    try:

        # Run the server.
        result = run()

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

