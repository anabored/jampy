from core.executor import Executor
import time


class SimpleAgent(Executor):

    def __init__(self):
        Executor.__init__(self)
        self.post("HelloWorld")
        self.__benefit = 0
        self.__cost = 0
        self.__state = 0

    def simple_utility_func(self):
        return self.__benefit - self.__cost

    def initialize_utility(self):
        self.__benefit = 0
        self.__cost = 0

    @Executor.plan_deco("HelloWorld",simple_utility_func, 0.8)
    def __hello_world_plan(self):
        self.initialize_utility()
        goal_state = 5
        prev_distance = goal_state - self.__state
        if self.__state < 5:
            self.__state_plus_one()

        elif self.__state >5:
            self.__state_minus_one()

        current_distance = goal_state - self.__state
        dif = current_distance - prev_distance
        if dif > 0:
            self.__benefit = dif
        else:
            self.__cost = dif
        return "ByeWorld"

    @Executor.plan_deco("ByeWorld", simple_utility_func, 0.)
    def __bye_world_plan(self):
        self.initialize_utility()
        goal_state = -1
        prev_distance = goal_state - self.__state
        self.__orthogonal_with_goal_action()
        current_distance = goal_state - self.__state
        dif = current_distance - prev_distance
        if dif > 0:
            self.__benefit = dif
        else:
            self.__cost = dif

    def __state_plus_one(self):
        self.__state = self.__state +1
    def __state_minus_one(self):
        self.__state = self.__state -1
    def __orthogonal_with_goal_action(self):
        self.__state = self.__state

if __name__ == '__main__':
    SimpleAgent().start()