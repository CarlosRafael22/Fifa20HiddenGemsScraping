import pytest
from players import *


# class TestDatabasePlayer:
#     def test_init(self):
#         player = FIFADatabasePlayer('John', 18, 'GK', 65, 85, 2022)
#         assert PlayerDatabase.get_players_amount() == 1
#         assert player.growth == 20
#         assert player.__str__() == '65 overall -> 20 growth'
#         assert player.__repr__() == 'John'


class TestPlayerDatabase:
    def test_init(self):
        database = PlayerDatabase()
        assert database.players_amount == 0
        assert len(database.defenders) == 0

    def test_players_amount_encapsulation(self):
        ''' Test whether its thrown an Exception when trying to modify players_amount directly'''
        database = PlayerDatabase()
        assert database.players_amount == 0

        with pytest.raises(Exception) as excp:
            database.players_amount = 5
    
    test_data = [
        (Attacker, PlayerDatabase.attackers),
        (Defender, PlayerDatabase.defenders),
        (Midfielder, PlayerDatabase.midfielders),
        (GoalKeeper, PlayerDatabase.goalkeepers)
    ]
    @pytest.mark.parametrize("cls,cls_array", test_data)
    def test_add_player_for_classes_created(self, cls, cls_array):
        previous_amount = PlayerDatabase.get_players_amount()
        player = cls('John', 18, 'ST', 65, 85, 2022)

        assert type(player).__name__ == cls.__name__
        assert PlayerDatabase.get_players_amount() == previous_amount + 1
        assert len(cls_array) == 1

    @pytest.mark.parametrize("cls,cls_array", test_data)
    def test_add_player_to_correct_array(self, cls, cls_array):
        player = FIFAPlayer('John', 18, 'ST', 65, 85, 2022)
        previous_amount = len(cls_array)
        PlayerDatabase.add_player_to_correct_array(player, cls.__name__)
        # import pdb; pdb.set_trace()

        # assert PlayerDatabase.get_players_amount() == 1
        assert len(cls_array) == previous_amount + 1
    
    def test_add_player_raises_exception_for_FIFAPlayer(self):
        player = FIFAPlayer('John', 18, 'ST', 65, 85, 2022)
        with pytest.raises(Exception):
            PlayerDatabase.add_player(player)

    # def test_add_player_raises_exception_for_FIFADatabasePlayer(self):
    #     player = FIFADatabasePlayer('John', 18, 'ST', 65, 85, 2022)
    #     with pytest.raises(Exception) as excp_info:
    #         PlayerDatabase.add_player(player)
    #         assert str(excp_info) == 'Cant receive FIFADatabasePlayer class only its inheritance'

    def test_clear_database(self):
        # previous_amount = PlayerDatabase.get_players_amount()
        # previous_attackers = len(PlayerDatabase.attackers)
        # import pdb; pdb.set_trace()
        PlayerDatabase.clear_database()

        assert PlayerDatabase.get_players_amount() == 0
        assert len(PlayerDatabase.attackers) == 0
        assert len(PlayerDatabase.midfielders) == 0
        assert len(PlayerDatabase.defenders) == 0
        assert len(PlayerDatabase.goalkeepers) == 0

    def pre_populate_attackers(self):
        # Cleaning all the attackers from the list
        PlayerDatabase.clear_database()

        Attacker('John Newton', 18, 'ST', 63, 81, 2023)
        Attacker('James Ruud', 17, 'ST', 65, 85, 2022)
        Attacker('James Harrison', 19, 'ST', 60, 73, 2024)
        Attacker('Javier Porto', 16, 'ST', 65, 80, 2022)
        Attacker('Clarence Williams', 18, 'ST', 66, 77, 2021)
        Attacker('Patrick Ford', 19, 'ST', 65, 82, 2021)

    def test_filter_equals(self):
        self.pre_populate_attackers()
        attackers = PlayerDatabase.attackers

        filtered_players = PlayerDatabase.filter_equals('age', 18, attackers)
        assert len(filtered_players) == 2
        assert filtered_players[0].name == 'John Newton'
        assert filtered_players[1].name == 'Clarence Williams'

    def test_filter_gte(self):
        self.pre_populate_attackers()
        attackers = PlayerDatabase.attackers

        filtered_players = PlayerDatabase.filter_gte('age', 19, attackers)
        assert len(filtered_players) == 2
        assert filtered_players[0].name == 'James Harrison'
        assert filtered_players[1].name == 'Patrick Ford'

    def test_filter_lt(self):
        self.pre_populate_attackers()
        attackers = PlayerDatabase.attackers

        filtered_players = PlayerDatabase.filter_lt('age', 18, attackers)
        assert len(filtered_players) == 2
        assert filtered_players[0].name == 'James Ruud'
        assert filtered_players[1].name == 'Javier Porto'

    def test_filter_contains(self):
        self.pre_populate_attackers()
        attackers = PlayerDatabase.attackers

        filtered_players = PlayerDatabase.filter_contains('name', 'James', attackers)
        assert len(filtered_players) == 2
        assert filtered_players[0].name == 'James Ruud'
        assert filtered_players[1].name == 'James Harrison'

    filter_test_data = [
        ('age__gte', 19, ['James Harrison', 'Patrick Ford']),
        ('age__lt', 18, ['James Ruud', 'Javier Porto']),
        ('age', 18, ['John Newton', 'Clarence Williams']),
        ('name__contains', 'James', ['James Ruud', 'James Harrison']),
        ('name', 'James', []),
    ]
    @pytest.mark.parametrize("query,value,expected_array", filter_test_data)
    def test_filter_players(self, query, value, expected_array):
        self.pre_populate_attackers()
        attackers = PlayerDatabase.attackers

        query_dict = { query: value }
        filtered_players = PlayerDatabase.filter_players(attackers, **query_dict)
        players_names = [player.name for player in filtered_players]
        assert len(filtered_players) == len(expected_array)
        assert players_names == expected_array
    
    filter_test_data = [
        ('age__gte', 'age', 'gte'),
        ('age__lt', 'age', 'lt'),
        ('age', 'age', None),
        ('name__contains', 'name', 'contains')
    ]
    @pytest.mark.parametrize("query,expected_attribute,expected_lookup", filter_test_data)
    def test_get_attribute_and_lookup_from_query_string(self, query, expected_attribute, expected_lookup):
        (attribute, lookup) = PlayerDatabase.get_attribute_and_lookup_from_query_string(query)
        assert attribute == expected_attribute
        assert lookup == expected_lookup


class TestCreateFIFAPlayer:
    ''' Test the creation of GoalKeeper, Defender, Midfielder or Attacker with method crate_FIFA_player '''

    creation_data = [
        ({
            'name': 'John',
            'age': 18,
            'position': 'GK',
            'overall': 65,
            'potential': 85,
            'contract_until': 2022,
        }, GoalKeeper),
        ({
            'name': 'John',
            'age': 18,
            'position': 'ST',
            'overall': 65,
            'potential': 85,
            'contract_until': 2022,
        }, Attacker),
        ({
            'name': 'John',
            'age': 18,
            'position': 'CM',
            'overall': 65,
            'potential': 85,
            'contract_until': 2022,
        }, Midfielder),
        ({
            'name': 'John',
            'age': 18,
            'position': 'CB',
            'overall': 65,
            'potential': 85,
            'contract_until': 2022,
        }, Defender),
    ]
    @pytest.mark.parametrize("attributes, expected_cls", creation_data)
    def test_creation(self, attributes, expected_cls):
        player = create_FIFA_player(attributes)
        assert type(player) == expected_cls


# class TestPlayer:
#     def test_creation(self):
#         player = Player('John', 18, 'ST')
#         assert player.name == 'John'
#         assert player.age == 18
#         assert player.position == 'ST'


# class TestFIFAPlayer:
#     def test_init(self):
#         player = FIFAPlayer('John', 18, 'ST', 65, 85, 2022)
#         assert player.position == 'ST'
#         assert player.growth == 20

#         assert PlayerDatabase.players_amount == 1