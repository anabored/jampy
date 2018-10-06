from plantools import plandef
from agent.simple_agent import SimpleAgent
from world.simple_world import SimpleWorld
#
# maybe GOAL NAME referenced by string could have little benefit.
# if post goal occurs from external interface,
# it could handle that circumstance more easy than
# when it is implemented with some python-dependent-structure like class
# ---> python has eval method, what exactly this method can do?
#

#
# TODO : for corresponding with the convention, should heuristic be cost?
# According to A* algorithm, Usually heuristic margin(admissible) MUST be bigger than real utility that plan gives.
# If plan's heuristic utility is smaller than real(runtime:it can be dynamically changed) utility,
# optimality can't be accomplished. because A* doesn't search path that
# heuristic cost[heuristic utility] is bigger[lower] than other (not optimal) path's real cost[utility].
# (but, in fact, optimal path's real cost is lower)
#

#
#
#

# TODO : if @SimpleAgent.PLAN( ... ) replaces below, what happens?
@plandef(goal_name="HelloWorld",
         heuristic_marginal_utility=0.8,
         argument_meta_info={"agent":SimpleAgent, "world":SimpleWorld},
         utility_operand="simple_utility")
def __hello_world_plan(agent:SimpleAgent, world:SimpleWorld):
    #
    # after python 3.5, async def, await keyword is added
    #
    yield "go_front"
    yield "ByeWorld"
    # TODO :
    # exactly same with self.post("ByeWorld")
    return 0.5

@plandef(goal_name="simple_utility",
         heuristic_marginal_utility=0.8,
         argument_meta_info={"agent":SimpleAgent},
         utility_operand=1)
def __simple_utility(agent:SimpleAgent):
    return agent.simple_utility_func()

@plandef(goal_name="go front", heuristic_marginal_utility=1., argument_meta_info={"agent":SimpleAgent})
def __go_front_plan(agent:SimpleAgent):
    agent.primitive_action()

@plandef(goal_name="MultiAgentPlan", heuristic_marginal_utility=0.7)
def __multi_agent_plan(agent1, agent2):
    agent1

@plandef(goal_name="ByeWorld", heuristic_marginal_utility=0.)
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