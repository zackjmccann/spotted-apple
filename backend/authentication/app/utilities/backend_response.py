"""
A Subclass of the flask.Response class.
"""
import json
from json.decoder import JSONDecodeError
from flask import Response

class BackendResponse(Response):
    def __init__(self, *args, **kwargs):
        response = self._parse_response(args)
        headers = self._update_headers(kwargs.get('headers', None))
        kwargs['content_type'] = 'application/json'
        kwargs['mimetype'] = 'application/json'
        kwargs['direct_passthrough'] = False
        kwargs['status'] = response['code']
        kwargs['headers'] = headers
        super().__init__(response['data'], **kwargs)

    def _parse_response(self, response):
        try:
            if len(response) == 0: # For Flask OPTIONS handling
                return {'code': 200, 'data': None}
            elif type(response) == tuple or type(response) == list:
                response = response[0]

            if type(response) == str:
                response = json.loads(response)
            
            return {
                'code': response['code'],
                'data': json.dumps(response['data']),
                }

        except JSONDecodeError:
            return {
                'code': response['code'],
                'data': None,
                }

    def _update_headers(self, headers):
        if headers is None:
            headers = {}
        headers.update({
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Access-Control-Allow-Credentials': 'true'
            })
        return headers