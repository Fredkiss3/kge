import time
from typing import List, Any, Optional, TypeVar

from kge.core.constants import DEFAULT_FPS
from kge.graphics.image import Image
from kge.utils.vector import Vector

T = TypeVar("T")


class Frame(object):
    """
    An animation frame
    """

    def __init__(self, duration: float = .02, **states):
        """
        :param states: the states of the animations
        :param duration: duration in seconds

        Example of usage:
            >>> Frame(image=Image('stand1'), duration=.1)
        """

        if not len(states) > 0:
            raise ValueError("Should at least add one state to the Frame")

        if not isinstance(duration, (int, float)):
            raise TypeError("duration should a number (in seconds)")
        elif duration < 1 / DEFAULT_FPS:
            raise ValueError(f"duration should not be less than {1 / DEFAULT_FPS:.3f} seconds")

        self.states = states
        self.duration = duration

    def __getitem__(self, item: str):
        return self.states[item]

    def __repr__(self):
        return f"Animation Frame(states={self.states}, duration={self.duration} seconds)"


class Animation(object):
    """
    An animation clip
    
    Usage : 
        >>> run_anim = Animation(
        >>>    owner=parent,
        >>>    frames=[Frame(image=run1), Frame(image=run2), Frame(image=run3)],
        >>>    loop=True,
        >>>    function=Step
        >>> )

    Where :
        - owner: the object which we want to apply the animation
        - frames: the frames of the animation
        - loop: set the animation as looping or not
        - function: The transition function that the animation should apply when
            passing from one frame to another.
            Use ```Animation.Smooth``` in order to get smooth animations.
    """

    # Override this to change the clock used for frames.
    _clock = time.monotonic
    nbItems = 0

    # Animation Curves
    class Fn:
        pass

    Smooth = Fn()  # For smooth animations
    Step = Fn()  # For immediate animations

    def __init__(self, owner: Any, frames=None, loop: bool = True, name: str = None, function: Fn = Step):
        if frames is None:
            frames = []
        if not (isinstance(len(frames), int) and isinstance(loop, bool)):
            raise TypeError(
                'Frames should be a list of frames and property should be a string and loop should be a bool')

        if not function in [Animation.Step, Animation.Smooth]:
            raise ValueError("Curve should be a value in list : [Animation.Step, Animation.Lerp]")
        try:
            assert len(frames) > 0 or hasattr(self, 'const')
        except AssertionError:
            raise ValueError("Your animation should have at least one frame in it !")

        # Set Name
        type(self).nbItems += 1

        if name is None:
            self.name = f"Animation {type(self).nbItems}"
        else:
            self.name = name

        self.frames = frames  # type: List[Frame]
        self.loop = loop

        # Set length
        self.length = sum([f.duration for f in self.frames])

        self._owner = owner
        self._last_frame = None  # type: Optional[Frame]
        self._cur_frame = frames[0]  # type: Optional[Frame]
        self._next_frame = None  # type: Optional[Frame]

        # Time stamps
        self._cur_time = 0
        self._last_ftime = 0
        self._t_dep = 0
        self._stopped = False

        # curves
        self._fn = function

    @property
    def finished(self):
        return False if self.loop else (
                (self._cur_frame is not None
                 and self.frames.index(self._cur_frame) == len(self.frames) - 1)
                or self._stopped
        )

    def update(self):
        """
        Apply the properties to owner
        :return:
        """
        frame = next(self)
        # print(self.frames.index(frame), len(self.frames) - 1, self.finished)

        if frame is not None:
            # Set state only if different
            for prop, state in frame.states.items():
                if self._fn == Animation.Step:
                    if getattr(self._owner, prop) != state:
                        setattr(self._owner, prop, state)
                elif self._fn == Animation.Smooth:
                    p = (self._cur_time - self._last_ftime) / frame.duration

                    try:
                        val = self.lerp(state, self._next_frame[prop], p)
                    except TypeError:
                        if getattr(self._owner, prop) != state:
                            setattr(self._owner, prop, state)
                    else:
                        if getattr(self._owner, prop) != val:
                            setattr(self._owner, prop, val)

    @property
    def last_frame(self):
        return self._last_frame

    @property
    def next_frame(self):
        return self._next_frame

    @property
    def current_frame(self):
        return self._cur_frame

    @staticmethod
    def lerp(a: T, b: T, p: float) -> T:
        """
        Linear interpolation function
        """
        return a + (b - a) * p

    def restart(self):
        self._t_dep = 0
        self._cur_frame = None
        self._stopped = False

    def stop(self):
        self._t_dep = 0
        self._cur_frame = None
        self._stopped = True

    # @property
    def __next__(self) -> Optional[Frame]:
        """
        :return:
        """
        if self._stopped:
            return None

        self._cur_time = self._clock()

        if self._t_dep == 0:
            self._t_dep = self._cur_time
            self._last_ftime = self._cur_time
            self._cur_frame = self.frames[0]
            self._last_frame = self._cur_frame

            if len(self.frames) > 1:
                self._next_frame = self.frames[1]
            else:
                self._next_frame = self._cur_frame

            return self._cur_frame
        else:
            if self._cur_time - self._t_dep > self.length + .04:
                # If arrived to the end of the animation
                # FIXME : SKIPPING THE LAST FRAME ?
                if self.loop:
                    self._t_dep = 0
                else:
                    self.stop()
                self._last_ftime = self._cur_time
                self._last_frame = self._cur_frame
                self._cur_frame = self.frames[-1]
                self._next_frame = self.frames[0]

                return self._cur_frame
            elif self._cur_time >= self._last_ftime + self._cur_frame.duration:
                # Change Frame
                self._last_ftime = self._cur_time

                i = self.frames.index(self._cur_frame) + 2
                if i >= len(self.frames):
                    i = -1

                self._last_frame = self._cur_frame
                self._cur_frame = self._next_frame
                self._next_frame = self.frames[i]

        return self._cur_frame

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
    import pyglet


    class O:
        name = ''
        lname = ''

        def __repr__(self):
            return f"First name : {self.name}, Last Name: {self.lname}"


    frames = [
        Frame(name='kiss', lname="Boss"),
        Frame(name='game'),
        Frame(name='engine'),
        Frame(name='by'),
        Frame(name='FredKiss', lname="Badass"),
    ]

    o = O()
    anim = Animation(o, frames, loop=True)


    def up(dt):
        anim.update()
        print(o)


    pyglet.clock.schedule(up)
    pyglet.app.run()
