from project.agents.AbstractAgent import MultiAgentSearchAgent
from project.agents.Heuristics import evaluate_attack, evaluate_defense


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Our minimax agent with alpha-beta pruning
    """

    def __init__(self, evaluation_function, depth):
        super().__init__(evaluation_function, depth)
        self.stateDictMax = dict()
        self.stateDictMin = dict()

    def __repr__(self):
        description = "balanced"
        if self.evaluation_function == evaluate_attack:
            description = "attack"
        elif self.evaluation_function == evaluate_defense:
            description = "defense"
        return " depth:" + str(self.depth) + description

    def get_action(self, game_state):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        max_value = float('-inf')
        selected_step = None
        max_player = game_state.current_player
        for action_lst in game_state.get_possible_moves(max_player).values():
            for action in action_lst:
                pos0, pos1 = action
                x = str(game_state.action_handler_2(pos0, pos1).board)
                if (x, self.depth) in self.stateDictMax:
                    temp_score = self.stateDictMax[(x, self.depth)]
                else:
                    temp_score = self.alpha_beta_helper(game_state.action_handler_2(pos0, pos1),
                                                        (game_state.current_player + 1) % 2,
                                                        self.depth - 1, float('-inf'),
                                                        float('inf'), max_player)
                    self.stateDictMax[(x, self.depth)] = temp_score
                if max_value <= temp_score:
                    max_value = temp_score
                    selected_step = action

        return selected_step

    def alpha_beta_helper(self, game_state, player, current_depth, alpha, beta, max_player):
        if current_depth == 0 or game_state.game_over:
            return self.evaluation_function(game_state, max_player)

        configuration = None
        if player == max_player:  # max_player
            value = float('-inf')
            legal_moves = game_state.get_possible_moves(player)
            for action_lst in legal_moves.values():
                for action in action_lst:
                    pos0, pos1 = action
                    next_b = game_state.action_handler_2(pos0, pos1)
                    if (str(next_b.board), current_depth) in self.stateDictMax:
                        temp_score = self.stateDictMax[(str(next_b.board), current_depth)]
                    else:
                        temp_score = \
                            self.alpha_beta_helper(
                                next_b, (player + 1) % 2,
                                        current_depth - 1, alpha, beta, max_player)
                        self.stateDictMax[(str(next_b.board), current_depth)] = temp_score
                    if value <= temp_score:
                        value = temp_score
                        configuration = temp_score
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break
            return configuration

        else:  # min_player
            value = float('inf')
            legal_moves = game_state.get_possible_moves(player)
            for action_lst in legal_moves.values():
                for action in action_lst:
                    pos0, pos1 = action
                    next_b = game_state.action_handler_2(pos0, pos1)
                    if (str(next_b.board), current_depth) in self.stateDictMin:
                        temp_score = self.stateDictMin[(str(next_b.board), current_depth)]
                    else:
                        temp_score = \
                            self.alpha_beta_helper(
                                next_b, (player + 1) % 2,
                                        current_depth - 1, alpha, beta, max_player)
                        self.stateDictMin[(str(next_b.board), current_depth)] = temp_score
                    if value >= temp_score:
                        value = temp_score
                        configuration = temp_score
                    beta = min(beta, value)
                    if beta <= alpha:
                        break
            return configuration
