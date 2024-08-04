import os
import streamlit as st
from http.server import BaseHTTPRequestHandler, HTTPServer


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # auth_code will set to either be the error or None
        self.server.auth_code = self.server.error = None 
        try:
            self.server.state = 'state' # TODO: Get state in redirect request
            self.server.auth_code = 'auth_code' # TODO: Get auth_code in redirect request
        except AuthenticationError as error:
            self.server.error = error


        self.send_response(200)
        message = bytes('Connection Successful', 'utf8')
        self.send_header('Content-type','text/plain; charset=utf-8')
        self.send_header('Content-length', str(len(message)))
        self.end_headers()
        
        if self.server.error:
            return self.server.error
        else:
            self.wfile.write(message)
            self.wfile.flush()
            return

class LocalHTTPServer(HTTPServer):
    timeout = 10
    allow_reuse_address = True

    def handle_timeout(self):
        raise TimeoutError(f'Local Server did not receive a request after {self.timeout} seconds.')    

def create_local_http_server(port, handler=RequestHandler):
    host = '127.0.0.1'
    return LocalHTTPServer((host, port), handler)

def get_host_port(network_location):
    """ 
    Retrieve the host and port from the provided network location (i.e.,
    a string representing the network location).

    The host is returned as a string, and the port is returned as an int.
    """
    if ":" in network_location:
        host, port = network_location.split(":", 1)
        port = int(port)
    else:
        host = network_location
        port = None

    return host, port

def handle_app_request(): # TODO: Maybe change the name here?
    if validate_email_input():
        if check_if_user_has_app_access():
            st.session_state['app_access_request'] = 'granted'
        else:
            st.session_state['app_access_request'] = 'pending'
    else:
        st.session_state['app_access_request'] = 'invalid'

def check_if_user_has_app_access():
    #TODO: Add check >> store users with development access to redis and validate
    if st.session_state['user_email'] == os.getenv('SPOTIFY_ADMIN'):
        return True
    else:
        return False
