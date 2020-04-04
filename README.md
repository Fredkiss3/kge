# KISS GAME ENGINE
### A 2D Game Engine Written in Python, running in Python and For Python Game Developpers. 

Its intend is to provide python game developpers with an easy API to learn to build their own 2D games and provide the possibility to  write little to very big games.

It is built on top of the [pyglet](https://pyglet.org) library for rendering, and a python version of a great physics engine named [Box2D](https://github.com/pybox2d/pybox2d). So you can expect it to be of top quality.

If you have any issue you can add an issue to the repository. I will be very pleased to help.

## Requirements
kge runs under python 3.7 Being written in pure Python, it also works on other Python interpreters such as PyPy. Supported platforms are:
   - Windows 7 or later
   - Linux, with the following libraries (most recent distributions will have these in a default installation):
        - OpenGL and GLX
        - GDK 2.0+ or Pillow (required for loading images other than PNG and BMP)
        - OpenAL or Pulseaudio (required for playing audio)
 
## Installation

pyglet is installable from PyPI:

    pip install --upgrade --user kge
    
## Installation from source

If you're reading this `README` from a source distribution, you can install kge with:

    python setup.py install --user
 
## Functionnalities availables :
System | Components
------------ | -------------
  Rendering | Simple Shapes (squares, circles, triangles),  Sprites with Images
  GUI | Text
  Debug | Debug the world, see colliders and bodies, draw custom shapes
  Physics Engine | Colliders (BoxColliders, CircleColiders, PolygonColliders, TriangleColliders, EdgeColliders), RigidBodies
  Audio Engine | Play Sound with volume
  Scripting | With Entities (i.e GameObjects), and Behaviours
  
### TODO
  - Level Transitions
  - Animation System :
      - Frame By Frame with Sprites
      - From Sequence of images on one Spritesheet
      - From GIF
  - Particle Sytem
  - 2D Light System
  - GUI System : with buttons, images and Text
  - Editor
