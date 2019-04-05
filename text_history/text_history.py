from abc import ABC, abstractmethod
from math import inf


def check_version(from_version, to_version):
    if from_version < 0:
        raise ValueError("Initial version is less than zero")
    if to_version < 0:
        raise ValueError("Final version is less than zero")
    if to_version < from_version:
        raise ValueError("Final version is less than initial version")
    return from_version, to_version


class TextHistory:
    def __init__(self, text='', actions=None, version=0):
        self._actions = actions
        self._text = text
        self._version = version

    @property
    def text(self):
        return self._text

    @property
    def version(self):
        return self._version

    @staticmethod
    def get_to_version_if_none(to_version):
        if to_version is None:
            return inf
        else:
            return to_version

    @staticmethod
    def get_from_version_if_none(from_version):
        if from_version is None:
            return 0
        else:
            return from_version

    def get_actions_if_none(self):
        if self._actions is None:
            self._actions = []
            return self._actions
        else:
            return self._actions

    def action(self, act):
        self._actions = self.get_actions_if_none()
        if act.from_version != self._version:
            raise ValueError("Action version differs from current text version.")
        self._text = act.apply(self._text)
        self._actions.append(act)
        self._version = act.to_version
        return act.to_version

    def insert(self, text, pos=None):
        if pos is None:
            pos = len(self._text)
        make_action = InsertAction(text, pos, self._version, self._version + 1)
        return self.action(make_action)

    def delete(self, pos, length):
        self._actions = self.get_actions_if_none()
        make_action = DeleteAction(pos, length, self._version, self._version + 1)
        return self.action(make_action)

    def replace(self, text, pos=None):
        self._actions = self.get_actions_if_none()
        if pos is None:
            pos = len(self._text)
        make_action = ReplaceAction(text, pos, self._version, self._version + 1)
        return self.action(make_action)

    def choose_optimization(self, actions):
        i = 0
        while i < len(actions) - 1:
            first_action = actions[i]
            second_action = actions[i + 1]
            if type(first_action) is type(second_action) is InsertAction:
                if first_action.pos + len(first_action.text) == second_action.pos:
                    actions.pop(i)
                    actions[i] = self.optimized_insert(first_action, second_action)
                else:
                    i += 1
            elif type(first_action) is type(second_action) is DeleteAction:
                if first_action.pos == second_action.pos:
                    actions.pop(i)
                    actions[i] = self.optimized_delete(first_action, second_action)
                else:
                    i += 1
            else:
                i += 1
        return actions

    @staticmethod
    def optimized_insert(first_action, second_action):
        pos = first_action.pos
        my_string = first_action.text + second_action.text
        from_version = first_action.from_version
        to_version = second_action.to_version
        make_action = InsertAction(my_string, pos, from_version, to_version)
        return make_action

    @staticmethod
    def optimized_delete(first_action, second_action):
        pos = first_action.pos
        length = first_action.length + second_action.length
        from_version = first_action.from_version
        to_version = first_action.to_version
        make_action = DeleteAction(pos, length, from_version, to_version)
        return make_action

    def get_actions(self, from_version=None, to_version=None):
        to_version = self.get_to_version_if_none(to_version)
        from_version = self.get_from_version_if_none(from_version)
        from_version, to_version = check_version(from_version, to_version)
        if to_version != inf and to_version > self._actions[-1].to_version:
            raise ValueError("Given version out of range.")
        actions = []
        self._actions = self.get_actions_if_none()
        for action in self._actions:
            if action.from_version >= from_version and action.to_version <= to_version:
                actions.append(action)
        return self.choose_optimization(actions)


class Action(ABC):
    def __init__(self, from_version, to_version, pos):
        from_version, to_version = check_version(from_version, to_version)
        self._from_version = from_version
        self._to_version = to_version
        self._pos = pos
        self.check_pos_negative_or_not()

    @property
    def from_version(self):
        return self._from_version

    @property
    def to_version(self):
        return self._to_version

    @abstractmethod
    def apply(self, apply_to):
        pass

    def check_is_position_in_length(self, apply_to):
        if len(apply_to) < self._pos:
            raise ValueError("Insert position out of string length")

    @property
    def pos(self):
        return self._pos

    def check_pos_negative_or_not(self):
        if self._pos is not None and int(self._pos) < 0:
            raise ValueError("Pos is negative")


class ReplaceAction(Action):
    def __init__(self, text, pos, from_version, to_version):
        self._text = text
        super().__init__(from_version, to_version, pos)

    @property
    def text(self):
        return self._text

    def apply(self, apply_to):
        self.check_is_position_in_length(apply_to)
        return apply_to[:self._pos] + self._text + apply_to[self._pos + len(self._text):]


class InsertAction(Action):
    def __init__(self, text, pos, from_version, to_version):
        self._text = text
        super().__init__(from_version, to_version, pos)

    @property
    def text(self):
        return self._text

    def apply(self, apply_to):
        self.check_is_position_in_length(apply_to)
        return apply_to[:self._pos] + self._text + apply_to[self._pos:]


class DeleteAction(Action):

    @staticmethod
    def check_length_negative_or_not(length):
        if length < 0:
            raise ValueError("length can not be negative")

    def __init__(self, pos, length, from_version, to_version):
        self.check_length_negative_or_not(length)
        self._length = length

        super().__init__(from_version, to_version, pos)

    @property
    def length(self):
        return self._length

    def apply(self, apply_to):
        self.check_is_position_in_length(apply_to)
        if self._pos + self._length > len(apply_to):
            raise ValueError("Trying to delete symbols out of string.")
        return apply_to[:self._pos] + apply_to[self._pos + self._length:]
