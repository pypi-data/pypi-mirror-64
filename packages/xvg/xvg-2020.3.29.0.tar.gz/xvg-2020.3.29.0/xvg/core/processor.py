from .context import Context


class Processor():

    def __init__(self):
        pass

    def process(self, context, script):
        """ Evaluates a script string with a context """
        exec(script,
             {"__builtins__": {"locals": locals, "globals": globals}},
             {"self": context})

    def processFile(self, context, path):
        """ Evaluates a script file with a context """
        with open(path) as file:
            self.run(file.read())
