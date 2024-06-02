import unittest

from database.models.guild import Guild
from database.methods import guild


class TestAddAndEditGuild(unittest.TestCase):
    guild = None
    guild_data = {
        'tag': 'TST',
        'name': 'Test guild',
        'castle': "eggplant"
    }

    def setUp(self) -> None:
        new_guild = Guild(tag='TST', name='Test guild', castle="eggplant")
        guild.update([new_guild])
        self.guild = guild.get('TST')

    def test_add(self):
        for k, v in self.guild_data.items():
            self.assertEqual(self.guild.__getattribute__(k), v)

    def test_edit(self):
        self.guild.name = 'Updated test guild'
        self.guild_data['name'] = 'Updated test guild'
        guild.update([self.guild])
        for k, v in self.guild_data.items():
            self.assertEqual(self.guild.__getattribute__(k), v)

    def tearDown(self) -> None:
        guild.delete(self.guild)


if __name__ == '__main__':
    unittest.main()
