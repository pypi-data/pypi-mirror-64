from xvg.core import Object
from xvg.math import Vector

import math
import xvg.core
import xvg.math
import xvg.models


class PureContext(Object):

    def __init__(self):
        self.name = 'untitled'
        self.size = Vector()
        self.scale = Vector()

    def setNode(self, id, model):
        pass

    def getNode(self, id):
        pass

    def useNode(self, id):
        pass

    def createGlobalsMap(self, context):
        return {
            "__builtins__": {"locals": locals, "globals": globals}
        }

    def createLocalsMap(self, context):
        localsMap = {}

        localsMap['math'] = math
        localsMap['debug'] = print

        localsMap.update(xvg.core.getModuleClasses(xvg.core))
        localsMap.update(xvg.core.getPublicModuleFunctions(xvg.core))

        localsMap.update(xvg.core.getModuleClasses(xvg.math))
        localsMap.update(xvg.core.getPublicModuleFunctions(xvg.math))

        localsMap.update(xvg.core.getModuleClasses(xvg.models))
        localsMap.update(xvg.core.getPublicModuleFunctions(xvg.models))

        localsMap.update(self.getPublicFields())
        localsMap.update(self.getPublicMethods())

        return localsMap
