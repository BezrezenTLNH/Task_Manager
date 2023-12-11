from django import test


class IndexViewTestCase(test.TestCase):

    def test_index_url(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)