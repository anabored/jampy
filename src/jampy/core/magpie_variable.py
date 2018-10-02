

class MagpieVariable:
    def __init__(self, inner_variable):
        self.__inner_variable = inner_variable

    @property
    def inner_variable(self):
        return self.__inner_variable

    @inner_variable.setter
    def inner_variable(self, value):
        self.__inner_variable = value

