from typing import Optional, Dict, Any, Tuple, Set, Callable, Union

import kge
from kge.core.component import BaseComponent
from kge.core.constants import ALWAYS
from kge.core.events import Event, AnimChanged
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
        self.animation = anim

    def __repr__(self):
        if self.animation is None:
            return "AnimState(animation=ANY)"

        return f"AnimState(animation={self.animation})"

    def __next__(self):
        """
        Enter in the state
        """
        if self.animation is not None:
            self.animation.update()
            return self.animation.finished
        return False

    def __enter__(self):
        if self.animation is not None:
            self.animation.restart()

    def __exit__(self, *_, **__):
        pass

    def exit(self):
        if self.animation is not None:
            self.animation.stop()


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
    """

    @property
    def entity(self) -> 'kge.Entity':
        return self._entity

    @entity.setter
    def entity(self, e: 'kge.Entity'):
        if isinstance(e, kge.Entity):
            if e.getComponent(kind=Animator) is not None:
                raise AttributeError(f"There is already another Animator component attached to '{e}'")

            # set entity
            self._entity = e

    next: Optional[AnimState]
    current: AnimState

    def __init__(self, *animations: Animation):
        self._entity = None
        super().__init__()

        if not len(animations):
            raise ValueError("Your animator should have at least one animation in it !")

        self.current = AnimState(animations[0])
        self.next = None  # type: Optional[AnimState]
        self.animations = {anim.name: AnimState(anim) for anim in animations}  # type: Dict[str, AnimState]
        self.transitions = {}  # type: Dict[Tuple[AnimState, Condition], Transition]

        self._fields = {}  # type: Dict[str, Any]
        self._conditions = {ALWAYS.prop: set()}  # type: Dict[str, Set[Condition]]

    def add_field(self, name: str, default_value: Any = None):
        if not name in self._fields:
            self._fields[name] = default_value
            self._conditions[name] = set()
        else:
            raise ValueError("This field is already in the animator")

    def __setitem__(self, key, value):
        """
        Set a field
        """
        self._fields[key] = value

        # Check all conditions to get a valid condition
        for cd in self._conditions[key]:
            # If from ANY, then check condition
            t = self.transitions.get((ANY, cd), False)

            if t:
                if cd.resolve(self):
                    state = AnimState(t.next)
                    if self.next != state:
                        self.next = state
                    return
            else:
                t = self.transitions.get((self.current, cd), False)
                if cd.resolve(self) and t:
                    # Set current animation
                    state = AnimState(t.next)
                    if self.next != state:
                        self.next = state
                    return

    def update(self, dispatch: Callable[[Event], None]):
        if self.next is not None:
            # Dispatch Animation Changed
            if self.next is not None:
                dispatch(
                    AnimChanged(previous=self.current.animation, next=self.next.animation, entity=self.entity)
                )

                with self.next:
                    pass

                self.current = self.next
                self.next = None

        # update the current animation
        finished = next(self.current)

        if finished:
            t = self.transitions.get((self.current, ALWAYS), None)

            if t is not None:
                # Dispatch Animation Changed
                dispatch(
                    AnimChanged(previous=self.current.animation, next=t.next, entity=self.entity)
                )

                state = AnimState(t.next)
                if self.current != state:
                    # Exit (Stop the animation)
                    if state is not None:
                        with state:
                            pass

                    self.current = state

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
            raise KeyError(f"The condition {forward_condition} is not in animator")

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
