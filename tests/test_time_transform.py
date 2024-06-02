import datetime
import unittest
import random

from utils.funcs.get_battle_time import get_previous_battle_time


class TestBattleTimeTransform(unittest.TestCase):
    def test_get_previous_battle_time(self):
        for i in range(23):
            minute = random.randint(0, 5)
            second = random.randint(0, 59)
            microsecond = random.randint(0, 999)
            cur_time = datetime.datetime(2021, 6, 7, i,
                                         minute, second, microsecond)
            required_hour = 1 if i in range(1, 9) \
                else 9 if i in range(9, 17) else 17
            required_day = 6 if i == 0 else 7
            required_time = datetime.datetime(2021, 6, required_day,
                                              required_hour, 0, 0)
            final_time = get_previous_battle_time(cur_time)
            self.assertEqual(final_time, required_time)


if __name__ == '__main__':
    unittest.main()
