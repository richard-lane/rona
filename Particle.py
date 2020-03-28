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

    def __init__(self, particles):
        """
        :param particles: iterable of Particles

        """
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
