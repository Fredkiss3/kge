# from enum import Enum, auto
import logging

import pyglet

from kge.core.constants import BLACK
from kge.resources.assetlib import AbstractAsset
from kge.utils.color import Color

logger = logging.getLogger(__name__)


class Font(AbstractAsset):
    """
    An asset for specifying fonts
    """

    def __init__(self, name: str = 'Arial',
                 file: str = None,
                 size: int = 15,
                 align: str = 'center',
                 italic: bool = False,
                 bold: bool = False,
                 color: Color = BLACK,
                 ):
        self.name = name

        self.size = size
        self.align = align
        self.style = italic
        self.weight = bold
        self.color = color
        self._filename = file

    def load(self):
        """
        :return:
        """
        try:
            if self._filename is not None:
                pyglet.font.add_file(self._filename)

            pyglet.font.load(self.name, self.size,
                             bold=self.weight,
                             italic=self.style,
                             )
        except:
            logger.error(f"The font {self._filename} has not been found")
