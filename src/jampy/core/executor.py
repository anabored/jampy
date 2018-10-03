from core.simple_reasoner import SimpleReasoner
import _thread
from functools import wraps

# TODO : JAMAgent
class Executor(object):
    goal_dic = {}

    def __init__(self, reasoner = SimpleReasoner()):
        self.__reasoner = reasoner
        self.__intentions = []
        self.plan_execute = self.__die_easy
        self.__utility = 0

        # TODO : policy
        self.__get_highest_utility_plan = self.__get_highest_expectation

    # def achieve_sync(self, goal_name):
    #     self.__class__.goal_dic[goal_name]
    #
    # def achieve_async(self, goal_name):
    #     _thread.start_new_thread()
    #
    # def maintain(self, goal_name, callback):
    #     pass

    @property
    def utility(self):
        return self.__utility

    @utility.setter
    def utility(self, value):
        self.__utility = value

    def set_die_hard(self):
        self.plan_execute = self.__die_hard

    def __run(self):
        while len(self.__intentions) > 0:
            current_goal = None
            current_plan = None
            utility_value = -1
            print(self.__intentions)
            for goal_name in self.__intentions:
                temp_plan, temp_value = self.__get_highest_utility_plan(goal_name)
                if utility_value < temp_value:
                    utility_value = temp_value
                    current_goal = goal_name
                    current_plan = temp_plan
            next_goal = self.plan_execute(current_goal, current_plan)
            if next_goal is not None:
                self.__intentions.append(next_goal)

    def plan_execute(self, goal, plan):
        pass

    #
    # for debugging
    #
    def __die_easy(self, goal, plan):
        print(goal)
        next_goal = plan(self)
        print(next_goal)
        print(self.__intentions)
        self.__intentions.remove(goal)
        return next_goal

    #
    # originally, agent sould always be in alive state
    #
    def __die_hard(self, goal, plan):
        try:
            next_goal = plan(self)
            self.__intentions.remove(goal)
        except Exception as e:
            print(e)
            next_goal = None
        return next_goal

    #
    # utility function iter : utility value might be dynamically changed, yet sorting is not considered
    #
    def __get_highest_utility_plan(self, goal_name):
        plan_dic = self.__class__.goal_dic[goal_name]
        utility_value = 0
        for plan, utility_func in plan_dic.items():
            temp_value = utility_func(self)
            if temp_value > utility_value:
                utility_value = temp_value
                highest_utility_plan = plan
        return highest_utility_plan, utility_value

    def __get_highest_expectation(self, goal_name):
        print(goal_name)
        plan_dic = self.__class__.goal_dic[goal_name]
        utility_value = -1
        for plan, experience_array in plan_dic.items():
            # TODO : change to numpy reduce
            sum =0.
            for experience in experience_array:
                print(experience)
                sum +=experience
            temp_value = sum/len(experience_array)
            if temp_value > utility_value:
                utility_value = temp_value
                highest_utility_plan = plan
        return highest_utility_plan, utility_value

    def post(self, goal_name):
        self.__intentions.append(goal_name)

    def start(self):
        self.__reasoner.start()
        self.__run()

    @classmethod
    def plan_deco(cls,goal_name: str, heuristic_margin:float):
        def plan_body_deco(plan):
            if goal_name in cls.goal_dic:
                cls.goal_dic[goal_name][plan] = [heuristic_margin]
            else:
                cls.goal_dic[goal_name] = {plan:[heuristic_margin]}
            @wraps
            def wrapper(self:Executor, *args, **kwargs):
                prev_utility_value = cls.utility
                res =  plan(self, *args,**kwargs)
                marginal_utility = cls.utility - prev_utility_value
                cls.goal_dic[goal_name][plan].append(marginal_utility)
                return res
            return wrapper
        return plan_body_deco

    @classmethod
    def PLAN(cls,plan_func= None, goal_name:str = None, heuristic_margin:float = -1.):
        if plan_func is not None:
            plan = _Plan(plan_func, goal_name, heuristic_margin)
            if goal_name in cls.goal_dic:
                cls.goal_dic[goal_name].append(plan)
            else:
                cls.goal_dic[goal_name] = [plan]
            return plan
        else:
            def plan_body_deco(plan_body):
                plan = _Plan(plan_body, goal_name, heuristic_margin)
                if goal_name in cls.goal_dic:
                    cls.goal_dic[goal_name].append(plan)
                else:
                    cls.goal_dic[goal_name] = [plan]
                return plan
            return plan_body_deco

    @classmethod
    def rule_deco(cls,rule_callback):
        return rule_callback

    @classmethod
    def primitive_deco(cls, primitive_func):
        @wraps
        def wrapper(self: Executor, *args, **kwargs):
            if self.i : return None
            return primitive_func(self, *args,**kwargs)
        return wrapper

class _Plan:
    def __init__(self, plan_func, goal_name:str, heuristic_margin:float):
        self.__plan_func = plan_func
        self.__goal_name = goal_name
        self.__heuristic_margin = heuristic_margin
        self.__experience_margin = []

    def __call__(self, *args, **kwargs):

        res = self.__plan_func(*args,**kwargs)

        return res