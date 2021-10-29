from app import app
import unittest


class FlaskTest(unittest.TestCase):
    

    def test_health_data(self):
        tester  = app.test_client(self)
        response = tester.get("/healthz")
        response_data = response.data
        self.assertTrue(b'Healthy!' in response_data)

    def test_health_status(self):
        tester  = app.test_client(self)
        response = tester.get("/healthz")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_health_content_type(self):
        tester = app.test_client(self)
        response = tester.get("/healthz")
        self.assertEqual(response.content_type, "application/json")

    def test_health_content_custom_header(self):
        tester = app.test_client(self)
        response = tester.get("/healthz")
        self.assertEqual(response.headers['Status'], '200')


if __name__ == "__main__":
    unittest.main()