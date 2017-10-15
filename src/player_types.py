from td_learning_player import TDLearningPlayer
from random_player import RandomPlayer
from human_player import HumanPlayer

LEARNERS = \
{
    "TD": {"class": TDLearningPlayer, "description": "Temporary Difference Learning Player"}
}
NON_LEARNERS = \
{
    "Random": {"class": RandomPlayer, "description": "Random Player"},
    "Human": {"class": HumanPlayer, "description": "Human Player"}
}

def get_learning_player(player_type):
    return LEARNERS[player_type]["class"]()

def get_player(player_type):
    try:
        return get_learning_player(player_type)
    except KeyError:
        return NON_LEARNERS[player_type]["class"]()

def get_learning_player_types():
    return sorted(LEARNERS.keys())

def get_player_types():
    return sorted(get_learning_player_types() + list(NON_LEARNERS.keys()))

def get_learning_player_descriptions():
    return sorted(_get_player_descriptions(LEARNERS))

def get_player_descriptions():
    return sorted(_get_player_descriptions(LEARNERS) + _get_player_descriptions(NON_LEARNERS))

def _get_player_descriptions(player_type_dict):
    return [value["description"] for value in player_type_dict.values()]

