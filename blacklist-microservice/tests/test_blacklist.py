import pytest
import json
from faker import Faker
from app.models.blacklist import BlacklistedEmail

fake = Faker()

class TestBlacklistPost:
    
    def test_add_email_to_blacklist_success(self, client, auth_headers, init_database):
        data = {
            'email': fake.email(),
            'app_uuid': '550e8400-e29b-41d4-a716-446655440000',
            'blocked_reason': 'Test spam detection'
        }
        
        response = client.post('/blacklists',
                              json=data,
                              headers=auth_headers)
        
        assert response.status_code == 201
        json_data = response.get_json()
        assert json_data['status'] == 'success'
        assert 'agregado a la lista negra exitosamente' in json_data['message']
    
    def test_add_duplicate_email_returns_conflict(self, client, auth_headers, init_database):
        email = fake.email()
        data = {
            'email': email,
            'app_uuid': '550e8400-e29b-41d4-a716-446655440000',
            'blocked_reason': 'Test reason'
        }
        
        response1 = client.post('/blacklists',
                               json=data,
                               headers=auth_headers)
        assert response1.status_code == 201
        
        response2 = client.post('/blacklists',
                               json=data,
                               headers=auth_headers)
        
        assert response2.status_code == 409
        json_data = response2.get_json()
        assert json_data['status'] == 'error'
        assert 'ya está en la lista negra' in json_data['message']
    
    def test_add_email_with_invalid_format(self, client, auth_headers, init_database):
        data = {
            'email': 'invalid-email-format',
            'app_uuid': '550e8400-e29b-41d4-a716-446655440000',
            'blocked_reason': 'Test'
        }
        
        response = client.post('/blacklists',
                              json=data,
                              headers=auth_headers)
        
        assert response.status_code == 400
        json_data = response.get_json()
        assert 'errors' in json_data
        assert 'email' in json_data['errors']
    
    def test_add_email_with_invalid_uuid(self, client, auth_headers, init_database):
        data = {
            'email': fake.email(),
            'app_uuid': 'invalid-uuid',
            'blocked_reason': 'Test'
        }
        
        response = client.post('/blacklists',
                              json=data,
                              headers=auth_headers)
        
        assert response.status_code == 400
        json_data = response.get_json()
        assert 'errors' in json_data
        assert 'app_uuid' in json_data['errors']
    
    def test_add_email_without_auth_token(self, client, init_database):
        data = {
            'email': fake.email(),
            'app_uuid': '550e8400-e29b-41d4-a716-446655440000',
            'blocked_reason': 'Test'
        }
        
        response = client.post('/blacklists', json=data)
        
        assert response.status_code == 401
        json_data = response.get_json()
        assert 'Authorization token is required' in json_data['message']
    
    def test_add_email_with_missing_required_fields(self, client, auth_headers, init_database):
        data = {'email': fake.email()}
        
        response = client.post('/blacklists',
                              json=data,
                              headers=auth_headers)
        
        assert response.status_code == 400
        json_data = response.get_json()
        assert 'errors' in json_data
        assert 'app_uuid' in json_data['errors']
    
    def test_add_email_without_blocked_reason(self, client, auth_headers, init_database):
        data = {
            'email': fake.email(),
            'app_uuid': '550e8400-e29b-41d4-a716-446655440000'
        }
        
        response = client.post('/blacklists',
                              json=data,
                              headers=auth_headers)
        
        assert response.status_code == 201
        json_data = response.get_json()
        assert json_data['status'] == 'success'


class TestBlacklistGet:
    
    def test_check_blacklisted_email_exists(self, client, auth_headers, populate_database):
        response = client.get('/blacklists/blocked1@example.com',
                            headers=auth_headers)
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['is_blacklisted'] is True
        assert json_data['blocked_reason'] == 'Test reason 1'
    
    def test_check_email_not_blacklisted(self, client, auth_headers, init_database):
        response = client.get('/blacklists/notblocked@example.com',
                            headers=auth_headers)
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['is_blacklisted'] is False
        assert json_data['blocked_reason'] is None
    
    def test_check_email_without_auth_token(self, client, init_database):
        response = client.get('/blacklists/test@example.com')
        
        assert response.status_code == 401
        json_data = response.get_json()
        assert 'Authorization token is required' in json_data['message']
    
    def test_check_multiple_emails_sequentially(self, client, auth_headers, populate_database):
        emails_to_check = [
            ('blocked1@example.com', True, 'Test reason 1'),
            ('blocked2@example.com', True, 'Test reason 2'),
            ('notblocked@example.com', False, None)
        ]
        
        for email, expected_blacklisted, expected_reason in emails_to_check:
            response = client.get(f'/blacklists/{email}',
                                headers=auth_headers)
            assert response.status_code == 200
            json_data = response.get_json()
            assert json_data['is_blacklisted'] == expected_blacklisted
            assert json_data['blocked_reason'] == expected_reason


class TestBlacklistDelete:
    
    def test_delete_all_blacklisted_emails_success(self, client, auth_headers, populate_database):
        response_before = client.get('/blacklists/blocked1@example.com',
                                    headers=auth_headers)
        assert response_before.get_json()['is_blacklisted'] is True
        
        response = client.delete('/blacklists', headers=auth_headers)
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['status'] == 'success'
        assert 'Base de datos limpiada exitosamente' in json_data['message']
        
        response_after = client.get('/blacklists/blocked1@example.com',
                                   headers=auth_headers)
        assert response_after.get_json()['is_blacklisted'] is False
    
    def test_delete_empty_database_success(self, client, auth_headers, init_database):
        response = client.delete('/blacklists', headers=auth_headers)
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['status'] == 'success'
        assert 'Base de datos limpiada exitosamente' in json_data['message']
    
    def test_delete_without_auth_token(self, client, populate_database):
        response = client.delete('/blacklists')
        
        assert response.status_code == 401
        json_data = response.get_json()
        assert 'Authorization token is required' in json_data['message']
    
    def test_delete_and_verify_all_emails_removed(self, client, auth_headers, populate_database, app):
        response = client.delete('/blacklists', headers=auth_headers)
        assert response.status_code == 200
        
        with app.app_context():
            count = BlacklistedEmail.query.count()
            assert count == 0