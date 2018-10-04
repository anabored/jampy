from executor import Executor
from plan_dic import plan_dic
from agent.simple_boss_agent import SimpleBossAgent
import numpy as np

class SimpleAgent(Executor):

    def __init__(self, boss_planner = None, world = None):
        agent = self
        Executor.__init__(self)
        self.__boss_planner = boss_planner
        self.post("HelloWorld")
        self.__benefit = 0
        self.__cost = 0
        # args = {"goal_list": self.goal_list,
        #  "plan_dic": plan_dic}
        # args.update(locals())
        args = locals()
        args.pop('self')
        self.set_plan_select_plan("simple_select", goal_list = self.goal_list,plan_dic = plan_dic,**args)
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
    from plan import simple_plan
    from plan import plan_for_planning
    from world.simple_world import SimpleWorld
    import _thread
    from agent.simple_agent import SimpleAgent

    b = SimpleBossAgent()
    _thread.start_new_thread(b.start,())
    a = SimpleAgent(b,SimpleWorld() )
    try :
        a.start()
    except KeyboardInterrupt as e:
        print(e)
    finally:
        pass
        # _thread.exit_thread()