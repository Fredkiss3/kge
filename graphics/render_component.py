import kge
from kge.core.component import BaseComponent


class RenderComponen(BaseComponent):
    def render(self, scene: "kge.Scene"):
        raise NotImplementedError("This class should be subclassed")