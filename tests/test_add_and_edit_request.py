import unittest

from database.methods import request


class TestAddAndEditRequest(unittest.TestCase):
    request = None
    request_data = {
        'id': 1,
        'text': 'test request'
    }

    def setUp(self) -> None:
        request.add('test request')
        self.request = request.get(1)

    def test_add(self):
        for k, v in self.request_data.items():
            self.assertEqual(self.request.__getattribute__(k), v)

    def test_edit(self):
        self.request_data['text'] = 'test edited request'
        request.edit(self.request, 'test edited request')
        self.request = request.get(1)
        for k, v in self.request_data.items():
            self.assertEqual(self.request.__getattribute__(k), v)

    def tearDown(self) -> None:
        request.delete(self.request)


if __name__ == '__main__':
    unittest.main()
