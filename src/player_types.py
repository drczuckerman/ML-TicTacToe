from operator import itemgetter
from td_learning_player import TDLearningPlayer
from td_symmetric_learning_player import TDSymmetricLearningPlayer
from random_player import RandomPlayer
from human_player import HumanPlayer

LEARNERS = \
{
    "TD": {"class": TDLearningPlayer, "description": "Temporal Difference Learning Player"},
    "TDS": {"class": TDSymmetricLearningPlayer,
            "description": "Temporal Difference Symmetric Learning Player"}
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
    return _sort_by_player_type_and_get_description(_get_player_types_and_descriptions(LEARNERS))

def get_player_descriptions():
    return _sort_by_player_type_and_get_description(
        _get_player_types_and_descriptions(LEARNERS) + _get_player_types_and_descriptions(NON_LEARNERS))

def _get_player_types_and_descriptions(player_type_dict):
    return [(player_type, value["description"]) for player_type, value in player_type_dict.items()]

def _sort_by_player_type_and_get_description(player_types_and_descriptions):
    return list(map(itemgetter(1), sorted(player_types_and_descriptions, key=itemgetter(0))))

def get_learning_player_command_line_args():
    return "\n".join(
        "- {}: {}".format(type, description)
        for type, description in zip(get_learning_player_types(), get_learning_player_descriptions()))
