

from agents import AbstractAgent

class DQN(AbstractAgent):
    """
    """
    def __init__(self, settings):
        """
        """
        self.settings = settings

    def build_q_net(self):
        """
        """
        pass

    #
    def generate(self, env):
        """ generate experience
        """
        pass

    #
    def get_batch(self, buffer):
        """ sample a batch from buffer
        """
        pass

    def optimize(self, batch):
        """ optimization step
        """
        pass



    
