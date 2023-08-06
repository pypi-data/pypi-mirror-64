from xvg.data import toJSON


class Renderer():

    def render(self, context):
        """ Renders the image and returns the result """
        return toJSON(context)

    def renderFile(self, context, path):
        """ Renders the image and writes the result file """
        with open(path, "w") as file:
            file.write(self.render(context))
