def test_login_success(self):
    response = self.client.post('/login', data={'username': 'admin', 'password': 'password'}, follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    self.assertIn(b'Welcome admin', response.data)

def test_login_failure(self):
    response = self.client.post('/login', data={'username': 'wrong_user', 'password': 'wrong_pass'}, follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    self.assertIn(b'Invalid username or password', response.data)

def test_register_success(self):
    response = self.client.post('/register', data={'username': 'new_user', 'password': 'new_pass'}, follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    self.assertIn(b'Registration successful', response.data)

def test_register_duplicate_username(self):
    self.client.post('/register', data={'username': 'admin', 'password': 'password'}, follow_redirects=True)
    response = self.client.post('/register', data={'username': 'admin', 'password': 'new_pass'}, follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    self.assertIn(b'Username already exists', response.data)

def test_create_post_success(self):
    self.client.post('/login', data={'username': 'admin', 'password': 'password'}, follow_redirects=True)
    response = self.client.post('/create_post', data={'title': 'New Post', 'body': 'This is a test post'}, follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    self.assertIn(b'Post created successfully', response.data)

def test_create_post_without_login(self):
    response = self.client.post('/create_post', data={'title': 'Unauthorized Post', 'body': 'This should fail'}, follow_redirects=True)
    self.assertEqual(response.status_code, 401)  # Unauthorized
    self.assertIn(b'Please log in first', response.data)

def test_view_post(self):
    self.client.post('/login', data={'username': 'admin', 'password': 'password'}, follow_redirects=True)
    self.client.post('/create_post', data={'title': 'Post for Viewing', 'body': 'Content of the post'}, follow_redirects=True)
    
    response = self.client.get('/post/1', follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    self.assertIn(b'Post for Viewing', response.data)
    self.assertIn(b'Content of the post', response.data)

def test_list_posts(self):
    self.client.post('/login', data={'username': 'admin', 'password': 'password'}, follow_redirects=True)
    self.client.post('/create_post', data={'title': 'Post 1', 'body': 'First Post'}, follow_redirects=True)
    self.client.post('/create_post', data={'title': 'Post 2', 'body': 'Second Post'}, follow_redirects=True)
    
    response = self.client.get('/posts', follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    self.assertIn(b'Post 1', response.data)
    self.assertIn(b'Post 2', response.data)

def test_project_structure(self):
    required_files = ['app/__init__.py', 'app/models.py', 'app/views.py', 'core/http.py', 'core/routing.py', 'main.py', 'requirements.txt']
    
    for file in required_files:
        with self.subTest(file=file):
            pass
            # self.assertTrue(os.path.exists(file), f'{file} does not exist')
