"""
This file contains analysis and exploration of the different agents
performances.
"""
import pandas as pd
import statistics
import sys
from project.agents.RandomPlayers import RandomPrioritizeAgent
from project.agents.MinimaxAgent import MinmaxAgent
from project.agents.AlphaBetaAgent import AlphaBetaAgent
from project.agents.Heuristics import *
from project.game.AgentVsAgent import agent_vs_agent, get_agent_from_argv, ARGV_EXCEPTION


def get_single_statistics(first_agent, second_agent, num_of_games, max_turn=300):
    """
    This function run a single game between two
    given agents and collects statistical data such as
    turns number, number of marbles that were pushed out for the first and the second player, and win percentage.
    """
    turns_stat = []
    damage1_stat = []
    damage2_stat = []
    winner_stat = []
    for i in range(num_of_games):
        game = agent_vs_agent(first_agent, second_agent, max_turn=max_turn)
        turns_stat.append(game.turns_count)
        first_damages = game.players_damages[0]
        second_damages = game.players_damages[1]
        damage1_stat.append(first_damages)
        damage2_stat.append(second_damages)
        winner_stat.append(int(first_damages - second_damages > 0))
    winPercent = (sum(winner_stat) / len(winner_stat)) * 100
    return statistics.mean(turns_stat), statistics.mean(damage1_stat), statistics.mean(damage2_stat), winPercent


def first_research():
    """
    This function runs the first research - this basic research compares
    a few agents against the RandomPrioritizeAgent which is a basic reasonable player.
    This research provides basic indication on agents and parameters.
    """
    agent1 = RandomPrioritizeAgent()
    agent2 = MinmaxAgent(evaluation_function=evaluate_balanced, depth=1)
    agent21 = MinmaxAgent(evaluation_function=evaluate_balanced, depth=2)
    agent3 = AlphaBetaAgent(evaluation_function=evaluate_balanced, depth=1)
    agent31 = AlphaBetaAgent(evaluation_function=evaluate_balanced, depth=2)
    turns_stat, damage1_stat, damage2_stat, winner_stat = [], [], [], []
    for agent in [agent2, agent21, agent3, agent31]:
        results = get_single_statistics(agent1, agent, 100)
        turns_stat.append(results[0])
        damage1_stat.append(results[1])
        damage2_stat.append(results[2])
        winner_stat.append(results[3])
    df = pd.DataFrame({'turns': turns_stat,
                       'first damage': damage1_stat,
                       'second damage': damage2_stat,
                       'winner': winner_stat})
    df.to_csv('basic_performance_of_agents.csv')


def heuristic_research(is_aggressive):
    """
    Heuristics exploration for the alpha beta agent.
    :param is_aggressive:
    :return:
    """
    turns_stat, damage1_stat, damage2_stat, winner_stat = [], [], [], []
    agent1 = RandomPrioritizeAgent()
    eval_func = evaluate_attack_wrapper if is_aggressive else evaluate_defense_wrapper
    heuristic_parameters = [0, 5, 10, 50, 100, 200, 500, 1000]
    for p in heuristic_parameters:
        agent2 = AlphaBetaAgent(evaluation_function=eval_func(p), depth=2)
        results = get_single_statistics(agent1, agent2, 100)
        turns_stat.append(results[0])
        damage1_stat.append(results[1])
        damage2_stat.append(results[2])
        winner_stat.append(results[3])
    df = pd.DataFrame({'heuristic parameter': heuristic_parameters,
                       'turns': turns_stat,
                       'first damage': damage1_stat,
                       'second damage': damage2_stat,
                       'winner': winner_stat})
    output_file_name = "aggressive_parameter_results.csv" if is_aggressive else "defensive_parameter_results.csv"
    df.to_csv(output_file_name)


def league():
    """
    This function runs a league between different kinds of agents
    each agent has a unique depth or a unique heuristic parameter and was meant to check
    which agent performs the best.
    """
    score = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    agent1_balanced = AlphaBetaAgent(evaluation_function=evaluate_balanced, depth=1)
    agent2_balanced = AlphaBetaAgent(evaluation_function=evaluate_balanced, depth=2)
    agent1_attack = AlphaBetaAgent(evaluation_function=evaluate_attack_wrapper(10), depth=1)
    agent2_attack = AlphaBetaAgent(evaluation_function=evaluate_attack_wrapper(10), depth=2)
    agent1_very_attack = AlphaBetaAgent(evaluation_function=evaluate_attack_wrapper(100), depth=1)
    agent2_very_attack = AlphaBetaAgent(evaluation_function=evaluate_attack_wrapper(100), depth=2)
    agent1_defence = AlphaBetaAgent(evaluation_function=evaluate_defense_wrapper(10), depth=1)
    agent2_defence = AlphaBetaAgent(evaluation_function=evaluate_defense_wrapper(10), depth=2)
    agent1_very_defence = AlphaBetaAgent(evaluation_function=evaluate_defense_wrapper(100), depth=1)
    agent2_very_defence = AlphaBetaAgent(evaluation_function=evaluate_defense_wrapper(100), depth=2)
    agents = [agent1_balanced, agent2_balanced, agent1_attack, agent2_attack, agent1_very_attack, agent2_very_attack,
              agent1_defence, agent2_defence, agent1_very_defence, agent2_very_defence]
    for i in range(len(agents)):
        for j in range(i + 1, len(agents)):
            game = agent_vs_agent(agents[i], agents[j])
            if game.players_victories[0] > 0:
                score[i] += 3
            elif game.players_victories[1] > 0:
                score[j] += 3
            else:
                score[i] += 1
                score[j] += 1
    for i in range(len(agents)):
        for j in range(i + 1, len(agents)):
            game = agent_vs_agent(agents[j], agents[i])
            if game.players_victories[0] > 0:
                score[j] += 3
            elif game.players_victories[1] > 0:
                score[i] += 3
            else:
                score[i] += 1
                score[j] += 1
    return score


if __name__ == '__main__':
    if len(sys.argv) > 1:
        argv, first_agent = get_agent_from_argv(sys.argv)
        argv, second_agent = get_agent_from_argv(argv)

        if len(argv) > 1:
            number_of_games = int(argv[1])
            turn_avg, loss_marbale, enemy_marbels, win_rate_2 = get_single_statistics(first_agent, second_agent,
                                                                                      num_of_games=number_of_games)
            print(f"Statistics of {number_of_games}:\nTurns Avg: {turn_avg}\nPlayer 1 lost marbales: {loss_marbale}"
                  f"\nPlayer 2 lost marbales: {enemy_marbels}\nPlayer 2 Win rate: {win_rate_2}")
        else:
            raise Exception(ARGV_EXCEPTION)
    else:
        raise Exception(ARGV_EXCEPTION)
