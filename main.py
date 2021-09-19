import random

from ursina import *
from ursina.prefabs.first_person_controller import *
from ursina.prefabs.trail_renderer import TrailRenderer
from ursina.prefabs.first_person_controller import FirstPersonController

import numpy as np

PERFECT = True

def find_gravity(a,b):
    mag = distance(a.ball,b.ball)

    grav = (a.mass * b.mass ) / mag ** 2

    v = (b.ball.position - a.ball.position)

    return v * grav * a.mass


def getfvector(a,b):
    v = find_gravity(a,b)
    arr = np.array(v)
    dt = a.velocity

    if a.perfect:
        a.velocity = np.cross(arr, (0,0,1))

    else:
        a.velocity = (dt + arr/10)

    return a.velocity


class Star:
    def __init__(self, pos = (0,0,0), mass = 1, radius = 1, c = color.black, s  = (1,1,1), acceleration = (0,0,0), perfect = False):
        self.pos = pos
        self.mass = mass
        self.radius = radius
        self.ball = Ball(position=pos, c = c, s = s)
        self.velocity = (np.random.uniform(-5,5), np.random.uniform(-5,5), np.random.uniform(-5,5))
        self.acceleration = acceleration
        self.perfect = perfect


class Ball(Button):
    def __init__(self, position = (0,0,0), c = color.black, s = (1,1,1)):
        super().__init__(
            parent = scene,
            position = position,
            model = 'sphere',
            color = c,
            highlight_color = color.blue,
            scale = s,
            collider = 'sphere',
            texture = 'sun'
        )


def addOrbiter():
    s = Star(mass=random.randint(1, 3), pos=(random.randint(-20, 20), random.randint(-20, 20), random.randint(-50, 50)),
             c=color.white, s=(0.3, 0.3, 0.3), acceleration = (np.random.uniform(-10,10), np.random.uniform(-10,10), np.random.uniform(-10,10)))
    st = TrailRenderer(parent = s.ball, thickness= 1, color = color.white, alpha = 0.1, duration = .01)
    orbiters.append(s)


def addPOrbiter():
    orbiters.append(
        Star(mass=random.randint(1, 3), pos=(random.randint(-20, 20), random.randint(-20, 20), random.randint(-50, 50)),
             c=color.white, s=(0.3, 0.3, 0.3),perfect = True, acceleration = (np.random.uniform(-1,1), np.random.uniform(-1,1), np.random.uniform(-1,1))))


stars = []
orbiters = []
background = []


def update():
    if held_keys['t']:
        addOrbiter()

    if held_keys['p']:
        addPOrbiter()

    if held_keys['c']:

        for orbiter in orbiters:
            destroy(orbiter.ball, delay=.1)

        orbiters.clear()

    for star in stars:
        for orbiter in orbiters:
            #orbiter.ball.animate_position(orbiter.ball.get_position() + getfvector(orbiter, star), duration=0.0001)
            orbiter.ball.set_position(getfvector(orbiter, star)/100 + orbiter.ball.get_position())
            #.ball.set_position(find_gravity(orbiter, star) + orbiter.ball.get_position())

            if star.ball.intersects(orbiter.ball).hit:
                destroy(orbiter.ball, delay=.01)
                orbiters.remove(orbiter)


if __name__ == '__main__':
    app = Ursina()
    #window.color = color.black
    s1 = Star(pos=(3, 3, 60), mass=5, c=color.black)

    stars.append(s1)

    s2 = Star(pos=(-3, -3, 20), mass=5)

    stars.append(s2)

    app.run()
