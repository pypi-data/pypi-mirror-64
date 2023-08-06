class ExecInterpreter():

    def __init__(self):
        pass

    def interpret(self, context, script):
        """ Evaluates a script string with a context """
        exec(script,
             context.createGlobalsMap(context),
             context.createLocalsMap(context))

    def interpretFile(self, context, path):
        """ Evaluates a script file with a context """
        with open(path) as file:
            self.run(file.read())
