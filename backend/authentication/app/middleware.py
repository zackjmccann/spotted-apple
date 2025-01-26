"""
Middleware for Authentication Server

All request to the server pass through this middleware.

TODO:
 1. Only accept POST requests... maybe? But this means all 
    request need 'application/json' headers
 2. Similar to the Ops server, authenticate a service, and ensure it
    presents the JWT in the Authorization header each time.
"""
import json
import logging
from flask import current_app
from utilities.payload_handler import PayloadHandler
from werkzeug.wrappers import Request, Response


class Middleware:
   def __init__(self, wsgi_app):
      self.wsgi_app = wsgi_app
      self.logger = logging.getLogger(__name__)
   
   def __call__(self, environment, start_response):
      request = Request(environment)

      if 'Client-ID' not in request.headers:
         data = {'message': 'Bad Request.'}
         res = self.get_response(data=data, status=500)
         return res(environment, start_response)

      if not self._validate_client(request.headers):
         data = {'message': 'Unknown client.'}
         res = self.get_response(data=data, status=400)
         return res(environment, start_response)

      return self.wsgi_app(environment, start_response)

   def get_response(self, **kwargs):
      raw_data = kwargs.get('data', None)
      data = json.dumps(raw_data)
      content_type = kwargs.get('content_type', 'application/json')
      status = kwargs.get('status', 500)
      return Response(data, content_type=content_type, status=status)

   def _validate_client(self, headers):
      client = {
         'client_id': headers.get('Client-ID'),
         'client_name': headers.get('Client-Name'),
         'client_secret': headers.get('Client-Secret'),
         }

      payload = PayloadHandler(client, '/middleware/client')
      
      response = current_app.db.validate_client(payload.data)
      
      if not response['valid']:
         return False
      return True
