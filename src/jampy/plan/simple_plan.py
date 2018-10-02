from core.executor import Executor


class SimplePlans:
    #
    # maybe goal name referenced by string could have little benefit.
    # if post goal occurs from external interface,
    # it could handle that circumstance more easy than
    # when it is implemented with some python-dependent-structure like class
    # 11
    #

    @Executor.plan_deco("HelloWorld", 0.8)
    def __hello_world_plan(self):
        goal_state = 5
        prev_distance = goal_state - self.__state
        if self.__state < 5:
            self.__state_plus_one()
        elif self.__state > 5:
            self.__state_minus_one()
        current_distance = goal_state - self.__state
        dif = current_distance - prev_distance
        # TODO :
        # exactly same with self.post("ByeWorld")
        return "ByeWorld"

    @Executor.plan_deco("ByeWorld", 0.)
    def __bye_world_plan(self):
        goal_state = -1
        prev_distance = goal_state - self.__state
        self.__orthogonal_with_goal_action()
        current_distance = goal_state - self.__state
        dif = current_distance - prev_distance

    def __state_plus_one(self):
        self.__state = self.__state +1
    def __state_minus_one(self):
        self.__state = self.__state -1
    def __orthogonal_with_goal_action(self):
        self.__state = self.__state