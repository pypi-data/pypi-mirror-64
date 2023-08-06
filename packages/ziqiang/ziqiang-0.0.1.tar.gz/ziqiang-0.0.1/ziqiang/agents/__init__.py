

from abc import ABCMeta, abstractmethod

class AbstractAgent(metaclass=ABCMeta):
    """
    """
    def __init__(self, settings):
        """
        """
        pass

    @abstractmethod
    def generate(self, env):
        """ generate experience
        """
        pass

    @abstractmethod
    def get_batch(self, buffer):
        """ sample a batch from buffer
        """
        pass

    @abstractmethod
    def optimize(self, batch):
        """ optimization step
        """
        pass

    
