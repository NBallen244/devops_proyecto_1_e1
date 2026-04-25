import pytest
import os
import tempfile
from flask_jwt_extended import create_access_token
from app.models.blacklist import db, BlacklistedEmail
from application import create_app

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    
    # Create app with test configuration
    test_config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'JWT_SECRET_KEY': 'test-secret-key',
        'JWT_ACCESS_TOKEN_EXPIRES': False
    }
    
    app = create_app(test_config)
    
    with app.app_context():
        db.create_all()
        
    yield app
    
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def auth_token(app):
    with app.app_context():
        token = create_access_token(
            identity='test-user',
            expires_delta=False
        )
        return token

@pytest.fixture
def auth_headers(auth_token):
    return {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json'
    }

@pytest.fixture
def sample_blacklist_data():
    return {
        'email': 'test@example.com',
        'app_uuid': '550e8400-e29b-41d4-a716-446655440000',
        'blocked_reason': 'Spam activity detected'
    }

@pytest.fixture
def init_database(app):
    with app.app_context():
        db.session.query(BlacklistedEmail).delete()
        db.session.commit()
        yield db
        db.session.remove()

@pytest.fixture
def populate_database(app, init_database):
    with app.app_context():
        emails = [
            BlacklistedEmail(
                email='blocked1@example.com',
                app_uuid='550e8400-e29b-41d4-a716-446655440001',
                blocked_reason='Test reason 1',
                ip_address='127.0.0.1'
            ),
            BlacklistedEmail(
                email='blocked2@example.com',
                app_uuid='550e8400-e29b-41d4-a716-446655440002',
                blocked_reason='Test reason 2',
                ip_address='127.0.0.1'
            )
        ]
        
        for email in emails:
            db.session.add(email)
        db.session.commit()
        
        yield emails