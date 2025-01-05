import jsonschema
from jsonschema import validate
from datetime import datetime


def sanitize(payload, schema, type_casting=None):
    validate(instance=payload, schema=schema)
    check_for_dangerous_characters(payload)

    if not type_casting:
        return payload
    
    cleaned_payload = cast_to_type(payload, type_casting)
    return cleaned_payload
        
def cast_to_type(payload, mappings):
    clean_payload = dict()
    for field, type_cast in mappings.items():
        if type_cast == 'str':
            clean_payload[field] = str(payload[field])
        elif type_cast == 'int':
            clean_payload[field] = int(payload[field])
        elif type_cast == 'float':
            clean_payload[field] = float()(payload[field])
        elif type_cast == 'bool':
            clean_payload[field] = bool()(payload[field])
        else:
            raise ValueError('Unsupported type cast')   
    return clean_payload

def check_for_dangerous_characters(payload):
    forbidden_characters = ['$', '..', ';', '--']
    for field in payload.keys():
        if type(payload[field]) == str:
            for character in forbidden_characters:
                if character in payload[field]:
                    raise ValueError('Payload contains forbidden character')

def validate_with_datetime(schema, instance):
    BaseVal = jsonschema.Draft7Validator
    
    def is_datetime(checker, inst):
        return isinstance(inst, datetime)

    date_check = BaseVal.TYPE_CHECKER.redefine('datetime', is_datetime)
    Validator = jsonschema.validators.extend(BaseVal, type_checker=date_check)
    Validator(schema=schema).validate(instance)
