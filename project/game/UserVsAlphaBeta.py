"""
The user VS agent version of the ABALONE game, run a game against the
Alpha-Beta Agent.
"""

import pyglet
import time
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
from gym_abalone.game.graphics.abalonegui import AbaloneGui
from gym_abalone.game.engine.gamelogic import AbaloneGame
from project.agents.Heuristics import *
from project.agents.AlphaBetaAgent import AlphaBetaAgent

DT = 0.5


def random_game(dt, gui):
    alpha_beta = AlphaBetaAgent(evaluation_function=evaluate_balanced, depth=2)
    t0 = time.time()
    pos0, pos1 = alpha_beta.get_action(gui.game)
    # highlight the starting pos
    gui.action(pos0)

    # make a move
    def delayed_action(dt):
        move_type = gui.action(pos1)
        if gui.game.game_over:
            print(f"Game Over!\nTurns number: {gui.game.turns_count}\nResults: {gui.game.players_victories}")
            gui.reset_game_gui(random_pick=False)
            pyglet.app.exit()

    remaining = 0.5 * DT - (time.time() - t0)
    pyglet.clock.schedule_once(delayed_action, max(0, remaining))


def run_game():
    game = AbaloneGame()
    abalone_gui = AbaloneGui(game, debug=True)
    # abalone_gui.reset_game_gui(variant_name='anglattack', random_pick=False)
    abalone_gui.reset_game_gui(random_player=False)
    pyglet.clock.schedule_once(random_game, DT, abalone_gui)
    pyglet.app.run()
    print('good bye !')


if __name__ == '__main__':
    run_game()
