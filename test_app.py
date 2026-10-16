import unittest
import os
import sqlite3

from app import app, DATABASE, init_db, get_db


class TestAuthAPI(unittest.TestCase):
    def setUp(self):
        """Set up test client and test database"""
        app.config['TESTING'] = True
        self.client = app.test_client()
        
        # Use a test database
        self.test_db = 'test_users.db'
        app.DATABASE = self.test_db
        
        # Initialize test database
        init_db()

    def tearDown(self):
        """Clean up test database"""
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_register_user(self):
        """Test user registration"""
        response = self.client.post('/register',
                                     json={'username': 'testuser', 'password': 'testpass'},
                                     content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['message'], 'User registered successfully')

    def test_register_duplicate_user(self):
        """Test registering duplicate username"""
        # Register first user
        self.client.post('/register',
                        json={'username': 'testuser', 'password': 'testpass'},
                        content_type='application/json')
        
        # Try to register same username again
        response = self.client.post('/register',
                                    json={'username': 'testuser', 'password': 'testpass'},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 409)
        data = response.get_json()
        self.assertEqual(data['error'], 'Username already exists')

    def test_register_missing_fields(self):
        """Test registration with missing fields"""
        response = self.client.post('/register',
                                    json={'username': 'testuser'},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data['error'], 'Username and password are required')

    def test_login_success(self):
        """Test successful login"""
        # Register a user first
        self.client.post('/register',
                        json={'username': 'testuser', 'password': 'testpass'},
                        content_type='application/json')
        
        # Login with correct credentials
        response = self.client.post('/login',
                                    json={'username': 'testuser', 'password': 'testpass'},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['message'], 'Login successful')
        self.assertEqual(data['username'], 'testuser')
        self.assertIn('user_id', data)

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        # Register a user
        self.client.post('/register',
                        json={'username': 'testuser', 'password': 'testpass'},
                        content_type='application/json')
        
        # Try to login with wrong password
        response = self.client.post('/login',
                                    json={'username': 'testuser', 'password': 'wrongpass'},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertEqual(data['error'], 'Invalid username or password')

    def test_login_nonexistent_user(self):
        """Test login with non-existent user"""
        response = self.client.post('/login',
                                    json={'username': 'nonexistent', 'password': 'testpass'},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertEqual(data['error'], 'Invalid username or password')

    def test_login_missing_fields(self):
        """Test login with missing fields"""
        response = self.client.post('/login',
                                    json={'username': 'testuser'},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data['error'], 'Username and password are required')


if __name__ == '__main__':
    unittest.main()
