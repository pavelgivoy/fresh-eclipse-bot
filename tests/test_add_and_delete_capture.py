import unittest
import datetime

from database.models.db_conn import DatabaseConnection
from database.methods import captures, history
from utils.game_staff.basic_hq import BASIC_HQ_NAME

cur_time = datetime.datetime.now()


class TestAddAndDeleteCapture(unittest.TestCase):
    def setUp(self) -> None:
        with DatabaseConnection() as session:
            capture_id = captures.get_empty_capture_id(session=session)
            code = captures.create_code(capture_id)
            location = captures.add(capture_id,
                                    code, "Collapsed Mine lvl.34",
                                    session=session)
            history.add_location(cur_time,
                                 location.id,
                                 {
                                     'name': "Collapsed Mine lvl.34",
                                     'result': "😴",
                                     'owner': BASIC_HQ_NAME
                                 },
                                 session=session)
            session.add(location)
            session.commit()

    def test_add(self):
        location_data = {
            'id': 4,
            'name': 'Collapsed Mine lvl.34',
            'code': 'unknown_4',
            'type': 'mine'
        }
        hist_data = {
            'id': 1,
            'date': cur_time,
            'capture_id': 4,
            'result': "😴",
            'owner': BASIC_HQ_NAME
        }
        location = captures.get(4)
        for k, v in location_data.items():
            self.assertEqual(location.__getattribute__(k), v)

        hist = history.get(1)
        for k, v in hist_data.items():
            self.assertEqual(hist.__getattribute__(k), v)

    def tearDown(self) -> None:
        with DatabaseConnection() as session:
            capture = captures.get(4, session=session)
            captures.delete(capture, True, session=session)
            session.commit()


if __name__ == '__main__':
    unittest.main()
