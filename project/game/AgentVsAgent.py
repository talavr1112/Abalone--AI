"""
The agent VS agent version of the ABALONE game, run a single game between
first_agent and second_agent
"""
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
from project.game.GameEngine import *
import sys
from project.agents.RandomPlayers import RandomAgent, RandomPrioritizeAgent
from project.agents.MinimaxAgent import MinmaxAgent
from project.agents.AlphaBetaAgent import AlphaBetaAgent
from project.agents.Heuristics import evaluate_attack_wrapper, \
    evaluate_defense_wrapper, evaluate_balanced
from project.agents.QlearningAgent import QLearningAgent


def agent_vs_agent(first_agent, second_agent, max_turn=300, showGui=False):
    game = startGame(first_agent, second_agent, max_turn=max_turn,
                     numberOfGames=1, showGui=showGui)
    return game


ATTACK_PARAM = 10
DEFENSE_PARAM = 10
Q_LEARNING_FILE_PATH = "project/statistics/q_learning_data"

HEURISTIC_EXCEPTION = "Heuristic does not exist"
DEPTH_EXCEPTION = "Depth mast be Int"
AGENT_EXCEPTION_MESSAGE = "Agent does not exist"
ARGV_EXCEPTION = "Incorrect input"


def get_agent_from_argv(argv):
    if argv[1] == "Random":
        agent = RandomAgent()
    elif argv[1] == "RandomPrioritize":
        agent = RandomPrioritizeAgent()
    elif argv[1] == "Minimax" or argv[1] == "AlphaBeta":
        # Choose heuristic
        if argv[2] == "attack":
            heuristic = evaluate_attack_wrapper(ATTACK_PARAM)
        elif argv[2] == "defense":
            heuristic = evaluate_defense_wrapper(DEFENSE_PARAM)
        elif argv[2] == "balance":
            heuristic = evaluate_balanced
        else:
            raise Exception(HEURISTIC_EXCEPTION)

        # Choose depth
        try:
            depth = int(argv[3])
        except ValueError:
            raise Exception(DEPTH_EXCEPTION)

        if argv[1] == "Minimax":
            agent = MinmaxAgent(heuristic, depth)
        else:
            agent = AlphaBetaAgent(heuristic, depth)

        argv.pop(3)
        argv.pop(2)
    elif argv[1] == "QLearning":
        agent = QLearningAgent.load_trained_q_learning_agent(file_name=Q_LEARNING_FILE_PATH)
    else:
        raise Exception(AGENT_EXCEPTION_MESSAGE)
    argv.pop(1)
    return argv, agent


if __name__ == '__main__':
    if len(sys.argv) > 1:
        argv = sys.argv

        argv, first_agent = get_agent_from_argv(argv)
        argv, second_agent = get_agent_from_argv(argv)

        agent_vs_agent(first_agent, second_agent, showGui=True)
    else:
        raise Exception(ARGV_EXCEPTION)
