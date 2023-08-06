import types
import inspect


def getModuleClasses(target):
    return dict(filter(
        lambda kvp: inspect.isclass(kvp[1]),
        inspect.getmembers(target)))


def getModuleFunctions(target):
    return dict(filter(
        lambda kvp: inspect.isfunction(kvp[1]) or inspect.isbuiltin(kvp[1]),
        inspect.getmembers(target)))


def getPublicModuleFunctions(target):
    return dict(filter(
        lambda kvp: kvp[0][0] != '_' and (
            inspect.isfunction(kvp[1]) or inspect.isbuiltin(kvp[1])),
        inspect.getmembers(target)))


def getPrivateModuleFunctions(target):
    return dict(filter(
        lambda kvp: kvp[0][0] == '_' and (
            inspect.isfunction(kvp[1]) or inspect.isbuiltin(kvp[1])),
        inspect.getmembers(target)))


def getFieldKeys(target):
    return vars(target).keys()


def getFieldValues(target):
    return vars(target).values()


def getFields(target):
    return vars(target).items()


def getPublicFields(target):
    return dict(filter(
        lambda kvp: kvp[0][0] != '_',
        vars(target).items()))


def getPrivateFields(target):
    return dict(filter(
        lambda kvp: kvp[0][0] == '_',
        vars(target).items()))


def getMethods(target):
    return dict(filter(
        lambda kvp: isinstance(
            kvp[1], types.FunctionType),
        type(target).__dict__.items()))


def getPublicMethods(target):
    return dict(filter(
        lambda kvp: kvp[0][0] != '_' and isinstance(
            kvp[1], types.FunctionType),
        type(target).__dict__.items()))


def getPrivateMethods(target):
    return dict(filter(
        lambda kvp: kvp[0][0] == '_' and isinstance(
            kvp[1], types.FunctionType),
        type(target).__dict__.items()))
