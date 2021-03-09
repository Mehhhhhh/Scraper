from output_handlers.base_handler import BaseHandler

class FileHandler(BaseHandler):
    """
    A context manager class that handles file IO
    """
    def __init__(self, file_path):
        self.path = file_path

    def __enter__(self):
        self.file = open(self.path, "a+")
        return self

    def __exit__(self, *exc):
        self.file.close()

    def output(self, content):
        """
        Write content into file

        :type content: str
        """
        self.file.write(content)
        self.file.flush()


    