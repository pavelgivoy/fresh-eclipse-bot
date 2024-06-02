import pathlib
import unittest

from parsers.battle_reports import parse_hq_report


class TestParseHQReport(unittest.TestCase):

    def test_parse_hq_report(self):
        test_data = [{
            'name': 'Alert Eyes',
            'result': 'too easily defended',
            'stock': 0,
            'glory': 0,
        }, {
            'name': 'Creepy Balboa',
            'result': 'too easily defended',
            'stock': 0,
            'glory': 0,
        }, {
            'name': 'Twinkle Pawn',
            'result': 'too easily defended',
            'stock': 0,
            'glory': 0,
        }, {
            'name': 'General Master',
            'result': 'too easily defended',
            'stock': 0,
            'glory': 0,
        }, {
            'name': 'Exalted Centurion',
            'result': 'too easily defended',
            'stock': 0,
            'glory': 0,
        }, {
            'name': 'Coarse Mercury',
            'result': 'too easily defended',
            'stock': 0,
            'glory': 0,
        },]

        p = pathlib.Path(__file__).parent
        with open(p / 'hq_report.txt', 'r', encoding='utf-8') as f:
            read_file = f.read().strip()

        parsed_hq_report = parse_hq_report(read_file)

        for i in range(len(parsed_hq_report)):
            for k, v in parsed_hq_report[i].items():
                self.assertEqual(test_data[i][k], v)


if __name__ == '__main__':
    unittest.main()
