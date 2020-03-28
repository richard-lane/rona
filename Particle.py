"""
Class for a particle, representing a person or something

"""
import collections


"""
Encapsulate particle state

"""
particle_state = collections.namedtuple("particle_state", ["x", "y", "vx", "vy"])


class Box:
    """
    Box that the particles live in

    """

    def __init__(self, particles, position, width, height):
        """
        :param particles: iterable of particles in the box
        :param position:  low left edge of box; (x, y)
        :param width:     width of box
        :param height:    height of box

        """
        assert len(position) == 2

        self.position = position
        self.width = width
        self.height = height
        self.particles = particles


class Particle:
    """
    A particle that will move around inside a box and not collide with anything

    """

    def __init__(self, particlestate):
        """ particlestate should be a dict or namedtuple of particle properties """
        self.x = particlestate.x
        self.y = particlestate.y
        self.vx = particlestate.vx
        self.vy = particlestate.vy

    def step(self, dt):
        """
        Move this particle

        """
        self.x += self.vx * dt
        self.y += self.vy * dt
