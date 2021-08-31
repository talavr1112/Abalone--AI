from project.agents.QlearningAgent import QLearningAgent
from project.agents.RandomPlayers import RandomPrioritizeAgent, RandomAgent
from project.agents.Heuristics import evaluate_balanced
from gym_abalone.game.engine.gamelogic import AbaloneGame
from project.statistics.GameStatistics import get_single_statistics


def runEpisode(agent, game, episode, agent1):
    agent.startEpisode()
    print("BEGINNING EPISODE: " + str(episode))
    while True:

        # END IF IN A TERMINAL STATE

        if game.game_over:
            agent.stopEpisode()
            print(f"Game Over!\nTurns number: {game.turns_count}")
            return game

        # GET ACTION (USUALLY FROM AGENT)
        # action = decision(state)
        action = agent.get_action(game)
        currentPlayer = game.current_player
        if action == None:
            raise Exception('Error: Agent returned None action')

        # EXECUTE ACTION
        pos0, pos1 = action
        nextState = game.action_handler_2(pos0, pos1)

        reward = evaluate_balanced(nextState, currentPlayer) - evaluate_balanced(game, currentPlayer)

        # UPDATE LEARNER
        agent.observeTransition(game, action, nextState, reward)

        game = nextState

        # EXECUTE SECOND AGENT ACTION
        pos0, pos1 = agent1.get_action(game)
        game.action_handler(pos0, pos1)


def train_q_learning_agent(agent_to_train, opponent_agent, episodes):
    """training process of q learning Agent and saving it to file"""
    game = AbaloneGame()
    for i in range(1, episodes + 1):
        game.reset(random_player=False)
        game = runEpisode(agent_to_train, game, i, opponent_agent)
        print(f"Results: {game.players_victories}\n")

    agent_to_train.save_trained_counter()


def create_q_learning_agent(numTraining=100):
    """Example of training process of q learning Agent and saving it to file"""
    q_args = {'gamma': 0.9,
              'alpha': 0.5,
              'epsilon': 0.2,
              'actionFn': lambda game: game.get_possible_moves(game.current_player, group_by_type=False)}
    return QLearningAgent(**q_args, numTraining=numTraining)


def explore_q_learning():
    episodes_lst = [100, 500, 1000, 1500, 10000]
    statistics = []
    opponent_agent = RandomAgent()
    train_opponent = RandomPrioritizeAgent()
    for number_episodes in episodes_lst:
        print(f"Train {number_episodes}")
        q_learning_agent = create_q_learning_agent(number_episodes)
        train_q_learning_agent(q_learning_agent, train_opponent, number_episodes)
        results = get_single_statistics(q_learning_agent, opponent_agent, 20, max_turn=400)
        win_percent = 100 - results[3]
        statistics.append(win_percent)
    return statistics


# if __name__ == '__main__':
#     ## Train Qlearning Agent for 10000 iterations
#     number_episodes = 10000
#
#     q_learning_agent = create_q_learning_agent(number_episodes)
#     opponent_agent = RandomPrioritizeAgent()
#     train_q_learning_agent(q_learning_agent, opponent_agent, number_episodes)
#
#     ## Get statistics of Q learning process
#     explore_q_learning()
