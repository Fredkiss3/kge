from dataclasses import dataclass
from typing import Union, Dict, Any, Type, Collection, Set, List

import kge
from kge.inputs.keys import KeyCode
from kge.inputs.mouse import MouseInput, WheelDown, WheelUp
from kge.utils.vector import Vector


class Event:
    """
    The event class
    """
    scene: 'kge.Scene' = None
    onlyEntity: Union['kge.Entity', None] = None
    time_scale: float = 1.0


"""
The events below are handled by user
"""


# @dataclass
# class PauseGame(Event):
#     """
#     Fired when we need to pause the game
#     """
#     scene: "kge.Scene" = None
#
# @dataclass
# class GamePaused(Event):
#     """
#     Fired when the game has been paused
#     """
#     scene: "kge.Scene" = None
#
# @dataclass
# class ContinueGame(Event):
#     """
#     Fired when we need to pause the game
#     """
#     scene: "kge.Scene" = None
#
# @dataclass
# class GameContinued(Event):
#     """
#     Fired when we need to pause the game
#     """
#     scene: "kge.Scene" = None
#

@dataclass
class LateUpdate(Event):
    """
    Fired when when need an update after the real update has finished
    """
    delta_time: float = 0.0
    scene: 'kge.Scene' = None


@dataclass
class MouseButtonPressed(Event):
    """
    Fired when a mouse button is pressed
    """
    button: MouseInput
    position: Vector  # Scene position
    screen_position: Vector
    scene: 'kge.Scene' = None


@dataclass
class MouseWheelUp(Event):
    """
    Fired when a mouse button is pressed
    """
    position: Vector  # Scene position
    scene: 'kge.Scene' = None


@dataclass
class MouseWheelDown(Event):
    """
    Fired when a mouse button is pressed
    """
    position: Vector  # Scene position
    scene: 'kge.Scene' = None


@dataclass
class MouseButtonReleased(Event):
    """
    Fired when a mouse button is released
    """
    button: MouseInput
    position: Vector  # Scene position
    screen_position: Vector
    scene: 'kge.Scene' = None


@dataclass
class MouseMotion(Event):
    """
    An event to represent mouse motion.
    """
    position: Vector
    screen_position: Vector
    delta: Vector
    buttons: Collection[MouseInput]
    scene: 'kge.Scene' = None


@dataclass
class KeyDown(Event):
    """
    Fired when a keyboard key is pressed
    mods represents special buttons like SHIFT, ALT, CTRL, etc
    """
    key: KeyCode
    mods: Set[KeyCode]
    scene: 'kge.Scene' = None


@dataclass
class KeyUp(Event):
    """
    Fired when a keyboard key is released
    mods represents special buttons like SHIFT, ALT, CTRL, etc
    """
    key: KeyCode
    mods: Set[KeyCode]
    scene: 'kge.Scene' = None


@dataclass
class Update(Event):
    """
    Fired when, we need to update entities,
    components and other things.
    Called at each frame
    """
    delta_time: float = 0.0
    scene: 'kge.Scene' = None


@dataclass
class Init(Event):
    """
    Fired on initialisation of an entity
    """
    scene: 'kge.Scene' = None


@dataclass
class DestroyEntity(Event):
    """
    Fired when we want to destroy an Entity
    """
    entity: "kge.Entity"
    scene: "kge.Scene" = None


@dataclass
class TimeDilation(Event):
    """
    Fired when we need to change the time scale
    """
    new_time_scale: float
    scene: "kge.Scene" = None


"""
The events below are handled by the engine
"""


@dataclass
class EntityDestroyed(Event):
    """
    Fired when an entity gets destroyed
    """
    entity: "kge.Entity"
    scene: "kge.Scene" = None


@dataclass
class PreRender(Event):
    """
    Fired before rendering.
    """
    scene: 'kge.Scene' = None


@dataclass
class WindowResized(Event):
    """
    Fired when the window has been resized
    """
    new_size: "kge.Vector"
    fullscreen: bool = False
    scene: "kge.Scene" = None


@dataclass
class FixedUpdate(Event):
    """
    Fired when physics have been updated
    """
    fixed_delta_time: float
    scene: 'kge.Scene' = None


@dataclass
class Quit(Event):
    """
    Fired on an OS Quit event.

    You may also fire this event to stop the engine.
    """
    scene: 'kge.Scene' = None


@dataclass
class Render(Event):
    """
    Fired at render.
    """
    scene: 'kge.Scene' = None


@dataclass
class Rendered(Event):
    """
    Fired when the window has been drawn
    """
    scene: 'kge.Scene' = None


@dataclass
class DisableEntity(Event):
    """
    Fired when we need to activate an entity
    """
    entity: "kge.Entity"
    scene: 'kge.Scene' = None


@dataclass
class EnableEntity(Event):
    """
    Fired when we need to deactivate an entity
    """
    entity: "kge.Entity"
    scene: 'kge.Scene' = None


@dataclass
class EntityEnabled(Event):
    """
    Fired when an entity has been activated
    """
    entity: "kge.Entity"
    scene: 'kge.Scene' = None


@dataclass
class EntityDisabled(Event):
    """
    Fired when an entity has been deactivated
    """
    entity: "kge.Entity"
    scene: 'kge.Scene' = None


@dataclass
class StartScene(Event):
    """
    Fired to start a new scene.

    new_scene can be an instance or a class. If a class, must include kwargs.
    If new_scene is an instance kwargs should be empty or None.

    Before the previous scene pauses, a ScenePaused event will be fired.
    Any events signaled in response will be delivered to the new scene.

    After the ScenePaused event and any follow up events have been delivered, a
    SceneStarted event will be sent.

    Examples:
        * `signal(new_scene=StartScene(MyScene(player=player))`
        * `signal(new_scene=StartScene, kwargs={"player": player})`
    """
    new_scene: Union['kge.Scene', Type['kge.Scene']]
    kwargs: Dict[str, Any] = None
    scene: 'kge.Scene' = None


@dataclass
class ReplaceScene(Event):
    """
    Fired to replace the current scene with a new one.

    new_scene can be an instance or a class. If a class, must include kwargs.
    If new_scene is an instance kwargs should be empty or None.

    Before the previous scene stops, a SceneStopped event will be fired.
    Any events signaled in response will be delivered to the new scene.

    After the SceneStopped event and any follow up events have been delivered,
    a SceneStarted event will be sent.

    Examples:
        * `signal(new_scene=ReplaceScene(MyScene(player=player))`
        * `signal(new_scene=ReplaceScene, kwargs={"player": player})`
    """
    new_scene: Union['kge.Scene', Type['kge.Scene']]
    kwargs: Dict[str, Any] = None
    scene: 'kge.Scene' = None


@dataclass
class SceneContinued(Event):
    """
    Fired when a paused scene continues.

    This is delivered to a scene as it resumes operation after being paused via
    a ScenePaused event.

    From the middle of the event lifetime that begins with SceneStarted.
    """
    scene: 'kge.Scene' = None


@dataclass
class SceneStarted(Event):
    """
    Fired when a scene starts.

    This is delivered to a Scene shortly after it starts. The beginning of the
    scene lifetime, ended with SceneStopped, paused with ScenePaused, and
    resumed from a pause with SceneContinued.
    """
    scene: 'kge.Scene' = None


@dataclass
class SceneStopped(Event):
    """
    Fired when a scene stops.

    This is delivered to a scene and it's objects when a StopScene or
    ReplaceScene event is sent to the engine.

    The end of the scene lifetime, started with SceneStarted.
    """
    scene: 'kge.Scene' = None


@dataclass
class ScenePaused(Event):
    """
    Fired when a scene pauses.

    This is delivered to a scene about to be paused when a StartScene event is
    sent to the engine. When this scene resumes it will receive a
    SceneContinued event.

    A middle event in the scene lifetime, started with SceneStarted.
    """
    scene: 'kge.Scene' = None


@dataclass
class StopScene(Event):
    """
    Fired to stop a scene.

    Before the scene stops, a SceneStopped event will be fired. Any events
    signaled in response will be delivered to the previous scene if it exists.

    If there is a paused scene on the stack, a SceneContinued event will be
    fired after the responses to the SceneStopped event.
    """
    scene: 'kge.Scene' = None


@dataclass
class Idle(Event):
    """
    An engine plumbing event to pump timing information to subsystems.
    """
    time_delta: float
    scene: 'kge.Scene' = None


@dataclass
class AddComponent(Event):
    """
    Fired when we need to add a component to an entity
    """
    entity: 'kge.Entity'
    key: str
    component: Type['kge.Component']
    scene: 'kge.Scene' = None


@dataclass
class ComponentAdded(Event):
    """
    Fired when we need to add a component to an entity
    """
    entity: 'kge.Entity'
    component: Union[Type['kge.Component'], "kge.Component"]
    scene: 'kge.Scene' = None


@dataclass
class RemoveComponent(Event):
    """
    Fired when we need to remove a component to an entity
    """
    entity: 'kge.Entity'
    kind: Union[Type['kge.Component'], "kge.Component", str]
    scene: 'kge.Scene' = None


@dataclass
class ComponentRemoved(Event):
    """
    Fired when we need to remove a component to an entity
    """
    entity: 'kge.Entity'
    components: List[Union[Type['kge.Component'], "kge.Component"]]
    scene: 'kge.Scene' = None


if __name__ == '__main__':
    print(Idle(.05))
