from simple_reasoner import SimpleReasoner
from plan_dic import plan_dic
import copy

#
# TODO : Should Executor have plan dictionary? rather, some module's ownership is more appropriate?
# and just type module.plan_dic not self.__plan_dic
#
class Executor(object):

    def __init__(self, reasoner=SimpleReasoner()):
        self.__reasoner = reasoner
        self.goal_list = []
        self.plan_execute = self.__die_easy
        self.__utility = 0

    @property
    def utility(self):
        return self.__utility

    @utility.setter
    def utility(self, value):
        self.__utility = value

    def set_die_hard(self):
        self.plan_execute = self.__die_hard

    def __run(self):
        while len(self.goal_list) > 0:
            callable_plan = self.__plan_select()
            # TODO : processing tree-structure-plan code should be added
            next_goal = self.plan_execute(callable_plan)
            if next_goal is not None:
                self.goal_list.append(next_goal)

    def set_plan_select_plan(self, goal_name:str, **kwargs):
        if goal_name in plan_dic.keys():
            plan = plan_dic[goal_name]
            if isinstance(plan,_Plan):
                self.__plan_select = plan.bind(**kwargs)
            else:
                raise TypeError("plan of {} is not instance of Plan".format(plan.goal_name))
        else:
            raise KeyError("plan for {} is not exist".format(goal_name))

    def __plan_select(self):
        raise Exception("before running, set_plan_select_plan should be called")

    def plan_execute(self, callable_plan):
        pass

    #
    # for debugging
    #
    def __die_easy(self, callable_plan):
        next_goal = callable_plan()
        self.goal_list.remove(callable_plan.goal_name)
        return next_goal

    #
    # originally, agent sould always be in alive state
    #
    def __die_hard(self, plan):
        try:
            next_goal = plan()
            self.goal_list.remove(plan.goal_name)
        except Exception as e:
            print(e)
            next_goal = None
        return next_goal

    def post(self, goal_name):
        self.goal_list.append(goal_name)

    def start(self):
        self.__reasoner.start()
        self.__run()

    #
    # push out all of pre-defined goal:plan mapping, and insert a plan
    #
    @staticmethod
    def ONLY_ONE_PLAN_FOR_GOAL(plan_func=None,
                               goal_name:str = None,
                               argument_meta_info:dict={}):
        if plan_func is not None:
            plan = _Plan(plan_func, goal_name, 1, argument_meta_info,0)
            plan_dic[goal_name] = plan
        else:
            def plan_body_deco(plan_body):
                plan = _Plan(plan_body, goal_name, 1,argument_meta_info,0)
                plan_dic[goal_name] = plan
                return plan

            return plan_body_deco

    @staticmethod
    def PLAN(plan_func=None,
             goal_name: str = None,
             heuristic_marginal_utility: float or str or _Plan= -1.,
             argument_meta_info:dict={},
             utility_operand: float or str=-1):
        if plan_func is not None:
            plan = _Plan(plan_func, goal_name, heuristic_marginal_utility, argument_meta_info, utility_operand)
            if goal_name in plan_dic:
                plan_dic[goal_name].append(plan)
            else:
                plan_dic[goal_name] = [plan]
            return plan
        else:
            def plan_body_deco(plan_body):
                plan = _Plan(plan_body, goal_name, heuristic_marginal_utility, argument_meta_info, utility_operand)
                if goal_name in plan_dic:
                    plan_dic[goal_name].append(plan)
                else:
                    plan_dic[goal_name] = [plan]
                return plan

            return plan_body_deco


class _Plan(object):
    def __init__(self, plan_func,
                 goal_name: str,
                 heuristic_marginal_utility: float or str or _Plan,
                 argument_meta_info: dict,
                 utility_operand: float or str):
        self.__plan_func = plan_func
        self.__goal_name = goal_name
        self.__h_mu = heuristic_marginal_utility
        self.__arg_info = argument_meta_info
        self.__mu = utility_operand
        self.kwargs = {}

    def bind(self, **kwargs):
        for key,value in self.__arg_info.items():
            if key in kwargs:
                if not issubclass(type(kwargs[key]),value):
                    raise TypeError(key+" of binding is not subclass of "+value.__name__)
                    return
        plan_copy = copy.deepcopy(self)
        plan_copy.kwargs.update(kwargs)
        return plan_copy

    def __call__(self, **kwargs):
        print("calling1")
        for key,value in self.__arg_info.items():
            if key in kwargs:
                if not issubclass(type(kwargs[key]),value):
                    raise TypeError(key+" of binding is not subclass of "+value.__name__)
                    return
        temp_dic = kwargs
        print(self.kwargs)
        print("calling2")
        temp_dic.update(self.kwargs)
        res = self.__plan_func(**temp_dic)
        return res

    @property
    def argument_meta_info(self):
        return self.__arg_info

    @property
    def goal_name(self):
        return self.__goal_name

    @property
    def heuristic_marginal_utility(self):
        if callable(self.__h_mu):
            return self.__h_mu()
        else:
            return self.__h_mu

    @property
    def marginal_utility(self):
        if callable(self.__mu):
            return self.__mu()
        else:
            return self.__mu