import pytest
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from application import application
from database import db


@pytest.fixture
def client():
    original_db_uri = application.config.get('SQLALCHEMY_DATABASE_URI')
    original_engine_opts = application.config.get('SQLALCHEMY_ENGINE_OPTIONS', {})
    
    application.config['TESTING'] = True
    application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    application.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    with application.app_context():
        db.create_all()
        
        with application.test_client() as test_client:
            yield test_client
        
        db.session.remove()
        db.drop_all()
    
    application.config['SQLALCHEMY_DATABASE_URI'] = original_db_uri
    application.config['SQLALCHEMY_ENGINE_OPTIONS'] = original_engine_opts


@pytest.fixture
def auth_token(client):
    response = client.post('/auth/login',
                          data=json.dumps({
                              'username': 'admin',
                              'password': 'admin123'
                          }),
                          content_type='application/json')
    data = json.loads(response.data)
    return data['access_token']


class TestHealthEndpoint:
    
    def test_health_check(self, client):
        response = client.get('/')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] is True


class TestLoginEndpoint:
    
    def test_login_exitoso(self, client):
        response = client.post('/auth/login',
                              data=json.dumps({
                                  'username': 'admin',
                                  'password': 'admin123'
                              }),
                              content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'access_token' in data
        assert data['token_type'] == 'Bearer'
        assert data['user'] == 'admin'
    
    def test_login_credenciales_invalidas(self, client):
        response = client.post('/auth/login',
                              data=json.dumps({
                                  'username': 'admin',
                                  'password': 'wrong_password'
                              }),
                              content_type='application/json')
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_login_sin_datos(self, client):
        response = client.post('/auth/login',
                              data=json.dumps({}),
                              content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_login_sin_username(self, client):
        response = client.post('/auth/login',
                              data=json.dumps({
                                  'password': 'admin123'
                              }),
                              content_type='application/json')
        
        assert response.status_code == 400
    
    def test_login_sin_password(self, client):
        response = client.post('/auth/login',
                              data=json.dumps({
                                  'username': 'admin'
                              }),
                              content_type='application/json')
        
        assert response.status_code == 400


class TestBlacklistEndpoint:
    
    def test_agregar_email_exitoso(self, client, auth_token):
        response = client.post('/blacklists',
                              data=json.dumps({
                                  'email': 'test@example.com',
                                  'app_uuid': '123e4567-e89b-12d3-a456-426614174000',
                                  'blocked_reason': 'Test reason'
                              }),
                              content_type='application/json',
                              headers={'Authorization': f'Bearer {auth_token}'})
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'message' in data
        assert 'test@example.com' in data['message']
    
    def test_agregar_sin_autenticacion(self, client):
        response = client.post('/blacklists',
                              data=json.dumps({
                                  'email': 'test@example.com',
                                  'app_uuid': '123e4567-e89b-12d3-a456-426614174000'
                              }),
                              content_type='application/json')
        
        assert response.status_code == 401
    
    def test_agregar_email_duplicado(self, client, auth_token):
        client.post('/blacklists',
                   data=json.dumps({
                       'email': 'duplicate@example.com',
                       'app_uuid': '123e4567-e89b-12d3-a456-426614174000'
                   }),
                   content_type='application/json',
                   headers={'Authorization': f'Bearer {auth_token}'})
        
        response = client.post('/blacklists',
                              data=json.dumps({
                                  'email': 'duplicate@example.com',
                                  'app_uuid': '123e4567-e89b-12d3-a456-426614174000'
                              }),
                              content_type='application/json',
                              headers={'Authorization': f'Bearer {auth_token}'})
        
        assert response.status_code == 409
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_agregar_email_invalido(self, client, auth_token):
        response = client.post('/blacklists',
                              data=json.dumps({
                                  'email': 'invalid-email',
                                  'app_uuid': '123e4567-e89b-12d3-a456-426614174000'
                              }),
                              content_type='application/json',
                              headers={'Authorization': f'Bearer {auth_token}'})
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_agregar_uuid_invalido(self, client, auth_token):
        response = client.post('/blacklists',
                              data=json.dumps({
                                  'email': 'test@example.com',
                                  'app_uuid': 'invalid-uuid'
                              }),
                              content_type='application/json',
                              headers={'Authorization': f'Bearer {auth_token}'})
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'UUID' in data['error'] or 'uuid' in data['error']
    
    def test_agregar_sin_email(self, client, auth_token):
        response = client.post('/blacklists',
                              data=json.dumps({
                                  'app_uuid': '123e4567-e89b-12d3-a456-426614174000'
                              }),
                              content_type='application/json',
                              headers={'Authorization': f'Bearer {auth_token}'})
        
        assert response.status_code == 400
    
    def test_agregar_sin_app_uuid(self, client, auth_token):
        response = client.post('/blacklists',
                              data=json.dumps({
                                  'email': 'test@example.com'
                              }),
                              content_type='application/json',
                              headers={'Authorization': f'Bearer {auth_token}'})
        
        assert response.status_code == 400
    
    def test_agregar_reason_muy_largo(self, client, auth_token):
        response = client.post('/blacklists',
                              data=json.dumps({
                                  'email': 'test@example.com',
                                  'app_uuid': '123e4567-e89b-12d3-a456-426614174000',
                                  'blocked_reason': 'a' * 256
                              }),
                              content_type='application/json',
                              headers={'Authorization': f'Bearer {auth_token}'})
        
        assert response.status_code == 400


class TestBlacklistEmailEndpoint:
    
    def test_consultar_email_bloqueado(self, client, auth_token):
        client.post('/blacklists',
                   data=json.dumps({
                       'email': 'blocked@example.com',
                       'app_uuid': '123e4567-e89b-12d3-a456-426614174000',
                       'blocked_reason': 'Spam'
                   }),
                   content_type='application/json',
                   headers={'Authorization': f'Bearer {auth_token}'})
        
        response = client.get('/blacklists/blocked@example.com',
                             headers={'Authorization': f'Bearer {auth_token}'})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['blacklisted'] is True
        assert data['email'] == 'blocked@example.com'
        assert data['reason'] == 'Spam'
        assert 'app_uuid' in data
    
    def test_consultar_email_no_bloqueado(self, client, auth_token):
        response = client.get('/blacklists/notblocked@example.com',
                             headers={'Authorization': f'Bearer {auth_token}'})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['blacklisted'] is False
        assert data['email'] == 'notblocked@example.com'
    
    def test_consultar_sin_autenticacion(self, client):
        response = client.get('/blacklists/test@example.com')
        
        assert response.status_code == 401
    
    def test_consultar_email_invalido(self, client, auth_token):
        response = client.get('/blacklists/invalid-email',
                             headers={'Authorization': f'Bearer {auth_token}'})
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

