from interactivity.generics import HandlerFactory

from .handlers import ActionHandler
from .payloads import ActionPayload

__all__ = ("ActionFactory",)


class ActionFactory(HandlerFactory[ActionHandler]):
    """
    Factory that initializes a `ActionHandler` using the Slack request payload.
    """

    @classmethod
    def extract_key(cls, payload: ActionPayload) -> str:
        """
        Assumes that a single action is submitted at a time. I have not run across
        a situation where this isn't the case but if I do I will update this interface.
        """
        return payload.actions[0]["action_id"]
