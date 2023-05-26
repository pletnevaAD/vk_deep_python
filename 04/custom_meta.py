class CustomMeta(type):

    def __new__(mcs, name, bases, classdict, **kwargs):

        def __setattr__(self, attr_name, value):
            if not (attr_name.startswith("__") and attr_name[-2:] == "__"):
                self.__dict__[f"custom_{attr_name}"] = value

        new_classdict = {'__setattr__': __setattr__}
        for key, value in classdict.items():
            if key.startswith("__") and key[-2:] == "__":
                new_classdict[key] = value
            else:
                new_classdict[f"custom_{key}"] = value
        cls = super().__new__(mcs, name, bases, new_classdict)
        return cls


class CustomClass(metaclass=CustomMeta):
    x = 50

    def __init__(self, val=99):
        self.val = val

    def line(self):
        return 100

    def __str__(self):
        return "Custom_by_metaclass"
