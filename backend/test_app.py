import unittest
from app import app

class Test(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()


    #test api news
    def test_get_news(self):
        response = self.client.get('/api/news')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)

        if data:
            article = data[0]
            self.assertIn('headline', article)
            self.assertIn('snippet', article)
            self.assertIn('abstract', article)
            self.assertIn('url', article)
            self.assertIn('image', article)

if __name__ == '__main__':
    unittest.main()