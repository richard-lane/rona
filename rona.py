"""
Main file for virus simulation thing

"""
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import argparse
from math import sqrt

import Particle


def run_animation(particle_box, dt, markersize):
    """
    Animate a box of particles
    Does a bunch of stuff then returns a matplotlib animation object . i think

    """

    # set up figure and animation
    fig = plt.figure()
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    ax = fig.add_subplot(
        111, aspect="equal", autoscale_on=False, xlim=(-3.2, 3.2), ylim=(-2.4, 2.4)
    )

    # particles holds the locations of the particles
    uninfected_particles, = ax.plot([], [], "bo", ms=6)
    infected_particles, = ax.plot([], [], "rx", ms=6)
    recovered_particles, = ax.plot([], [], "go", ms=6)

    # rect is the box edge
    rect = plt.Rectangle(
        particle_box.position,
        particle_box.width,
        particle_box.height,
        ec="none",
        lw=2,
        fc="none",
    )
    ax.add_patch(rect)

    def init():
        """ Initialise animation """
        uninfected_particles.set_data([], [])
        infected_particles.set_data([], [])
        recovered_particles.set_data([], [])
        rect.set_edgecolor("none")
        return uninfected_particles, infected_particles, recovered_particles, rect

    def animate(i):
        """perform animation step"""
        particle_box.step(dt)
        uninfected_x = []
        uninfected_y = []
        infected_x = []
        infected_y = []
        recovered_x = []
        recovered_y = []
        # This could be optimised, i cba
        for particle in particle_box.uninfected_particles:
            uninfected_x.append(particle.x)
            uninfected_y.append(particle.y)
        for particle in particle_box.infected_particles:
            infected_x.append(particle.x)
            infected_y.append(particle.y)
        for particle in particle_box.recovered_particles:
            recovered_x.append(particle.x)
            recovered_y.append(particle.y)

        # update pieces of the animation
        rect.set_edgecolor("k")
        uninfected_particles.set_data(uninfected_x, uninfected_y)
        infected_particles.set_data(infected_x, infected_y)
        recovered_particles.set_data(recovered_x, recovered_y)

        uninfected_particles.set_markersize(markersize)
        infected_particles.set_markersize(markersize)
        recovered_particles.set_markersize(markersize)

        return uninfected_particles, infected_particles, recovered_particles, rect

    return animation.FuncAnimation(
        fig, animate, frames=600, interval=10, blit=True, init_func=init
    )


def random_state(x_range, y_range, v):
    """
    Takes in (xmin, xmax), (ymin, ymax), v
    v is the maximum speed along either coord axis
    return a list of (x, y, vx, vy)

    positions are between 0 and 1; velocities are between 0 and 0.2
    Not guaranteed to be a uniform distribution or anything
    """
    x = random.uniform(*x_range)
    y = random.uniform(*y_range)
    vx = v * (2 * random.random() - 1)
    vy = v * (2 * random.random() - 1)

    return x, y, vx, vy


def cli():
    """
    CLI parsing

    Returns an argparse object containing the arguments passed in from the command line
    """
    parser = argparse.ArgumentParser(description="Run particle infection simulator")
    parser.add_argument("--width", default=4, type=float, help="Box width")
    parser.add_argument("--height", default=4, type=float, help="Box height")
    parser.add_argument("--speed", default=0.2, type=float, help="Max particle speed")
    parser.add_argument(
        "--radius",
        default=0.05,
        type=float,
        help="Radius below which particles may catch the infection",
    )
    parser.add_argument(
        "--infection_chance",
        default=0.5,
        type=float,
        help="Chance to catch the infection per timestep",
    )
    parser.add_argument(
        "--death_chance",
        default=0.0001,
        type=float,
        help="Chance to die of the infection per timestep",
    )
    parser.add_argument(
        "--recovery_chance",
        default=0.0001,
        type=float,
        help="Chance to recover from the infection per timestep",
    )
    parser.add_argument(
        "--num", default=100, type=int, help="Number of particles to simulate"
    )

    return parser.parse_args()


def main(args):
    """
    Animate a few particles moving

    """
    box_width = args.width
    box_height = args.height
    particle_speed = (  # Not actually the speed of the particles; max vx, vy of the particles
        args.speed / sqrt(2)
    )
    infection_chance = args.infection_chance
    infection_radius = args.radius

    my_particles = []
    for i in range(args.num):
        my_particle_state = Particle.particle_state(
            *random_state(
                (-box_width / 2, box_width / 2),
                (-box_height / 2, box_height / 2),
                particle_speed,
            )
        )
        my_particles.append(Particle.Particle(my_particle_state))

    particle_box = Particle.Box(
        my_particles,
        (-box_width / 2, -box_height / 2),
        box_width,
        box_height,
        infection_chance,
        infection_radius,
        args.death_chance,
        args.recovery_chance,
    )

    run_animation(particle_box, 0.1, 2)
    plt.show()


if __name__ == "__main__":
    main(cli())
