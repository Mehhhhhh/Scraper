from output_handlers.base_handler import BaseHandler

class StdoutHandler(BaseHandler):
    """
    A context manager class that handles stdout
    Nothing much to do to simply send output to console
    """
    def __init__(self, *args):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        pass

    def output(self, content):
        print(content)