# from dataclasses import dataclass
#
# import kge
# from kge.core.events import Event
#
# # from typing import Type
#
# """
# User Managed events
# """
#
#
# @dataclass
# class CollisionBegin(Event):
#     """
#     Fired when two colliders begin to hit one another
#     """
#     collider: "kge.Collider"
#     scene: 'kge.Scene' = None
#
#
# @dataclass
# class CollisionEnd(Event):
#     """
#     Fired when two colliders end to hit one another
#     """
#     collider: "kge.Collider"
#     scene: 'kge.Scene' = None
#
#
# @dataclass
# class CollisionEnter(Event):
#     """
#     Fired when one collider enter inside another collider
#     """
#     collider: "kge.Collider"
#     scene: 'kge.Scene' = None
#
#
# @dataclass
# class CollisionExit(Event):
#     """
#     Fired when a collider exit outside of another collider
#     """
#     collider: "kge.Collider"
#     scene: 'kge.Scene' = None
#
#
# """
# Engine Managed Events
# """
#
#
# @dataclass
# class CreateBody(Event):
#     """
#     Fired when we need to create a body for an entity in the physics world
#     """
#     entity: 'kge.Entity'
#     rb: "kge.RigidBody"
#     scene: 'kge.Scene' = None
#
#
# @dataclass
# class BodyCreated(Event):
#     """
#     Fired when a body has been created for an entity
#     """
#     entity: 'kge.Entity'
#     rb: "kge.RigidBody"
#     scene: 'kge.Scene' = None
#
#
# @dataclass
# class PhysicsUpdate(Event):
#     """
#     Fired when we need to update the physics world
#     """
#     delta_time: float
#     scene: 'kge.Scene' = None
#
#
# @dataclass
# class DestroyBody(Event):
#     """
#     Fired when we want to destroy a rigid body
#     """
#     entity: 'kge.Entity'
#     rb: "kge.RigidBody"
#     scene: 'kge.Scene' = None
#
#
# @dataclass
# class BodyDestroyed(Event):
#     """
#     Fired when a body get destroyed
#     """
#     entity: 'kge.Entity'
#     rb: "kge.RigidBody"
#     scene: 'kge.Scene' = None
