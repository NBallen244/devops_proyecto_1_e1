import pytest
from flask_jwt_extended import decode_token

class TestAuthentication:
    
    def test_generate_token_success(self, client, app):
        response = client.post('/token')
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert 'access_token' in json_data
        assert isinstance(json_data['access_token'], str)
        
        with app.app_context():
            decoded = decode_token(json_data['access_token'])
            assert decoded['sub'] == 'blacklist-service'
    
    def test_generated_token_works_for_protected_endpoints(self, client, init_database):
        token_response = client.post('/token')
        token = token_response.get_json()['access_token']
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'email': 'test@example.com',
            'app_uuid': '550e8400-e29b-41d4-a716-446655440000',
            'blocked_reason': 'Test'
        }
        
        response = client.post('/blacklists', json=data, headers=headers)
        assert response.status_code == 201
    
    def test_invalid_token_rejected(self, client):
        headers = {
            'Authorization': 'Bearer invalid.token.here',
            'Content-Type': 'application/json'
        }
        
        response = client.get('/blacklists/test@example.com', headers=headers)
        
        assert response.status_code == 401
        json_data = response.get_json()
        assert 'Invalid token' in json_data['message']
    
    def test_missing_token_rejected(self, client):
        response = client.get('/blacklists/test@example.com')
        
        assert response.status_code == 401
        json_data = response.get_json()
        assert 'Authorization token is required' in json_data['message']
    
    def test_malformed_authorization_header_rejected(self, client):
        headers = {
            'Authorization': 'InvalidFormat token123',
            'Content-Type': 'application/json'
        }
        
        response = client.get('/blacklists/test@example.com', headers=headers)
        
        assert response.status_code == 401