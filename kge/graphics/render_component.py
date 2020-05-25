import kge
from kge.core.component import BaseComponent


class RenderComponent(BaseComponent):
    """
    Generic Render Component
    """
    def render(self, scene: "kge.Scene"):
        raise NotImplementedError("This class should be subclassed")