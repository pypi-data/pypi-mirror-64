import os
import darkslide.cli


README_PATH = os.path.join(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))),
    "README.md"
)


class Options(object):
    def __init__(self):
        self.copy_theme = True
        self.debug = False
        self.destination_file = 'index.html'
        self.encoding = 'utf8'
        self.embed = False
        self.linenos = 'inline'
        self.maxtoclevel = 2
        self.direct = False
        self.presenter_notes = True
        self.verbose = True
        self.relative = True
        self.theme = 'default'
        self.extensions = ''
        self.watch = False


def build():
    darkslide.cli.run(README_PATH, Options())
