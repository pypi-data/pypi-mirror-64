import math
import xvg.data
import xvg.math
import xvg.models
from .context import Context


class Interpreter():

    def __init__(self):
        self.arguments = {}

    def interpret(self, context, script):
        """ Evaluates a script string with a context """
        exec(script,
             self.createGlobalsMap(context),
             self.createLocalsMap(context))

    def interpretFile(self, context, path):
        """ Evaluates a script file with a context """
        with open(path) as file:
            self.run(file.read())

    def createGlobalsMap(self, context):
        return {
            "__builtins__": {"locals": locals, "globals": globals}
        }

    def createLocalsMap(self, context):
        localsMap = {}

        localsMap['math'] = math
        localsMap['debug'] = print

        localsMap.update(xvg.data.getModuleClasses(xvg.data))
        localsMap.update(xvg.data.getPublicModuleFunctions(xvg.data))

        localsMap.update(xvg.data.getModuleClasses(xvg.math))
        localsMap.update(xvg.data.getPublicModuleFunctions(xvg.math))

        localsMap.update(xvg.data.getModuleClasses(xvg.models))
        localsMap.update(xvg.data.getPublicModuleFunctions(xvg.models))

        localsMap.update(context.getPublicFields())
        localsMap.update(context.getPublicMethods())

        return localsMap
