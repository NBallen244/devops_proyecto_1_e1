from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from app.models.blacklist import db, BlacklistedEmail
from app.schemas.blacklist_schema import BlacklistCreateSchema, BlacklistCheckSchema

class BlacklistResource(Resource):
    @jwt_required()
    def delete(self):
        try:
            db.session.query(BlacklistedEmail).delete()
            db.session.commit()
            return {'message': 'Base de datos limpiada exitosamente', 'status': 'success'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': 'Error interno del servidor', 'status': 'error'}, 500

    @jwt_required()
    def post(self):
        try:
            schema = BlacklistCreateSchema()
            data = schema.load(request.get_json())
            
            client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
            
            existing_email = BlacklistedEmail.query.filter_by(email=data['email']).first()
            if existing_email:
                return {
                    'message': 'El email ya está en la lista negra',
                    'status': 'error'
                }, 409
            
            blacklisted_email = BlacklistedEmail(
                email=data['email'],
                app_uuid=data['app_uuid'],
                blocked_reason=data.get('blocked_reason'),
                ip_address=client_ip
            )
            
            db.session.add(blacklisted_email)
            db.session.commit()
            
            return {
                'message': 'Email agregado a la lista negra exitosamente',
                'status': 'success'
            }, 201
            
        except ValidationError as e:
            return {'errors': e.messages}, 400
        except IntegrityError:
            db.session.rollback()
            return {
                'message': 'Error al agregar el email a la lista negra',
                'status': 'error'
            }, 409
        except Exception as e:
            db.session.rollback()
            return {
                'message': 'Error interno del servidor',
                'status': 'error'
            }, 500

class BlacklistCheckResource(Resource):
    @jwt_required()
    def get(self, email):
        try:
            blacklisted_email = BlacklistedEmail.query.filter_by(email=email).first()
            
            if blacklisted_email:
                schema = BlacklistCheckSchema()
                return schema.dump({
                    'is_blacklisted': True,
                    'blocked_reason': blacklisted_email.blocked_reason
                }), 200
            else:
                schema = BlacklistCheckSchema()
                return schema.dump({
                    'is_blacklisted': False,
                    'blocked_reason': None
                }), 200
                
        except Exception as e:
            return {
                'message': 'Error interno del servidor',
                'status': 'error'
            }, 500

class BlacklistResetResource(Resource):
    @jwt_required()
    def delete(self):
        try:
            db.session.query(BlacklistedEmail).delete()
            db.session.commit()
            return {'message': 'Base de datos limpiada exitosamente', 'status': 'success'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': 'Error interno del servidor', 'status': 'error'}, 500
