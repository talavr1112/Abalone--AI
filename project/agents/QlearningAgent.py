import random, util, math

from project.agents.AbstractAgent import AbstractAgent
from util import Counter
import pickle


class ValueEstimationAgent(AbstractAgent):
    """
      Abstract agent which assigns values to (state,action)
      Q-Values for an environment. As well as a value to a
      state and a policy given respectively by,

      V(s) = max_{a in actions} Q(s,a)
      policy(s) = arg_max_{a in actions} Q(s,a)

      Both ValueIterationAgent and QLearningAgent inherit
      from this agent. While a ValueIterationAgent has
      a model of the environment via a MarkovDecisionProcess
      (see mdp.py) that is used to estimate Q-Values before
      ever actually acting, the QLearningAgent estimates
      Q-Values while acting in the environment.
    """

    def __init__(self, alpha=1.0, epsilon=0.05, gamma=0.8, numTraining=10):
        """
        Sets options, which can be passed in via the Pacman command line using -a alpha=0.5,...
        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        self.alpha = float(alpha)
        self.epsilon = float(epsilon)
        self.discount = float(gamma)
        self.numTraining = int(numTraining)

    ####################################
    #    Override These Functions      #
    ####################################
    def getQValue(self, state, action):
        """
        Should return Q(state,action)
        """
        util.raiseNotDefined()

    def getValue(self, state):
        """
        What is the value of this state under the best action?
        Concretely, this is given by

        V(s) = max_{a in actions} Q(s,a)
        """
        util.raiseNotDefined()

    def getPolicy(self, state):
        """
        What is the best action to take in the state. Note that because
        we might want to explore, this might not coincide with getAction
        Concretely, this is given by

        policy(s) = arg_max_{a in actions} Q(s,a)

        If many actions achieve the maximal Q-value,
        it doesn't matter which is selected.
        """
        util.raiseNotDefined()

    def get_action(self, state):
        """
        state: can call state.getLegalActions()
        Choose an action and return it.
        """
        util.raiseNotDefined()


class ReinforcementAgent(ValueEstimationAgent):
    """
      Abstract Reinforcemnt Agent: A ValueEstimationAgent
        which estimates Q-Values (as well as policies) from experience
        rather than a model

        What you need to know:
            - The environment will call
              observeTransition(state,action,nextState,deltaReward),
              which will call update(state, action, nextState, deltaReward)
              which you should override.
        - Use self.getLegalActions(state) to know which actions
              are available in a state
    """

    def update(self, state, action, nextState, reward):
        """
            This class will call this function, which you write, after
            observing a transition and reward
        """
        util.raiseNotDefined()

    def getLegalActions(self, state):
        """
          Get the actions available for a given
          state. This is what you should use to
          obtain legal actions for a state
        """
        return self.actionFn(state)

    def observeTransition(self, state, action, nextState, deltaReward):
        """
            Called by environment to inform agent that a transition has
            been observed. This will result in a call to self.update
            on the same arguments


        """
        self.episodeRewards += deltaReward
        self.update(state, action, nextState, deltaReward)

    def startEpisode(self):
        """
          Called by environment when new episode is starting
        """
        self.lastState = None
        self.lastAction = None
        self.episodeRewards = 0.0

    def stopEpisode(self):
        """
          Called by environment when episode is done
        """
        if self.episodesSoFar < self.numTraining:
            self.accumTrainRewards += self.episodeRewards
        else:
            self.accumTestRewards += self.episodeRewards
        self.episodesSoFar += 1
        if self.episodesSoFar >= self.numTraining:
            # Take off the training wheels
            self.epsilon = 0.0  # no exploration
            self.alpha = 0.0  # no learning

    def isInTraining(self):
        return self.episodesSoFar < self.numTraining

    def isInTesting(self):
        return not self.isInTraining()

    def __init__(self, actionFn=None, numTraining=100, epsilon=0.5, alpha=0.5, gamma=1):
        """
        actionFn: Function which takes a state and returns the list of legal actions

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        if actionFn == None:
            actionFn = lambda state: state.get_possible_moves(state, group_by_type=False)
        self.actionFn = actionFn
        self.episodesSoFar = 0
        self.accumTrainRewards = 0.0
        self.accumTestRewards = 0.0
        self.numTraining = int(numTraining)
        self.epsilon = float(epsilon)
        self.alpha = float(alpha)
        self.discount = float(gamma)

    ################################
    # Controls needed for Crawler  #
    ################################
    def setEpsilon(self, epsilon):
        self.epsilon = epsilon

    def setLearningRate(self, alpha):
        self.alpha = alpha

    def setDiscount(self, discount):
        self.discount = discount

    def doAction(self, state, action):
        """
            Called by inherited class when
            an action is taken in a state
        """
        self.lastState = state
        self.lastAction = action


class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent
    """

    def __init__(self, **args):

        ReinforcementAgent.__init__(self, **args)
        self.values = util.Counter()

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we never seen
          a state or (state,action) tuple
        """
        return self.values[(str(state.board), action)]

    def getValue(self, state):
        """
        Returns max_action Q(state,action)
        where the max is over legal actions.  Note that if
        there are no legal actions, which is the case at the
        terminal state, return a value of 0.0.
        """
        actions = self.getLegalActions(state)
        if not len(actions):
            return 0.0
        return max([self.getQValue(state, action) for action in actions])

    def getPolicy(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          return None.
        """

        actions = self.getLegalActions(state)
        if not len(actions) or state.game_over:
            return None
        best_actions, best_value = [], None
        for action in actions:
            reward = self.getQValue(state, action)
            if best_value is None or reward > best_value:
                best_actions = [action]
                best_value = reward
            elif reward == best_value:
                best_actions.append(action)
        return random.choice(best_actions)

    def get_action(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, choose None as the action.
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        if state.game_over:
            return None
        coin = util.flipCoin(self.epsilon)
        if coin:
            return random.choice(legalActions)
        return self.getPolicy(state)

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.

        """

        self.values[(str(state.board), action)] += self.alpha * (reward + (self.discount * self.getValue(nextState)) -
                                                                 self.getQValue(state, action))

    def get_trained_counter(self):
        return self.values.get_dict()

    def set_trained_counter(self, dic):
        counter = Counter(dic)
        self.values = counter

    def save_trained_counter(self, file_name="q_learning_data"):
        values = self.get_trained_counter()
        with open(file_name + ".pkl", "wb") as file:
            pickle.dump(values, file)

    @staticmethod
    def load_trained_q_learning_agent(file_name="q_learning_data"):
        """loading trained and running Q Learning Agent from file"""
        counter = None
        with open(file_name + ".pkl", "rb") as saved_counter:
            counter = pickle.load(saved_counter)
        if counter is not None:
            q_args = {'gamma': 1,
                      'alpha': 0,
                      'epsilon': 0,
                      'actionFn': lambda game: game.get_possible_moves(
                          game.current_player, group_by_type=False)}
            agent = QLearningAgent(**q_args)
            agent.set_trained_counter(counter)
            return agent
