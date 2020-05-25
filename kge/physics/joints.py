from typing import Optional

from kge.core.component import BaseComponent
from kge.core.entity import BaseEntity
from kge.physics.rigid_body import RigidBody
from kge.utils.vector import Vector


class Joint(BaseComponent):
    """
    A Joint is a constraint between two RigidBodies
    TODO
    """

    def __init__(self,
                 attachedBody: RigidBody = None,
                 attachedAnchor: Vector = Vector.Zero(),
                 anchor: Vector = Vector.Zero(),
                 ):
        super().__init__(None)
        # TODO : Check types

        # set the entity
        self._entity = None  # type: Optional[BaseEntity]

        # parent rigid body
        self._parent_rb = None # type: Optional[RigidBody]
        self._anchor = anchor

        # Attached RigidBody
        self._attached_rb = attachedBody
        self._attached_anchor = attachedAnchor

    @property
    def entity(self) -> BaseEntity:
        return self._entity

    @entity.setter
    def entity(self, e: BaseEntity):
        if isinstance(e, BaseEntity):
            rb = e.getComponent(kind=RigidBody)
            if rb is None:
                raise AttributeError(f"Add a RigidBody to your entity before adding a Joint")

            # set entity
            self._entity = e
            self._parent_rb = rb

