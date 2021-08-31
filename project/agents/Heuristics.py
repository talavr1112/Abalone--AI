"""
All kinds of heuristics (defense, attack and balance) for our Minimax/AlphaBeta Agents.
"""
import numpy as np

WIN_NUM = 6
MARBLES_NUM = 14
W1 = 50000
W2 = 1
W3 = 1
W4 = 1
W5 = 10
W6 = 70
W7 = 200
BEST_SCORE = 600000000000


def evaluate_attack_wrapper(p):
    def evaluate_attack(game, player):
        return evaluate_generally(game, player, p, 1)
    return evaluate_attack


def evaluate_defense_wrapper(p):
    def evaluate_defense(game, player):
        return evaluate_generally(game, player, 1, p)
    return evaluate_defense


def evaluate_attack(game, player, p):
    return evaluate_generally(game, player, p, 1)


def evaluate_defense(game, player, p):
    return evaluate_generally(game, player, 1, p)


def evaluate_balanced(game, player):
    return evaluate_generally(game, player, 1, 1)


def evaluate_generally(game, player, attack, defend):
    eval_by_num = MARBLES_NUM - np.sum(game.board == (player + 1) % game.players)
    return W1 * eval_by_num + defend * evaluate_board(game, player) - attack * evaluate_board(game, (
            player + 1) % game.players)


def evaluate_board(game, player):
    """
    The main evaluation function for the ABALONE game board.
    """
    players_marbles = np.argwhere(game.board == player)
    player_dist_from_center, friendly_neighbors, form_score,  margin_score_1,  margin_score_2 = 0, 0, 0, 0, 0
    center = [5, 5]
    corner_score = 0
    first_corner = (5, 1)
    second_corner = (5, 9)
    for marble in players_marbles:
        # calc distance from center
        distances = np.abs(marble - center)
        player_dist_from_center += distances[0] + distances[1]
        enemy_neighbors = 0
        is_margin_marble = False
        # neighbors = 0
        for action in game.ACTIONS:
            pos = marble + action
            # check if in margin
            if not is_margin_marble and game.board[pos[0], pos[1]] == -2:
                is_margin_marble = True
            # check if marble is surrounded by friendly neighbors
            if game.board[pos[0], pos[1]] == player:
                friendly_neighbors += 1
            # check if marble is surrounded by enemy neighbors
            elif game.board[pos[0], pos[1]] == ((player + 1) % game.players):
                enemy_neighbors += 1
        if enemy_neighbors > 4:
            form_score += 1
        if is_margin_marble:
            if enemy_neighbors == 1:
                margin_score_1 += 1
            elif enemy_neighbors == 2:
                margin_score_2 += 1
    if game.board[first_corner] == player:
        corner_score += 1
    if game.board[second_corner] == player:
        corner_score += 1

    if game.game_over and player == (game.current_player + 1) % game.players:
        return BEST_SCORE
    return (-W2 * player_dist_from_center + W3 * friendly_neighbors + W4 * form_score -
            W5 * margin_score_1 - W6 * margin_score_2 - W7 * corner_score) / players_marbles.shape[0]