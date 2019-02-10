from factory import app
import unittest


class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        # Wrong key:
        # app.config['CSRF_ENABLED'] = False
        # Right key:
        app.config['WTF_CSRF_ENABLED'] = False

    # Ensure that flask was set up correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure that the login page loads correctly
    def test_login_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/signin', content_type='html/text')
        self.assertTrue(b'Sign In' in response.data)

    # Ensure login behaves correctly give the correct credentials
    def test_correct_login(self):
        tester = app.test_client(self)
        response = tester.post(
                '/signin',
                data=dict(email="test@test.com", password="aoho0Eeg"),
                follow_redirects = True)
        self.assertIn(b'Welcome test@test.com\'s profile page', response.data)


    # Ensure login behaves correctly give the in incorrect credentials
    def test_incorrect_login(self):
        tester = app.test_client(self)
        response = tester.post(
                '/signin',
                data=dict(email="test@test.com", password="wrong"),
                follow_redirects = True
                )
        self.assertIn(b'Invalid e-mail or password', response.data)

    # Ensure logout behaves correctly give the correct credentials
    def test_logout(self):
        tester = app.test_client(self)
        tester.post(
                '/signin',
                data=dict(email="test@test.com", password="aoho0Eeg"),
                follow_redirects = True
                )
        response = tester.get('/signout', follow_redirects=True)
        self.assertIn(b'Welcome to APP', response.data)

    # Ensure that the main page require login
    def test_main_route_requires_login(self):
        tester = app.test_client(self)
        response = tester.get('/showdelivery', follow_redirects=True)
        self.assertTrue(b'Sign In' in response.data)


    # Ensure Adding new item, behaves correctly give the correct credentials
    def test_add_item(self):
        tester = app.test_client(self)
        tester.post(
                '/signin',
                data=dict(email="test@test.com", password="aoho0Eeg"),
                follow_redirects = True
                )
        tester.post('/delivery', data=dict(name="test", phone1="1234567890", phone2="1234567890", email="",city="test", address="test", floor="1", apartment="1", address_comments="test", order_comments="test", number_of_pieces="1", time_of_pickup="2000-01-01 00:00:00", time_of_delivery="2000-01-01 00:00:00", lang="ENG", condition="Use"),
                follow_redirects = True
                )
        response = tester.get('/showdelivery', follow_redirects=True)
        self.assertIn(b'1234567890', response.data)


if __name__ == '__main__':
    unittest.main()
