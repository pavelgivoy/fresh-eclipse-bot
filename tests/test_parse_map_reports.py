import pathlib
import unittest

from parsers.battle_reports import parse_map_report


class TestParseMapReport(unittest.TestCase):

    def test_parse_map_report(self):
        test_data = [{
            'name': 'Fort lvl.60',
            'result': 'too easily protected',
            'new_owner': None,
        }, {
            'name': 'Unfinished Mine lvl.46',
            'result': 'Easy win',
            'new_owner': 'Twinkle Pawn',
        }, {
            'name': 'Unfinished Mine lvl.20',
            'result': 'too easily protected',
            'new_owner': None,
        }, {
            'name': 'Outpost lvl.45',
            'result': 'too easily protected',
            'new_owner': 'Запретные силы',
        }, {
            'name': 'Ancient Ruins lvl.76',
            'result': 'easily protected',
            'new_owner': None,
        }, {
            'name': 'Abandoned Mine lvl.55',
            'result': 'too easily protected',
            'new_owner': None,
        }, {
            'name': 'Fort lvl.44',
            'result': 'too easily protected',
            'new_owner': None,
        }, {
            'name': 'Outpost lvl.37',
            'result': 'easily protected',
            'new_owner': 'Запретные силы',
        }, {
            'name': 'Unfinished Mine lvl.78',
            'result': 'too easily protected',
            'new_owner': 'Запретные силы',
        }, {
            'name': 'Ancient Ruins lvl.27',
            'result': 'Captured',
            'new_owner': 'Coarse Mercury',
        }, {
            'name': 'Abandoned Mine lvl.34',
            'result': 'too easily protected',
            'new_owner': None,
        }, {
            'name': 'Unfinished Mine lvl.41',
            'result': 'Easy win',
            'new_owner': 'Coarse Mercury',
        }, {
            'name': 'Trusted Ruins lvl.38',
            'result': 'too easily protected',
            'new_owner': None,
        }, {
            'name': 'Fort lvl.78',
            'result': 'too easily protected',
            'new_owner': None,
        },]

        p = pathlib.Path(__file__).parent
        with open(p / 'map_report.txt', 'r', encoding='utf-8') as f:
            read_file = f.read().strip()

        parsed_map_report = parse_map_report(read_file)

        for i in range(len(parsed_map_report)):
            for k, v in parsed_map_report[i].items():
                self.assertEqual(test_data[i][k], v)


if __name__ == '__main__':
    unittest.main()
