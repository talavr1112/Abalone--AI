from project.agents.AbstractAgent import AbstractAgent
import random


class RandomAgent(AbstractAgent):
    """
    Random Agents
    """

    def get_action(self, game_state):
        player = game_state.current_player
        possible_moves = game_state.get_possible_moves(player,
                                                       group_by_type=False)
        pos0, pos1 = random.choice(possible_moves)
        return pos0, pos1


class RandomPrioritizeAgent(AbstractAgent):
    """
    RandomPrioritized agent, choose randomly from prioritized actions.
    """

    def get_action(self, game_state):
        player = game_state.current_player
        possible_moves = game_state.get_possible_moves(player,
                                                       group_by_type=True)
        for move_type in ['winner', 'ejected', 'inline_push', 'inline_move',
                          'sidestep_move']:
            if possible_moves[move_type]:
                pos0, pos1 = random.choice(possible_moves[move_type])
                break
        return pos0, pos1
