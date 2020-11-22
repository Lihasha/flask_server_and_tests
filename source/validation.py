from marshmallow import fields, Schema, validate


class DictionaryPostSchema(Schema):
    key = fields.Str(required=True, validate=validate.Length(max=20))
    value = fields.Str(required=True, validate=validate.Length(max=100))


class DictionaryPutSchema(Schema):
    value = fields.Str(required=True, validate=validate.Length(max=100))


class DictionaryPutKeySchema(Schema):
    key = fields.Str(required=True, validate=validate.Length(max=20))


class DictionaryGetSchema(Schema):
    key = fields.Str(required=True, validate=validate.Length(max=20))


class DictionaryDeleteSchema(Schema):
    key = fields.Str(required=True, validate=validate.Length(max=20))
