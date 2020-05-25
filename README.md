# KISS GAME ENGINE

KISS GAME ENGINE (`kge`) is a 2D Game Engine written in Python, running in Python and For Python Game Developers.

Its intend is to provide python game developers with an easy API to learn to build their own 2D games and provide the possibility to write from little to very big games.

It is built on top of the [pyglet][pyglet] library for rendering, and a python version of the great physics engine [Box2D](https://github.com/pybox2d/pybox2d). So you can expect it to be of top quality.

If you have any issue you can add an issue to the repository. The community will be very pleased to help.

## Requirements

kge runs only under `python 3.7` only in windows. So only python is required.

## Installation

kge can be installed from PyPI:

    pip install --upgrade --user kge

## Installation from source

If you're reading this `README` from a source distribution, you can install kge with:

    python -m pip install .

## Getting started

To get started to create your first scene, add an image named `player.png` to your game folder and start with the code :

```python
import kge
from kge import *

class Player(Sprite):
    def on_update(self, event: kge.events.Update, dispatch):
        self.position += Vector.Right() * event.delta_time

def setup(scene: Scene):
    scene.add(Player(image='player.png'))

kge.run(setup)
```

## Get Involved

The fastest way to get involved is to check out the [ongoing
discussions.](https://github.com/Fredkiss3/kge/issues?q=is%3Aissue+is%3Aopen+label%3Adiscussion)
If you're already using `kge` feel free to report bugs, suggest enhancements, or ask for new features.

If you want to contribute code, definitely read the relavant portions
of Contributing.MD

## Kiss Game Engine Design Principles

The engine uses Event System to run almost everything in the game. you can see it from the method `on_update` in the code above. you will notice further that every event of the engine has the same signature i.e `on_event_name(self, event_type, dispatch_function)`. to see all of the events available checkout the [List of events][events].

We want our users to start really easily on making game so each of the functions, constants and classes are available on the top level module, no need to to import manually all of the stuff like :

```python
from kge import Vector

v = Vector.Left()
```

Instead you can use directly with :

```python
from kge import *

v = Vector.Left()
```

## Kiss Game Engine RoadMap

So far we have done :

- Animations [see docs here][anim docs]
- Audio (Only wav and ogg files) [See docs here][audio docs]
- Physics [See docs here][physics docs]
- Sprites [See docs here][sprite docs]
- A behavior system [See docs here][behaviour docs]
- Scene Management [See docs here][scene docs]
- UI System [See docs here][ui docs]
- Debug Draw [See docs here][debug docs]

Our next functionnalities we are excited to give the users are :

- A Particle System
- Light System
- Editor
- Simple way of saving advancement
- Joystick Management

<!-- We are also looking to improve most of the systems we have built so far :

    - Add More elements to UI like : progress bars, Text Fields, listviews, checkboxes, comboboxes, etc
    - Improve Debug Draw to be less performance reducing
    - Add mp3 support for audio system
    - Add More elements to physics : Joints, Pass Through Colliders, Capsule Colliders
    - Improve our rendering system -->
<!-- Correct link -->

[pyglet]: https://pyglet.org
[events]: https://readthedocs.org/projects/kge/user_guide/events
[anim docs]: https://readthedocs.org/projects/kge/user_guide/animations
[audio docs]: https://readthedocs.org/projects/kge/user_guide/audio
[physics docs]: https://readthedocs.org/projects/kge/user_guide/physics
[sprite docs]: https://readthedocs.org/projects/kge/user_guide/images
[behaviour docs]: https://readthedocs.org/projects/kge/user_guide/behaviors
[scene docs]: https://readthedocs.org/projects/kge/user_guide/scene
[ui docs]: https://readthedocs.org/projects/kge/user_guide/ui
[debug docs]: https://readthedocs.org/projects/kge/user_guide/debug
