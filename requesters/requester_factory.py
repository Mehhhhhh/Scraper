import logging

logger = logging.getLogger(__name__)

class RequesterFactory:
    """
    Requester factory to get desired requester
    """
    _registration_table = {}

    @classmethod
    def register(cls, name, requester):
        """ 
        register requester in the map

        :type name: str, name of the requester
        :param requester: the requester class being registered.
        """

        if name not in cls._registration_table.keys():
            logger.debug("registering requester {}".format(name))
            cls._registration_table[name] = requester

    @classmethod
    def get_requesters(cls):
        """
        get all requesters in case of iteration

        :rtype: generator of iterable requester classes
        """
        return (requester for requester in cls._registration_table.values())

    @classmethod
    def get_requester(cls, name):
        """
        get requester with a certain name

        :type name: str, the name of the registered requester.
        :rtype: requester class.
        """
        return cls._registration_table[name]