from plantools import powerplandef, Plan,sub_goal_generate

#
# utility function iter : utility value might be dynamically changed, yet sorting is not considered
#
@powerplandef(goal_name="simple_select",argument_meta_info={"goal_list":list,"plan_dic":dict})
def simple_plan_select(goal_list, plan_dic, **kwargs):
    utility_value = -1
    selected_plan = None
    for goal_name in goal_list:
        temp_plan, temp_value = __get_highest_heuristic_margin_plan(goal_name, plan_dic)
        if utility_value < temp_value:
            utility_value = temp_value
            selected_plan = temp_plan
    return simple_plan_bind(selected_plan, **kwargs)

from inspect import isgeneratorfunction
@powerplandef(goal_name="A_star",argument_meta_info={"goal_name":str,"plan_dic":dict})
def A_star_plan_select(goal_name:str,plan_dic:dict,**kwargs):
    if isgeneratorfunction(a_star_sub_routine):
        gen = a_star_sub_routine(plan_dic)
        gen.send(None)
    while True:
        selected_plan = gen.send(goal_name, utility)
        yield simple_plan_bind(selected_plan, **kwargs)

def a_star_sub_routine(plan_dic):
    dict = {}
    prev_marginal_utility = 0
    selected_plan = None
    while True:
        new_goal_name, get_marginal_utility = yield selected_plan
        plan_list = plan_dic[new_goal_name]
        for plan in plan_list:
            dict[plan] = get_marginal_utility + prev_marginal_utility
        highest_utility = -1
        selected_plan = None
        for plan, prev_util in dict.items():
            temp_utility = plan.heuristic_marginal_utility + prev_util
            if temp_utility>highest_utility:
                highest_utility = temp_utility
                selected_plan = plan
        prev_marginal_utility = dict[selected_plan]
        dict.pop(selected_plan)

def simple_plan_bind(plan:Plan, **kwargs):
    for key in kwargs.copy():
        if key not in plan.argument_meta_info:
            kwargs.pop(key)
    return plan.bind(**kwargs)

def __get_highest_heuristic_margin_plan(goal_name, plan_dic):
    plan_list = plan_dic[goal_name]
    utility_value = -1
    for plan in plan_list:
        temp_value = plan.heuristic_marginal_utility
        if temp_value > utility_value:
            utility_value = temp_value
            highest_utility_plan = plan
    return highest_utility_plan, utility_value