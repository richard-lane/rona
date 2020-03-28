"""
Main file for virus simulation thing

"""
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

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
    recovered_particles, = ax.plot([], [], "mo", ms=6)

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


def random_state():
    """
    return a list of (x, y, vx, vy)
    positions are between 0 and 1; velocities are between 0 and 0.2

    """
    state = 2 * np.random.rand(4) - 1
    # Make velocities smaller so its easier to see the animation
    state[2] *= 0.2
    state[3] *= 0.2

    return state


def main():
    """
    Animate a few particles moving

    """
    my_particles = []
    for i in range(100):
        my_particle_state = Particle.particle_state(*random_state())
        my_particles.append(Particle.Particle(my_particle_state))

    particle_box = Particle.Box(my_particles, (-2, -2), 4, 4, 0.0001, 0.0001)

    run_animation(particle_box, 0.1, 2)
    plt.show()


if __name__ == "__main__":
    main()
