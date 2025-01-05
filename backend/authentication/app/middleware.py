"""
Middleware for Authentication Server

All request to the server pass through this middleware.

TODO:
 1. Only accept POST requests... maybe? But this means all 
    request need 'application/json' headers
 2. Similar to the Ops server, authenticate a service, and ensure it
    presents the JWT in the Authorization header each time.
"""
from logging import logger

class Middleware(logger):
    def access(self, resp, req, environ, request_time):
            logger = self.access_log
            logger.info(f'[{request_time}] {req.method} - {req.path}: {resp.status}')
