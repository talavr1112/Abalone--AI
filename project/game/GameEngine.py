"""
The Game Engine, supplies options to run the ABALONE game with
different configurations (with/without gui, number of turns to tie etc.)
"""

import time
from gym_abalone.game.engine.gamelogic import AbaloneGame
from gym_abalone.game.graphics.abalonegui import AbaloneGui
from pyglet import app, clock

DT = 0.00005


def random_game(dt, gui, agent0, agent1):
    """
    Play a single turn between Agent0 and Agent1 with gui
    """
    t0 = time.time()
    pos0, pos1 = getActionFromPlayer(gui.game, agent0, agent1)

    # highlight the starting pos
    gui.action(pos0)

    # make a move
    def delayed_action(dt):
        gui.action(pos1)
        if gui.game.game_over:
            print(f"Game Over!\nTurns number: {gui.game.turns_count}\nResults: {gui.game.players_victories}")
            app.exit()

    remaining = 0.5 * DT - (time.time() - t0)
    clock.schedule_once(delayed_action, max(0, remaining))
    clock.schedule_once(random_game, dt, gui, agent0, agent1)


def getActionFromPlayer(game, agent0, agent1):
    if game.current_player:
        return agent1.get_action(game)
    else:
        return agent0.get_action(game)


def gameWithoutGui(game, agent0, agent1, max_turn):
    """
    Play a single game between Agent0 and Agent1 without gui
    """
    turn_num = 0

    print("START GAME")

    while not game.game_over and turn_num < max_turn:
        pos0, pos1 = getActionFromPlayer(game, agent0, agent1)
        game.action_handler(pos0, pos1)
        turn_num += 1

    print("GAME OVER")
    print(f"first agent score: {game.players_victories[0]}, "
          f"second agent score: {game.players_victories[1]}")


def startGame(agent0, agent1, max_turn, numberOfGames=1, showGui=False):
    """
    Play numberOfGames games between Agent0 and Agent1, with/without gui
    """
    game = AbaloneGame()

    for i in range(numberOfGames):
        if not showGui:
            game.reset(random_player=False)
            gameWithoutGui(game, agent0, agent1, max_turn)
        else:
            if i == 0:
                abalone_gui = AbaloneGui(game, debug=True)
            abalone_gui.reset_game_gui(random_player=False)

            clock.schedule_once(random_game, DT, abalone_gui, agent0, agent1)
            app.run()
    return game
