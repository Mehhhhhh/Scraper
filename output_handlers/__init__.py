from output_handlers. output_handler_factory import OutputHandlerFactory

# register all possible output handlers
from output_handlers.file_handler import FileHandler
from output_handlers.stdout_handler import StdoutHandler

OutputHandlerFactory.register("console", StdoutHandler)
OutputHandlerFactory.register("file", FileHandler)