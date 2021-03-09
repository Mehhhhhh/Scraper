import logging

logger = logging.getLogger(__name__)

class OutputHandlerFactory:
    """
    Output handler factory to get desired output handler
    """
    _registration_table = {}

    @classmethod
    def register(cls, name, output_handler):
        """ 
        register output handler in the map

        :type name: str, name of the output handler
        :param output_handler: the output handler class being registered.
        """

        if name not in cls._registration_table.keys():
            logger.debug("registering output handler {}".format(name))
            cls._registration_table[name] = output_handler

    @classmethod
    def get_output_handlers(cls):
        """
        get all output handler in case of iteration

        :rtype: generator of iterable output handler classes
        """
        return (output_handler for output_handler in cls._registration_table.values())

    @classmethod
    def get_output_handler(cls, name):
        """
        get output handler with a certain name

        :type name: str, the name of the registered output handler.
        :rtype: output handler class.
        """
        return cls._registration_table[name]