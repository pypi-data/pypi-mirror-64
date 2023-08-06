from xvg.data import Object
from xvg.math import Vector


class Context(Object):

    def __init__(self):
        self.size = Vector()
        self.scale = Vector()

    def saveModel(self, id, model):
        pass

    def loadModel(self, id):
        pass

    def drawModel(self, id):
        pass
