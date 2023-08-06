from abc import ABC
from typing import Any, Dict

from interactivity.generics import ActivityHandler

from .payloads import ActionPayload

__all__ = ("ActionHandler",)


class ActionHandler(ActivityHandler[ActionPayload], ABC):
    """
    Base handler class used for block and attachment actions:
    https://api.slack.com/reference/interaction-payloads/block-actions
    """

    def __init__(self, *args, **kwargs):
        """
        Just like `ActionFactory`, assumes that a single action is submitted at a time.
        """
        super(ActionHandler, self).__init__(*args, **kwargs)
        self.action: Dict[str, Any] = self.payload.actions[0]
