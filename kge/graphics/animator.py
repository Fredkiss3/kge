from typing import Optional, Dict, Any, Tuple, Set, Callable, Union

import pyglet

import kge
from kge.core.component import BaseComponent
from kge.core.constants import ALWAYS
from kge.core.events import AnimChanged, Init
from kge.graphics.animation import Animation
from kge.utils.condition import Condition


class AnimState(object):
    """
    An animation state holding the value of an animation
    """
    _cache = {}

    def __new__(cls, anim: Animation = None):
        try:
            return cls._cache[anim]
        except KeyError:
            inst = super().__new__(cls)
            cls._cache[anim] = inst
            return inst

    def __init__(self, anim: Animation = None):
        self.state = anim

    def __repr__(self):
        if self.state is None:
            return "AnimState(animation=ANY)"

        return f"AnimState(animation={self.state})"

    def __next__(self):
        """
        Enter in the state
        """
        if self.state is not None:
            if not self.state.paused:
                self.state.play()
            return self.state.finished
        return False

    def __enter__(self):
        if self.state is not None:
            self.state.restart()

    def __exit__(self, *_, **__):
        pass


class Transition(object):
    """
    A transition between two animations
    """

    def __init__(self, prev: Optional[Animation], next: Animation):
        self.next = next
        self.previous = prev

    def __repr__(self):
        return f"Transition between {self.previous} and {self.next}"


class Animator(BaseComponent):
    """
    A component that controls which animation to play

    Usage :
        >>> animation1 = Animation()
        >>> animation2 = Animation()
        >>> animator = Animator(animation1, animation2)
        >>>
        >>> e = kge.Entity()
        >>> e.addComponent(animator)
    """

    @property
    def entity(self) -> 'kge.Entity':
        return self._entity

    @entity.setter
    def entity(self, e: 'kge.Entity'):
        if not isinstance(e, kge.Entity) and e is not None:
            raise TypeError(f"Entity should be provided")

        elif e is not None:
            if e.getComponent(kind=Animator) is not None:
                raise AttributeError(f"There is already another Animator component attached to '{e}'")

        # set entity
        self._entity = e

    def __init__(self, first_animation: Animation, *animations: Animation):
        self._entity = None
        super().__init__()

        if first_animation is None:
            raise ValueError("Your animator should have at least one animation in it !")

        self.current = None  # type: Optional[AnimState]
        self.next = AnimState(first_animation)  # type: Optional[AnimState]
        self.animations = {anim.name: AnimState(anim) for anim in
                           [first_animation, *animations]}  # type: Dict[str, AnimState]
        self.transitions = {}  # type: Dict[Tuple[AnimState, Condition], Transition]

        self._conditions = {ALWAYS.prop: set()}  # type: Dict[str, Set[Condition]]

        # If the animator is suspended or not
        self._pending = False
        self._paused = False
        self._dispatch = None  # type: Optional[Callable]

        self._fields = {}  # type: Dict[str, Any]

    @property
    def pending(self):
        return self._pending

    @property
    def paused(self):
        return self._paused

    def add_field(self, name: str, default_value: Any = None):
        if not name in self._fields:
            self._fields[name] = default_value
            self._conditions[name] = set()
        else:
            raise ValueError("This field is already in the animator")

    def _swap_anims(self, anim: AnimState):
        """
        Swap the animations
        """
        # Restart the animations
        if anim is not None:
            with anim, self.current:
                pass
        self.next = anim

    def _update(self):
        """
        Apply animations states to object
        """
        dispatch = self._dispatch

        self.current = self.next
        finished = next(self.current)

        # If finished and not paused, advance
        if finished and not self.current.state.paused:
            t = self.transitions.get((self.current, ALWAYS), None)

            # Find the next animation to play
            # If there is None, then set next to None
            state = None

            if t is not None:
                # Dispatch Animation Changed
                if dispatch is not None:
                    dispatch(
                        AnimChanged(previous=self.current.animation, next=t.next, entity=self.entity)
                    )

                state = AnimState(t.next)

            self._swap_anims(state)

    def pause(self):
        """
        Pause the animator,
        Stops the execution of the animator and pauses the animation
        """
        if self.current.state is not None:
            self.current.state.pause()
        pyglet.clock.unschedule(self.animate)

    def unpause(self):
        """
        Unpause the animator and continue
        """
        if self.current.state is not None:
            self.current.state.unpause()
        self.animate()

    def animate(self, dt=None):
        if not self._pending:
            self._update()

        if self.next is not None:
            pyglet.clock.schedule_once(self.animate, self.current.state.current_frame.duration)
        else:
            self._pending = True

    def get(self, key: str):
        return self.__getitem__(key)

    def set(self, **kwargs):
        for key, val in kwargs.items():
            self.__setitem__(key, val)

    def __setitem__(self, key, value):
        """
        Set a field
        """
        try:
            self._fields[key]
        except KeyError:
            self.add_field(key, value)
        else:
            self._fields[key] = value

            # Check all conditions to get a valid condition
            for cd in self._conditions[key]:
                # If from ANY, then check condition
                t = self.transitions.get((ANY, cd), None)

                if t is not None:
                    if cd.resolve(self):
                        state = AnimState(t.next)
                        if self.next != state:
                            self._swap_anims(state)

                            # Reanimate if dead
                            if self._pending:
                                self._pending = False
                                self.animate()
                        return
                else:
                    t = self.transitions.get((self.current, cd), None)
                    if cd.resolve(self) and t is not None:
                        # Set current animation
                        state = AnimState(t.next)
                        if self.next != state:
                            self._swap_anims(state)

                            # Reanimate if dead
                            if self._pending:
                                self._pending = False
                                self.animate()
                        return

    def __getitem__(self, item):
        try:
            return self._fields[item]
            # Do this to match python default behavior
        except KeyError:
            raise AttributeError(f"No such field in animator '{item}'")

    def __getattr__(self, attr):
        try:
            return self.__getitem__(attr)
        # Do this to match python default behavior
        except KeyError:
            raise AttributeError(f"No such field in animator '{attr}'")

    def __repr__(self):
        return f"component Animator({self.animations}) of entity '{self.entity}'"

    def on_init(self, ev: Init, dispatch):
        """
        Start Animations
        """
        # Start
        self.animate()

    @property
    def conditions(self):
        return self._conditions

    @property
    def fields(self):
        return self._fields

    def add_transition(self, from_: Union[Animation, AnimState], to: Animation, forward_condition: Condition = ALWAYS,
                       back_condition: Condition = None):
        """
        Add a transition between two animations.

        :param from_: the animation where the transition begin
        :param to: the animation where the transition should go next
        :param forward_condition: the condition to fulfill in order to switch to the next animation
        :param back_condition: the condition to fulfill in order to switch back to the previous animation

        Usage :
            >>> animator.add_transition(
            >>>     from_=idle, to=run,
            >>>     forward_condition=Condition(is_running=True),
            >>>     back_condition=Condition(is_running=False)
            >>> )
        """
        if forward_condition != ALWAYS and (not forward_condition.prop in self._conditions):
            raise KeyError(f"The field {forward_condition.prop} is not registered in animator")

        # Add conditions
        self._conditions[forward_condition.prop].add(forward_condition)

        if back_condition is not None:
            if not back_condition.prop in self._conditions:
                raise KeyError(f"The condition {back_condition} is not in animator")
            else:
                self._conditions[forward_condition.prop].add(forward_condition)

        # Create transitions for the animations states
        if from_ == ANY:
            self.transitions[(ANY, forward_condition)] = Transition(None, to)
        else:
            if not from_.name in self.animations:
                raise AttributeError(f"the animation '{from_.name}' is not in animator")
            else:
                self.transitions[(self.animations[from_.name], forward_condition)] = Transition(from_, to)

        if not to.name in self.animations:
            raise AttributeError(f"the animation '{to}' is not in animator")

        if back_condition is not None and from_ != ANY:
            self.transitions[(self.animations[to.name], back_condition)] = Transition(to, from_)
            self._conditions[back_condition.prop].add(back_condition)


ANY = AnimState(None)

if __name__ == '__main__':
    from kge.utils.condition import C

    c1 = C(speed__gt=.1)
    c2 = C(speed__lt=1)
    c3 = C(is_jumping=True)

    o = object()
    o.speed = 1
    o.jumping = True

    idle = Animation(o, [])
    run = Animation(o, [])
    animator = Animator(idle, run)
