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

        # Check our particles all start inside the box
        for particle in particles:
            assert position[0] < particle.x < position[0] + width
            assert position[1] < particle.y < position[1] + height

        self.position = position
        self.width = width
        self.height = height
        self.particles = particles

    def step(self, dt):
        """
        Move all particles in the box and process collisions

        """
        for particle in self.particles:
            particle.step(
                dt,
                self.position[0],
                self.position[0] + self.width,
                self.position[1],
                self.position[1] + self.height,
            )
            if not particle.alive:
                self.particles.remove(particle)


class Particle:
    """
    A particle that will move around inside a box

    """

    def __init__(self, particlestate):
        """ particlestate should be a dict or namedtuple of particle properties """
        self.x = particlestate.x
        self.y = particlestate.y
        self.vx = particlestate.vx
        self.vy = particlestate.vy
        self.alive = True

    def step(self, dt, left, right, bottom, top):
        """
        Move this particle, colliding from walls on the L/R/T/B

        """
        self.x += self.vx * dt
        self.y += self.vy * dt

        # If we have gone past a barrier, reflect the particle in the barrier
        # If a particle crosses the top barrier, it dies
        if self.x > right:
            self.x = 2 * right - self.x
            self.vx *= -1
        elif self.x < left:
            self.x = 2 * left - self.x
            self.vx *= -1
        if self.y > top:
            self.alive = False
        elif self.y < bottom:
            self.y = 2 * bottom - self.y
            self.vy *= -1
