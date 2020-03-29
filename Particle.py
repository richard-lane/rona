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

        # Set one of our particles to be sick

        self.position = position
        self.width = width
        self.height = height
        self.infection_chance = infection_chance
        self.infection_radius = infection_radius

        self.uninfected_particles = particles
        self.infected_particles = [particles[0]]
        del self.uninfected_particles[0]
        self.infected_particles[0].state = State.SICK
        self.recovered_particles = []
        self.dead_particles = []

        self.particle_lists = {
            State.UNINFECTED: self.uninfected_particles,
            State.SICK: self.infected_particles,
            State.RECOVERED: self.recovered_particles,
            State.DEAD: self.dead_particles,
        }

    def step(self, dt):
        """
        Move all particles in the box and process collisions

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
                    self.infected_particles,
                    self.infection_radius,
                    self.infection_chance,
                )
                # If the state has changed, remove it from its original list and add it to the new one
                if particle.state != initial_state:
                    self.particle_lists[particle.state].append(particle)
                    self.particle_lists[initial_state].remove(particle)


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

    def infection_progresses(self):
        """
        The infection progresses and we may either die or get better

        """
        rand_num = random.random()
        if rand_num < 0.0001:
            self.state = State.RECOVERED
        if rand_num > 0.995:
            self.state = State.DEAD

    def step(
        self,
        dt,
        left,
        right,
        bottom,
        top,
        infected_particles,
        infection_radius,
        infection_chance,
    ):
        """
        Move this particle, colliding from walls on the L/R/T/B

        """
        self.x += self.vx * dt
        self.y += self.vy * dt

        # If we have gone past a barrier, reflect the particle in the barrier
        if self.x > right:
            self.x = 2 * right - self.x
            self.vx *= -1
        elif self.x < left:
            self.x = 2 * left - self.x
            self.vx *= -1
        if self.y > top:
            self.y = 2 * top - self.y
            self.vy *= -1
        elif self.y < bottom:
            self.y = 2 * bottom - self.y
            self.vy *= -1

        if self.state == State.UNINFECTED:
            # If there is an infected_particle nearby, we may get infected
            for infected_particle in infected_particles:
                if (infected_particle.x - self.x) ** 2 + (
                    infected_particle.y - self.y
                ) ** 2 > infection_radius ** 2:
                    self.infect(infection_chance)
        elif self.state == State.SICK:
            self.infection_progresses()
