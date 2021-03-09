from abc import ABC, abstractmethod

class BaseHandler(ABC):
    """
    Abstract base class for all output handlers, this defines the common interfaces of concrete.
    output handlers to output data source.
    """

    @abstractmethod
    def __enter__(self):
        """
        Preparation before handling output, opening file, opening db connection, etc.
        """
        pass

    @abstractmethod
    def __exit__(self, *exc):
        """
        Finalization after output handling, closing file, closing db connections, etc.

        :type exc: arguments related to exception informations
        """
        pass

    @abstractmethod
    def output(self, formatted_content):
        """
        Output formatted content. Usually formatted_content should be from resource controllers.

        :type formatted_content: str, for this simple scraper case, we will get formatted_content from DataSource.
        """
        pass