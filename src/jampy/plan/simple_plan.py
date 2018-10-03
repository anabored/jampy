from core.executor import Executor

#
# maybe GOAL NAME referenced by string could have little benefit.
# if post goal occurs from external interface,
# it could handle that circumstance more easy than
# when it is implemented with some python-dependent-structure like class
#

#
# TODO : for corresponding with the convention, should heuristic be cost?
# According to A* algorithm, Usually heuristic margin MUST be bigger than real utility that plan gives.
# If plan's heuristic utility is smaller than real(runtime:it can be dynamically changed) utility,
# optimality can't be accomplished. because A* doesn't search path that
# heuristic cost[heuristic utility] is bigger[lower] than other (not optimal) path's real cost[utility].
# (but, in fact, optimal path's real cost is lower)
#

@Executor.PLAN(goal_name="HelloWorld",heuristic_margin=0.8)
def __hello_world_plan(agent):
    goal_state = 5
    prev_distance = goal_state - agent.__state
    if agent.__state < 5:
        agent.__state_plus_one()
    elif agent.__state > 5:
        agent.__state_minus_one()
    current_distance = goal_state - agent.__state
    dif = current_distance - prev_distance
    # TODO :
    # exactly same with self.post("ByeWorld")
    return "ByeWorld"

@Executor.PLAN(goal_name="MultiAgentPlan", heuristic_margin=0.7)
def __multi_agent_plan(agent1, agent2):
    agent1

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