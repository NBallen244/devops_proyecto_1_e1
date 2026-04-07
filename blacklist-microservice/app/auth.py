from flask_jwt_extended import JWTManager, create_access_token
from datetime import timedelta

jwt = JWTManager()

def create_static_token(app_secret):
    with app_secret.app_context():
        token = create_access_token(
            identity='blacklist-service',
            expires_delta=False
        )
        return token

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return {
        'message': 'Token has expired',
        'error': 'token_expired'
    }, 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return {
        'message': 'Invalid token',
        'error': 'invalid_token'
    }, 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return {
        'message': 'Authorization token is required',
        'error': 'authorization_required'
    }, 401