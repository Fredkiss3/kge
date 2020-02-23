"""
PYBOX2D Usage :

1 - Create World
2 - add bodies

3 - for every body in the world, add definitions :
    - definition is all the information of the body
    such as ``body type``, ``bounciness (restitution)``,
      ``mass``, ``friction``, etc.



"""
from pygame.time import Clock
import math
from Box2D import *
import Box2D as b2

# World creation
world = b2.b2World()

# create body definition with position
# Definition contain fixtures
groundBodyDef = b2.b2BodyDef()
groundBodyDef.position = (0, -10)

# Create the Body
# Make a body fitting this definition in the world.
# create Body create a statuc body
groundBody = world.CreateBody(groundBodyDef)

# Create the ground shape
# box ==> (width / 2 , height / 2)
groundBox = b2.b2PolygonShape(box=(50, 10))

# And create a fixture definition to hold the shape
groundBoxFixtureDef = b2.b2FixtureDef(shape=groundBox)

# Add the ground shape to the ground body.
# Fixture contains different shapes for a body
groundBody.CreateFixture(groundBoxFixtureDef)

# All these lines, can be summarized with :
world = b2World()

# create static body
groundBody = world.CreateStaticBody(
    # set position
    position=(0, 0),
    # set shape
    shapes=b2PolygonShape(box=(50, 2)),
)

# dynamic body
body = world.CreateDynamicBody(position=(0, 15), angle=math.radians(0))


class Player:
    health = 0


# fixture def
# Fixture contains :
#   shape,              ==> shape
#   density,            ==> density is computed to set mass (fixture mass)
#   userData,           ==> any Custom Data
#   sensor flag         ==> if the shape is a Trigger
#   restitution,        ==> bounciness
#   friction            ==> if it need to slide
bodyFixtureDef = b2.b2FixtureDef(
    shape=b2PolygonShape(box=(1, 1)),
    density=1,
    friction=0.1,
    restitution=1,
    userData=Player(),
    isSensor=True
)

# fixture holds shape, density, friction and bounciness (restitution)
# if bounciness is set to 1, the body will bounce to the starting point infinitely
# if bounciness is set to lower than 1, it will bounce to a lower point each time
# if bounciness is set to greater than 1, it will bounce to a higher point each time
box = body.CreateFixture(bodyFixtureDef)

# ThIS IS EQUIVALENT
box2 = body.CreateFixture(
    shape=b2PolygonShape(box=(1, 1)),
    density=1,
    friction=0.1,
    restitution=1,
    userData=Player(),
    isSensor=True
)

# By setting fixtures filters
# We can filter collisions
# If set to negative value, they will never collide
# Cool for layer based collisions
#
# FIXME : CANNOT SET GROUP INDEX OF STATIC BODIES
bodyFixtureDef.filter.grounpIndex = -2
groundBoxFixtureDef.filter.grounpIndex = -2

body2Def = b2.b2BodyDef(
    position=(1, 5),
    angle=math.radians(25),
    linearDamping=.5, # Damping is to make bodies look floaty
    type=b2.b2_dynamicBody,
    active=True,  # If a body is inactive, it is here but does participate to physics
    bullet=True,  # If the body is a really fast moving object
    allowSleep=True,  # allow the body to sleep
    awake=True,  # If the body is awake or not
    fixedRotation=False,  # Fix rotation
    userData=Player(),  # Can add userData for the body
    gravityScale=.1,  # The intensity of gravity to the body
)



for defi in dir(body2Def):
    print(defi)

print()
print()
for defi in dir(bodyFixtureDef):
    print(defi)

print()
print()
for defi in dir(b2PolygonShape(box=(1, 1))):
    print(defi)
# help(body2Def)
exit(0)

body2 = world.CreateBody(
    body2Def
)

# Set linear velocity in order to give the body a velocity
body2.linearVelocity = (5, 5)
body2.angularVelocity = 4

# Destroy Fixture
# fixture = body.CreateFixture(b2FixtureDef(...))
# body.DestroyFixture(fixture)

# body2.massData = b2.b2MassData(
#
# )

# ApplyForce
# body.ApplyForce(force=(fx,fy), point=(px,py))
# body.ApplyTorque(0.0)
# body.ApplyLinearImpulse(impulse=(ix,iy), point=(px,py))
# body.ApplyAngularImpulse(impulse=0.0)


# class callB(b2.b2RayCastCallback):
#     def ReportFixture(self, fixture, point, normal, fraction):
#         print(fixture, point, normal, fraction)
#
# # Launch a raycast
# world.RayCast(callB(), (1, 1), (0, 2))


if __name__ == '__main__':
    import time

    clock = Clock()

    last_idle = time.monotonic()


    def ceil(x):
        y = x - int(x)

        if y >= 0.5:
            # get up
            return math.ceil(x)
        else:
            # get down
            return math.floor(x)


    while True:
        now = time.monotonic()
        delta = now - last_idle
        last_idle = now

        # recommanded values
        vel_iters, pos_iters = 10, 10  # 6, 2
        world.Step(delta, vel_iters, pos_iters)

        # Clear applied body forces. We didn't apply any forces, but you
        # should know about this function.
        world.ClearForces()
        # world = b2World()

        print((ceil(body.position.x), ceil(body.position.y)), ceil(math.degrees(body.angle)) % 360)

        clock.tick(60)
