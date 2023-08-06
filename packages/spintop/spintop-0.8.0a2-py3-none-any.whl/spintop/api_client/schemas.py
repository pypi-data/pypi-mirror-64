from marshmallow import Schema, fields

class ManyTestsSchema(Schema):
    tests = fields.List(fields.Dict())
    
tests_schema = ManyTestsSchema()