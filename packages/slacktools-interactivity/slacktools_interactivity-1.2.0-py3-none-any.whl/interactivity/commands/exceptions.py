from interactivity.exceptions import InteractivityError
from interactivity.generics import Payload

__all__ = ("CommandValidationError",)


class CommandValidationError(InteractivityError):
    """
    Raised when the text provided from a command payload is invalid for the command.
    """

    def __init__(self, payload: Payload, message: str = None):
        """
        :param payload: The CommandPayload from the failed Command.
        :param message: Optional, message to use for the exception.
        """
        self.payload = payload
        if not message:
            message = f"{payload.command} {payload.text}, is not a valid command."
        super(CommandValidationError, self).__init__(message)
