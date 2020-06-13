from collections import OrderedDict, Callable
from typing import List, Any, Optional, TypeVar

import pyglet

from kge.core.constants import DEFAULT_FPS
from kge.graphics.image import Image
from kge.utils.vector import Vector

T = TypeVar("T")


class Frame(object):
    """
    An animation frame

    Example of usage:
        >>> Frame(image=Image('stand1.jpg'), duration=.1)
    """

    def __init__(self, duration: float = .02, **states):
        """
        :param states: the states of the frame
        :param duration: duration in seconds
        """

        if not len(states) > 0:
            raise ValueError("Should at least add one state to the Frame")

        if not isinstance(duration, (int, float)):
            raise TypeError("duration should a number (in seconds)")
        elif duration < 1 / DEFAULT_FPS:
            raise ValueError(f"duration should not be less than {1 / DEFAULT_FPS:.3f} seconds not {duration}")

        self.states = states
        self.duration = duration

    def __getitem__(self, item: str):
        return self.states[item]

    def __repr__(self):
        return f"Animation Frame(states={self.states}, duration={self.duration} seconds)"


class EasingFunction(Callable):
    """
    Animation Function,
    if you want to create a custom easing function,
    you should subclass this class

    Example :

    >>> class CustomEasingFunction(EasingFunction):
    >>>     def compute(self, t: float) -> float:
    >>>         # t here represents the time, it goes from 0 to 1
    >>>         return t ** 3

    Note that you 'compute' method should return a value between 0 & 1, otherwise you
    will have an error.
    """

    def __call__(self, value, inMin, inMax, outMin, outMax):
        """
        Translate a value from one range to another
        """
        out = value - inMin
        out /= (inMax - inMin)

        out = self.compute(out)

        if not (0 <= out <= 1):
            raise ValueError("Your compute function should return a value between 0 and 1")

        out *= (outMax - outMin)
        return out + outMin

    def compute(self, t: float) -> float:
        raise NotImplementedError("Should be subclassed")


class Animation(object):
    """
    An animation clip
    
    Usage : 
        >>> parent = object()
        >>> run_anim = Animation(
        >>>    owner=parent,
        >>>    frames=[
        >>>       Frame(image=Image("run1.png")),
        >>>       Frame(image=Image("run2.png")),
        >>>       Frame(image=Image("run3.png"))
        >>>     ],
        >>>    loop=True,
        >>> )

    Where :
        - owner: the object which we want to apply the animation
        - frames: the frames of the animation
        - loop: set the animation as looping or not
        - function: The transition function that the animation should apply when
            passing from one frame to another.
            Use ```Animation.Lerp``` in order to get smooth animations.
    """

    # instance count
    nbItems = 0

    class Lerp(EasingFunction):
        """
        Linear Interpolation Function
        """

        def compute(self, t: float):
            return t

    def __init__(self, owner: Any, frames: List[Frame], loop: bool = True, name: str = None,
                 easing: EasingFunction = None):
        if not (isinstance(frames, (tuple, list)) and isinstance(loop, bool)):
            raise TypeError(
                'Frames should be a list of frames and loop should be a bool')

        # Can provide a Type
        if isinstance(easing, type):
            easing = easing()

        if easing is not None and not isinstance(easing, EasingFunction):
            raise ValueError(
                "Easing function should be provided, try to use 'Animation.Lerp' or subclass the class 'EasingFunction'")
        try:
            assert len(frames) > 0
        except AssertionError:
            raise ValueError("Your animation should have at least one frame in it !")

        # Set Name
        type(self).nbItems += 1

        if name is None:
            self.name = f"Animation {type(self).nbItems}"
        else:
            self.name = name

        # Frames
        self.frames = [] if frames is None else self._sample(frames, easing)  # type: OrderedDict
        self._samples = list(self.frames.values())
        self.loop = loop

        # Set length
        self.length = sum([f.duration for f in self.frames.values()])

        # Owner
        self._owner = owner
        self._next_frame = self._samples[0]  # type: Optional[Frame]
        self._cur_frame = None  # type: Optional[Frame]

        # Time stamps
        self._paused = False
        self._finished = False

        # curves
        self._fn = easing

    def _sample(self, frames: List[Frame], easing: Optional[EasingFunction]) -> OrderedDict:
        """
        Sample the animation
        :param frames: the list of frames
        :param easing: the easing Function
        :return: a Dict with
            - key: a timestamp corresponding at the time to the next frame
            - frame: a frame
        """
        if not isinstance(frames, list):
            raise TypeError("frames should be a list of frames")

        # This has to be an ordered dict because we want access from index
        samples = OrderedDict()

        if len(frames) > 0:
            samples[0] = frames[0]
        if len(frames) > 1:
            if easing is None:
                x = frames[0].duration
                for i in range(1, len(frames)):
                    samples[x] = frames[i]
                    x += frames[i].duration

            else:
                # The start variables
                len_ = sum([f.duration for f in frames[:-1]])
                lframe = frames[0]
                nframe = frames[1]

                # the timesteps
                t0 = 0
                t = t0
                t1 = lframe.duration
                while t <= len_:
                    t += 1 / DEFAULT_FPS

                    # Time should not pass the next step
                    if t >= t1:
                        t = t1

                    # get the states
                    states = {}
                    for prop, state in lframe.states.items():
                        res = easing(t, t0, t1, state, nframe[prop])
                        states[prop] = res

                    # Build a Frame
                    f = Frame(1 / DEFAULT_FPS, **states)
                    samples[t] = f

                    # if time is greater than the last frame
                    if t >= t1:
                        try:
                            nframe = frames[frames.index(nframe) + 1]
                        except IndexError:
                            pass
                        lframe = nframe
                        t0 = t
                        t1 = t + lframe.duration

                # Change the duration of the first Frame
                frames[0].duration = 1 / DEFAULT_FPS

        return samples

    @property
    def finished(self):
        return self._finished

    @property
    def paused(self):
        return self._paused

    @property
    def last_frame(self):
        i = self._samples.index(self._cur_frame) - 1
        if i == -1:
            return None
        return self._samples[i]

    @property
    def next_frame(self):
        return self._next_frame

    @property
    def current_frame(self):
        return self._cur_frame

    def restart(self):
        """
        Restart the animation
        """
        self._finished = False
        self._paused = False
        self._next_frame = self._samples[0]

    def play(self, dt=None):
        """
        Play & apply the animation
        """
        if not self._paused:
            self._update()

    def pause(self):
        """
        Pause the animation
        """
        self._paused = True

    def unpause(self):
        """
        Continue the animation
        """
        self._paused = False

    def _update(self):
        """
        Apply the properties of the current frame to the owner
        """
        # get current frame
        if self._next_frame is not None:
            self._cur_frame = self._next_frame

            # Set state only if different
            for prop, state in self._cur_frame.states.items():
                if getattr(self._owner, prop) != state:
                    setattr(self._owner, prop, state)

        # Set next frame
        next(self)

    def __next__(self):
        """
        Swap animations
        """
        if self._finished or self._paused:
            return
        else:
            i = self._samples.index(self._next_frame)

            try:
                self._next_frame = self._samples[i + 1]
            except IndexError:
                # if index out of range
                if self.loop:
                    self._next_frame = self._samples[0]
                else:
                    self._next_frame = None
                    self._finished = True
                    # Stop
                    # pyglet.clock.unschedule(self.play)

    @classmethod
    def from_sequence(cls, owner: Any,
                      images: List[Image] = [],
                      frame_duration=.02,
                      name: str = None,
                      loop: bool = True,
                      property_name='image'):
        """
        Get an image animation from a sequence of images
        """
        frames = [Frame(duration=frame_duration, **{property_name: image}) for image in images]

        # For smooth return, we copy first frame to append it to the end
        if loop:
            frames.append(Frame(**{property_name: images[0]}, duration=frame_duration))
        return Animation(
            name=name,
            owner=owner,
            frames=frames,
            loop=loop
        )

    @classmethod
    def from_spritesheet(cls,
                         owner: Any,
                         image: Image,
                         grid_size: Vector,
                         frame_duration=.02,
                         name: str = None,
                         loop: bool = True,
                         property_name='image'):
        """
        Get an image animation from a sprite sheet
        """
        images = image.slice(grid_size)
        frames = [Frame(duration=frame_duration, **{property_name: sliced}) for sliced in images]

        # For smooth return, we copy first frame to append it to the end
        if loop:
            frames.append(Frame(**{property_name: images[0]}))

        return Animation(
            name=name,
            owner=owner,
            frames=frames,
            loop=loop
        )

    def __repr__(self):
        return f"Animation(name={self.name}, frames={len(self.frames)}, length={self.length} seconds)"

    def __str__(self):
        return f"{self.name} (Animation)"


if __name__ == '__main__':
    class O:
        name = ''
        lname = ''

        def __repr__(self):
            return f"First name : {self.name}, Last Name: {self.lname}"


    frames = [
        Frame(name='kiss', lname="Boss", duration=1),
        Frame(name='game', duration=1),
        Frame(name='engine', duration=1),
        Frame(name='by', duration=1),
        Frame(name='FredKiss', lname="Badass", duration=1),
    ]

    o = O()
    anim = Animation(o, frames, loop=True)
    anim.play()


    def up(dt):
        print(o)


    pyglet.clock.schedule(up)
    pyglet.app.run()
