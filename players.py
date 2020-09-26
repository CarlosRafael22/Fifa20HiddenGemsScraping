from typing import Union, Tuple

class DatabaseType(type):
    def __str__(self):
        return self.__name__


class Player():
    def __init__(self, name, age, position):
        self.name = name
        self.age = age
        self.position = position

    def __str__(self):
        return self.name


class FIFAPlayer(Player):
    def __init__(self, name: str, age: int, position: str, overall: int, potential: int, contract_until: int):
        Player.__init__(self, name, age, position)
        self.overall = overall
        self.potential = potential
        self.contract_until = contract_until
        # self.realPlayer = Player(name, age, position)

        # PlayerDatabase.players_amount += 1
        # PlayerDatabase.add_player(self)

    @classmethod
    def create_with_attribute_dict(cls, attributes):
        age = attributes.get('age', None)
        name = attributes.get('name', None)
        position = attributes.get('position', None)
        overall = attributes.get('overall', None)
        potential = attributes.get('potential', None)
        contract_until = attributes.get('contract_until', None)
        return cls(name, age, position, overall, potential, contract_until)

    @property
    def growth(self):
        return self.potential - self.overall

    def __str__(self):
        return f'{self.overall} overall -> {self.growth} growth'

    def __repr__(self):
        return f'{self.name}'


class FIFADatabasePlayer(FIFAPlayer):
    def __init__(self, name: str, age: int, position: str, overall: int, potential: int, contract_until: int):
        FIFAPlayer.__init__(self, name, age, position, overall, potential, contract_until)
        PlayerDatabase.add_player(self)


class GoalKeeper(FIFADatabasePlayer):
    pass


class Defender(FIFADatabasePlayer):
    pass


class Midfielder(FIFADatabasePlayer):
    pass


class Attacker(FIFADatabasePlayer):
    pass


class PlayerDatabase():
    # __metaclass__ = DatabaseType

    __players_amount = 0
    goalkeepers = []
    defenders = []
    midfielders = []
    attackers = []

    def __init__(self):
        print('Initializing the database')
    
    @property
    def players_amount(self):
        return self.__players_amount

    @classmethod
    def get_players_amount(cls):
        return cls.__players_amount
    
    # @players_amount.setter
    # def players_amount(self, amount):
    #     self.__players_amount = amount

    @classmethod
    def clear_database(cls):
        cls.__players_amount = 0
        cls.goalkeepers = []
        cls.defenders = []
        cls.midfielders = []
        cls.attackers = []

    @classmethod
    def add_player_to_correct_array(cls, player: Union[Attacker, Defender, GoalKeeper, Midfielder], player_type: str) -> None:
        add_function = {
            'GoalKeeper': cls.goalkeepers.append,
            'Defender': cls.defenders.append,
            'Midfielder': cls.midfielders.append,
            'Attacker': cls.attackers.append,
        }[player_type]
        add_function(player)

    @classmethod
    def add_player(cls, player):
        # Adding player to count
        cls.__players_amount += 1
        player_type = type(player).__name__
        print(' TYPE: ', player_type)

        if player_type == 'FIFADatabasePlayer':
            raise Exception('Cant receive FIFADatabasePlayer class only its inheritance')
        if player_type == 'FIFAPlayer':
            raise Exception('Cant receive FIFAPlayer class only its inheritance')

        cls.add_player_to_correct_array(player, player_type)

    def __str__(self):
        # positions_list = ['goalkeepers', 'defenders', 'midfielders', 'attackers']
        # create_array = lambda(position -> ', '.join([player.name for player in PlayerDatabase[position]])
        goalkeepers = ', '.join([goalkeeper.name for goalkeeper in PlayerDatabase.goalkeepers])
        defenders = ', '.join([defender.name for defender in PlayerDatabase.defenders])
        midfielders = ', '.join([midfielder.name for midfielder in PlayerDatabase.midfielders])
        attackers = ', '.join([attacker.name for attacker in PlayerDatabase.attackers])
        return f'Goalkeepers: {goalkeepers} / Defenders: {defenders} / Midfielders: {midfielders} / Attackers: {attackers}'

    @staticmethod
    def get_attribute_and_lookup_from_query_string(key_query_string: str) -> str:
        try:
            attribute, lookup = key_query_string.split('__')
        except ValueError:
            # print(excp)
            attribute = key_query_string.split('__')[0]
            lookup = None
        return (attribute, lookup)
    
    @staticmethod
    def filter_gte(attribute, value, list_to_filter):
            return list(filter(lambda x: getattr(x, attribute) >= value, list_to_filter))

    @staticmethod
    def filter_equals(attribute, value, list_to_filter):
        return list(filter(lambda x: getattr(x, attribute) == value, list_to_filter))
    
    @staticmethod
    def filter_lt(attribute, value, list_to_filter):
        return list(filter(lambda x: getattr(x, attribute) < value, list_to_filter))
    
    @staticmethod
    def filter_contains(attribute, value, list_to_filter):
        return list(filter(lambda x: value in getattr(x, attribute), list_to_filter))

    @classmethod
    def filter_players(cls, players, **kwargs):
        filtered_players = players
        for key, value in kwargs.items():
            # If we dont have the lookup on splitting then we handle it to not throw error
            (attribute, lookup) = PlayerDatabase.get_attribute_and_lookup_from_query_string(key)
            filter_function = {
                'gte': PlayerDatabase.filter_gte,
                'lt': PlayerDatabase.filter_lt,
                'contains': PlayerDatabase.filter_contains,
                None: PlayerDatabase.filter_equals
            }[lookup]
            filtered_players = filter_function(attribute, value, filtered_players)
        return filtered_players


def create_FIFA_player(player_attributes):
    position = player_attributes.get('position', None)
    if position in ['GK']:
        player = GoalKeeper.create_with_attribute_dict(player_attributes)
    elif position in ['LB', 'RB', 'CB']:
        player = Defender.create_with_attribute_dict(player_attributes)
    elif position in ['LM', 'RM', 'CM', 'CAM', 'CDM', 'LW', 'RW']:
        player = Midfielder.create_with_attribute_dict(player_attributes)
    elif position in ['ST', 'CF']:
        player = Attacker.create_with_attribute_dict(player_attributes)
    else:
        print('----------------- ', position)
        player = None
    return player
