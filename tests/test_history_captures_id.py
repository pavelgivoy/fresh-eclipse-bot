import unittest
import datetime

from database.models.db_conn import DatabaseConnection
from database.methods import history

cur_time = datetime.datetime.now()


class TestAddHistory(unittest.TestCase):
    def setUp(self) -> None:
        with DatabaseConnection() as session:
            history.add_alliance(
                cur_time,
                3,
                {
                    'result': "😴",
                    'stock': 0,
                    'glory': 0
                },
                session=session)
            session.commit()

    def test_add(self):
        hist_data = {
            'id': 1,
            'date': cur_time,
            'capture_id': 3,
            'result': "😴",
            'stock': 0,
            'glory': 0
        }
        hist = history.get(1)
        for k, v in hist_data.items():
            self.assertEqual(hist.__getattribute__(k), v)

    def tearDown(self) -> None:
        with DatabaseConnection() as session:
            hist = history.get(1)
            session.delete(hist)
            session.commit()


if __name__ == '__main__':
    unittest.main()
