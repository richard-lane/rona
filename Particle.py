"""
Class for a particle, representing a person or something

"""
import collections
import random
import enum


class State(enum.Enum):
    UNINFECTED = 0
    SICK = 1
    RECOVERED = 2
    DEAD = 3


"""
Encapsulate particle state
"""
particle_state = collections.namedtuple("particle_state", ["x", "y", "vx", "vy"])


class Box:
    """
    Box that the particles live in

    """

    def __init__(
        self, particles, position, width, height, infection_chance, infection_radius
    ):
        """
        :param particles: iterable of particles in the box
        :param position:  low left edge of box; (x, y)
        :param width:     width of box
        :param height:    height of box
        :param infection_chance: chance of a sick particle passing the disease on to a nearby healthy one, per timestep
        :param infection_radius: radius below which the disease may be passed on

        """
        assert len(position) == 2

        # Check our particles all start inside the box
        for particle in particles:
            assert position[0] < particle.x < position[0] + width
            assert position[1] < particle.y < position[1] + height

        self.position = position
        self.width = width
        self.height = height
        self.uninfected_particles = particles
        self.infection_chance = infection_chance
        self.infection_radius = infection_radius

        self.infected_particles = []
        self.recovered_particles = []
        self.dead_particles = []

        self.particle_lists = {
            State.UNINFECTED: self.uninfected_particles,
            State.SICK: self.infected_particles,
            State.RECOVERED: self.recovered_particles,
            State.DEAD: self.dead_particles,
        }

    def spread(self):
        """
        Spread infection from infected particles to nearby uninfected ones

        """
        for infected_particle in self.infected_particles:
            for uninfected_particle in self.uninfected_particles:
                distance2 = (infected_particle.x - uninfected_particle.x) ** 2 + (
                    infected_particle.y - uninfected_particle.y
                ) ** 2
                if distance2 < self.infection_radius ** 2:
                    uninfected_particle.infect(self.infection_chance)

    def step(self, dt):
        """
        Move all particles in the box and process collisions

        There is a bug here as we're iterating over some lists and modifiying them at the same time
        Fix it

        """
        # Iterate over all of our particle types
        for particle_list in self.particle_lists.items():
            # For each particle in this type...
            for particle in particle_list[1]:
                # Record its initial state so we can track if it changes after a timestep
                initial_state = particle.state
                particle.step(
                    dt,
                    self.position[0],
                    self.position[0] + self.width,
                    self.position[1],
                    self.position[1] + self.height,
                )
                # If the state has changed, remove it from its original list and add it to the new one
                if particle.state != initial_state:
                    self.particle_lists[particle.state].append(particle)
                    self.particle_lists[initial_state].remove(particle)
        self.spread()


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
        self.state = State.UNINFECTED

    def infect(self, infection_chance):
        """
        This particle has gone near a sick one and may now get infected

        Infection chance is the change of being infected per tick

        """
        assert 0 < infection_chance < 1
        if random.random() < infection_chance:
            self.state = State.SICK

    def step(self, dt, left, right, bottom, top):
        """
        Move this particle, colliding from walls on the L/R/T/B

        """
        self.x += self.vx * dt
        self.y += self.vy * dt

        # If we have gone past a barrier, reflect the particle in the barrier
        if self.x > right:
            self.x = 2 * right - self.x
            self.vx *= -1
            self.state = State.SICK
        elif self.x < left:
            self.x = 2 * left - self.x
            self.vx *= -1
        if self.y > top:
            self.y = 2 * top - self.y
            self.vy *= -1
        elif self.y < bottom:
            self.y = 2 * bottom - self.y
            self.vy *= -1
