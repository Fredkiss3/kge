from dataclasses import dataclass

import kge
from kge.core.events import Event


@dataclass
class AssetLoaded(Event):
    """
    Fired when an asset has been loaded
    """
    asset: 'kge.Asset'
    total_loaded: int
    total_queued: int
    scene: 'kge.Scene' = None