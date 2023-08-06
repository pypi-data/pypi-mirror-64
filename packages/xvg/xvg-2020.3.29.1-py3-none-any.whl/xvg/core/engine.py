from .renderer import Renderer
from .context import Context
from .interpreter import Interpreter


class Engine():

    def __init__(self, renderer=None, context=None, interpreter=None):
        self.renderer = renderer or Renderer()
        self.context = context or Context()
        self.interpreter = interpreter or Interpreter()

    def process(self, script):
        self.interpreter.interpret(self.context, script)
        return self.renderer.render(self.context)
