from dataclasses import dataclass
from typing import Type

import Box2D

import kge
from kge.core.events import Event

"""
User Managed events
"""


@dataclass
class CollisionEnter(Event):
    """
    Fired when one collider enter inside another collider
    """
    collider: "kge.Collider"
    scene: 'kge.Scene' = None


@dataclass
class CollisionExit(Event):
    """
    Fired when a collider exit outside of another collider
    """
    collider: "kge.Collider"
    scene: 'kge.Scene' = None


"""
Engine Managed Events
"""


@dataclass
class CreateBody(Event):
    """
    Fired when we need to create a body for an entity in the physics world
    """
    entity: 'kge.Entity'
    body_component: "kge.RigidBody"
    scene: 'kge.Scene' = None


@dataclass
class BodyCreated(Event):
    """
    Fired when a body has been created for an entity
    """
    entity: 'kge.Entity'
    body: 'Box2D.b2Body'
    scene: 'kge.Scene' = None


@dataclass
class PhysicsUpdate(Event):
    """
    Fired when we need to update the physics world
    """
    delta_time: float
    scene: 'kge.Scene' = None


@dataclass
class DestroyBody(Event):
    """
    Fired when we want to destroy a rigid body
    """
    entity: 'kge.Entity'
    body_component: "kge.RigidBody"
    scene: 'kge.Scene' = None


@dataclass
class BodyDestroyed(Event):
    """
    Fired when a body get destroyed
    """
    entity: 'kge.Entity'
    body: 'Box2D.b2Body'
    scene: 'kge.Scene' = None
