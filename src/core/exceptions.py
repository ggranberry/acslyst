class LLMException(Exception):
    """Exception raised when there is an issue dealing with the LLM

    Attributes:
        message -- explanation of the error
        original_exception -- the original exception that caused this custom error to be raised
    """

    def __init__(
        self,
        original_exception=None,
    ):
        self.message = "An error has occured when calling the LLM"
        self.original_exception = original_exception
        super().__init__(
            f"{self.message}: {str(original_exception)}"
        )  # Include original exception message

class HeuristicException(Exception):
    """Exception raised when there is an issue running the heuristic

    Attributes:
        message -- explanation of the error
        original_exception -- the original exception that caused this custom error to be raised
    """

    def __init__(
        self,
        original_exception=None,
    ):
        self.message = "An error has occured when running the heuristic"
        self.original_exception = original_exception
        super().__init__(
            f"{self.message}: {str(original_exception)}"
        )  # Include original exception message

class RepairException(Exception):
    """Exception raised when there is an issue repairing a program

    Attributes:
        message -- explanation of the error
        original_exception -- the original exception that caused this custom error to be raised
    """

    def __init__(
        self,
        original_exception=None,
    ):
        self.message = "An error has occured when repairing the program"
        self.original_exception = original_exception
        super().__init__(
            f"{self.message}: {str(original_exception)}"
        )  # Include original exception message


class WPException(Exception):
    """Exception raised when there is an issue dealing with Frama-C's WP tool

    Attributes:
        message -- explanation of the error
        original_exception -- the original exception that caused this custom error to be raised
    """

    def __init__(
        self, original_exception=None
    ):
        self.message = "An error has occured when executing WP"
        self.original_exception = original_exception
        super().__init__(
            f"{self.message}: {str(original_exception)}"
        )  # Include original exception message


class PathcrawlerException(Exception):
    """Exception raised when there is an issue dealing with Frama-C's Pathcrawler tool

    Attributes:
        message -- explanation of the error
        original_exception -- the original exception that caused this custom error to be raised
    """

    def __init__(
        self,
        original_exception=None,
    ):
        self.message = "An error has occured when executing Pathcrawler"
        self.original_exception = original_exception
        super().__init__(
            f"{self.message}: {str(original_exception)}"
        )  # Include original exception message

class EvaException(Exception):
    """Exception raised when there is an issue dealing with Frama-C's Eva

    Attributes:
        message -- explanation of the error
        original_exception -- the original exception that caused this custom error to be raised
    """

    def __init__(
        self,
        original_exception=None,
    ):
        self.message = "An error has occured when executing Eva"
        self.original_exception = original_exception
        super().__init__(
            f"{self.message}: {str(original_exception)}"
        )
