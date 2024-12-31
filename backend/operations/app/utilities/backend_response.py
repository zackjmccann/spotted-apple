"""
A Subclass of the flask.Response class.
"""
import json
from json.decoder import JSONDecodeError
from flask import Response

class BackendResponse(Response):
    def __init__(self, *args, **kwargs):
        response_args = self._handle_args(args)
        response_kwargs = self._handle_kwargs(kwargs)
        response_kwargs['status'] = response_args['code']
        super().__init__(response_args['data'], **response_kwargs)

    def _handle_args(self, args):
        response = None
        try:
            if type(args) == tuple:
                try:
                    response = args[0]
                except IndexError:
                    response = None
            if response is None or len(response) == 0: # For Flask OPTIONS handling
                return {'code': 200, 'data': None}
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

    def _handle_kwargs(self, kwargs):
        headers = self._update_headers(kwargs.get('headers', None))
        if 'mimetype' in kwargs.keys():
            del kwargs['mimetype']
        kwargs['content_type'] = 'application/json'
        kwargs['direct_passthrough'] = False
        kwargs['headers'] = headers
        return kwargs

    def _update_headers(self, headers):
        if headers is None:
            headers = {}
        headers.update({
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            })
        return headers
