from project.agents.AbstractAgent import MultiAgentSearchAgent


class MinmaxAgent(MultiAgentSearchAgent):
    """
    Our minimax agent.
    """

    def __init__(self, evaluation_function, depth):
        super().__init__(evaluation_function, depth)

    def get_action(self, game_state):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.
        """
        max_value = float('-inf')
        selected_step = None
        for action_lst in game_state.get_possible_moves(
                game_state.current_player).values():
            for action in action_lst:
                pos0, pos1 = action
                temp_score = self.minimax(
                    game_state.action_handler_2(pos0, pos1),
                    (game_state.current_player + 1) % 2,
                    self.depth - 1, game_state.current_player)
                if temp_score >= max_value:
                    max_value = temp_score
                    selected_step = action

        return selected_step

    def minimax(self, game_state, player, current_depth, max_player):
        if current_depth == 0 or game_state.game_over:
            return self.evaluation_function(game_state, max_player)

        legal_moves = game_state.get_possible_moves(player)
        if player == max_player:  # max_player
            temp_scores = [self.minimax(
                game_state.action_handler_2(action[0], action[1]),
                (player + 1) % 2, current_depth - 1, max_player)
                for action_lst in legal_moves.values() for action in
                action_lst]
            return max(temp_scores)

        else:  # min_player
            temp_scores = [self.minimax(
                game_state.action_handler_2(action[0], action[1]),
                (player + 1) % 2, current_depth - 1, max_player)
                for action_lst in legal_moves.values() for action in
                action_lst]
            return min(temp_scores)
