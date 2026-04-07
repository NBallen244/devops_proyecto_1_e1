from flask_marshmallow import Marshmallow
from marshmallow import fields, validate
from app.models.blacklist import BlacklistedEmail

ma = Marshmallow()

class BlacklistCreateSchema(ma.Schema):
    email = fields.Email(required=True)
    app_uuid = fields.String(required=True, validate=validate.Length(min=36, max=36))
    blocked_reason = fields.String(validate=validate.Length(max=255), allow_none=True)

class BlacklistResponseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BlacklistedEmail
        load_instance = True
        exclude = ('id', 'ip_address', 'created_at')

class BlacklistCheckSchema(ma.Schema):
    is_blacklisted = fields.Boolean()
    blocked_reason = fields.String(allow_none=True)