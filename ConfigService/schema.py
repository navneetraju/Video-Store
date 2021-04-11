import json
import jsonschema
import json
from jsonschema import validate

class SchemaValidator:
    def get_database_schema(self):
        with open('database_config_schema.json', 'r') as file:
            database_schema = json.load(file)
        return database_schema

    def get_mapping_schema(self):
        with open('mapping_config_schema.json', 'r') as file:
            mapping_schema = json.load(file)
        return mapping_schema
    def __init__(self):
        self.database_schema = self.get_database_schema()
        self.mapping_schema = self.get_mapping_schema()

    def validate_json(self,json_data,type):
        if type=="DATA":         
            try:
                validate(instance=json_data, schema=self.database_schema)
            except jsonschema.exceptions.ValidationError as err:
                return False, (str(err).split("\n\n"))[0]

            message = "Given JSON data is Valid"
            return True, message
        elif type == "MAPPING":
            try:
                validate(instance=json_data, schema=self.mapping_schema)
            except jsonschema.exceptions.ValidationError as err:
                return False, (str(err).split("\n\n"))[0]

            message = "Given JSON data is Valid"
            return True, message