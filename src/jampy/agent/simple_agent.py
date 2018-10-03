from core.executor import Executor
import time
import numpy as np

class SimpleAgent(Executor):

    def __init__(self):
        Executor.__init__(self)
        self.post("HelloWorld")

        self.__benefit = 0
        self.__cost = 0

        # TODO : subject, location, direction, information, emotion...
        self.__state_vector = np.zeros(5)

    def primitive_action(self):
        pass


    def simple_utility_func(self):
        return self.__benefit - self.__cost

    def initialize_utility(self):
        self.__benefit = 0
        self.__cost = 0



if __name__ == '__main__':
    SimpleAgent().start()