import json

from interactivity.generics import Payload

__all__ = ("ActionPayload",)


class ActionPayload(Payload):
    """
    Assumes that the `private_metadata` attribute set on a view is valid JSON.
    If the action payload contains a view, exposes the metadata attribute as a dict.

    https://api.slack.com/reference/interaction-payloads/block-actions
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        try:
            self.metadata = json.loads(self.view["private_metadata"])
        except AttributeError:
            pass
