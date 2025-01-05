"""
Base class for all Operations Services
"""
import os
import json

class BaseService:
    def __init__(self):
        pass

    @staticmethod
    def _get_environment_variable(variable_name: str, cast: str = None):
        try:
            if not cast:
                return os.environ[variable_name]
            else:
                if cast in ['list', 'tuple', 'dict']:
                    return json.loads(os.environ[variable_name])
                elif cast == 'int':
                    return int(os.environ[variable_name])
                elif cast == 'float':
                    return float(os.environ[variable_name])
                else:
                    raise TypeError(f'Unsupported type cast: {cast}')

        except KeyError:
            raise KeyError(f'Missing Service Configuration: {variable_name}')
