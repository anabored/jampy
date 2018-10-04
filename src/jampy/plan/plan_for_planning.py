from plantools import powerplandef, Plan

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

def simple_plan_bind(plan:Plan, **kwargs):
    print("bindingplan1")
    print(kwargs)
    for key in kwargs.copy():
        if key not in plan.argument_meta_info:
            kwargs.pop(key)
    print(kwargs)
    print("bindingplan2")
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