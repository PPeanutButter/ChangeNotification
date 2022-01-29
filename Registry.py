module_dict = {}


def register_module(cls):
    module_name = cls.__name__
    module_dict[module_name] = cls
    return cls


def get(module_name):
    return module_dict[module_name]
