import models
import jsonschema
from datetime import datetime
from flask import current_app

class Payload:
    def __init__(self, data: dict, endpoint: str):
        self.raw_data = data
        self.raw_endpoint = endpoint
        self.endpoint = self._format_endpoint()
        self.schema = self._get_schema()
        self.type_mappings = self._type_mappings()
        self.data = self.sanitize()

    def sanitize(self) -> dict:
        """
        Sanize a payload according to the endpoint

        Payload are validated according to a jsonschema configuration, then
        cast to mapped types, and finally parsed for dangerous characters.
        """
        self.validate()
        self.check_for_dangerous_characters()

        if not self.type_mappings:
            return self.raw_data

        return self.cast_to_type()

    def _format_endpoint(self) -> str:
        return self.raw_endpoint.replace('/', '_').strip('_')

    def _get_schema(self):
        schema = models.schemas.get(self.endpoint)
        try:
            assert schema
            return schema
        except AssertionError:
            current_app.logger.critical(f'No validation schema provided by endpoint {self.raw_endpoint}')
            return None

    def _type_mappings(self):
        return models.type_mappings.get(self.endpoint, None)

    def cast_to_type(self):
        clean_payload = dict()
        for field, type_cast in self.type_mappings.items():
            if type_cast == 'str':
                clean_payload[field] = str(self.raw_data[field])
            elif type_cast == 'int':
                clean_payload[field] = int(self.raw_data[field])
            elif type_cast == 'float':
                clean_payload[field] = float(self.raw_data[field])
            elif type_cast == 'bool':
                clean_payload[field] = bool(self.raw_data[field]) # TODO: Check this one
            else:
                raise ValueError('Unsupported type cast')   
        return clean_payload

    def check_for_dangerous_characters(self):
        forbidden_characters = ['$', '..', ';', '--']
        for field in self.raw_data.keys():
            if type(self.raw_data[field]) == str:
                for character in forbidden_characters:
                    if character in self.raw_data[field]:
                        raise ValueError('Payload contains forbidden character')

    def validate(self):
        schemas_with_datetime = [] # TODO: Make this dynamic

        if self.schema in schemas_with_datetime:
            BaseVal = jsonschema.Draft7Validator
                
            def is_datetime(checker, inst):
                return isinstance(inst, datetime)

            date_check = BaseVal.TYPE_CHECKER.redefine('datetime', is_datetime)
            Validator = jsonschema.validators.extend(BaseVal, type_checker=date_check)
            return Validator(schema=self.schema).validate(self.raw_data)

        else:
            jsonschema.validate(self.raw_data, self.schema)
