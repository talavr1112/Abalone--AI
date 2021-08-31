import abc


class AbstractAgent(object):
    """
    The Abstract class of an agent.
    """
    def __init__(self):
        super(AbstractAgent, self).__init__()

    @abc.abstractmethod
    def get_action(self, game_state):
        pass


class MultiAgentSearchAgent(AbstractAgent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinmaxAgent, AlphaBetaAgent.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.
    """

    def __init__(self, evaluation_function, depth=1):
        super().__init__()
        self.evaluation_function = evaluation_function
        self.depth = depth

    @abc.abstractmethod
    def get_action(self, game_state):
        return
