from copy import deepcopy


class ConditionAction():
    def __init__(self, condition=None, action=None):
        self.condition = condition
        self.action = action


def whenthen(func):
    pairs_whenthen = []
    condition_action = ConditionAction()

    def wrapper(*args, **kwargs):
        for my_pair in pairs_whenthen:
            if my_pair.condition(*args, **kwargs):
                return my_pair.action(*args, **kwargs)
        return func(*args, **kwargs)

    def when(when_func):
        if condition_action.condition is None:
            condition_action.condition = when_func
        else:
            raise ValueError
        return wrapper

    def then(then_func):
        if condition_action.condition is not None:
            condition_action.action = then_func
            pairs_whenthen.append(deepcopy(condition_action))
            condition_action.condition = None
        else:
            raise ValueError
        return wrapper

    wrapper.when = when
    wrapper.then = then
    return wrapper
