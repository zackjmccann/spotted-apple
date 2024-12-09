"""
A Subclass of the flask.Response class.
"""
import json
from flask import Response

class BackendResponse(Response):
    def __init__(self, *args, **kwargs):
        response = self._parse_response(args[0])
        kwargs['content_type'] = 'application/json'
        kwargs['mimetype'] = 'application/json'
        kwargs['direct_passthrough'] = False
        kwargs['status'] = response['code']
        super().__init__(response['data'], **kwargs)

    def _parse_response(self, response):
        if type(response) == str:
            response = json.loads(response)
        return {
            'code': response['code'],
            'data': json.dumps(response['data'])
            }
