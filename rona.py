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
    particles, = ax.plot([], [], "bo", ms=6)

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
        particles.set_data([], [])
        rect.set_edgecolor("none")
        return particles, rect

    def animate(i):
        """perform animation step"""
        particle_box.step(dt)
        x = []
        y = []
        for particle in particle_box.particles:
            x.append(particle.x)
            y.append(particle.y)

        # update pieces of the animation
        rect.set_edgecolor("k")
        particles.set_data(x, y)
        particles.set_markersize(markersize)
        return particles, rect

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
    for i in range(50):
        my_particle_state = Particle.particle_state(*random_state())
        my_particles.append(Particle.Particle(my_particle_state))

    particle_box = Particle.Box(my_particles, (-1, -1), 2, 2)

    run_animation(particle_box, 0.1, 2)
    plt.show()


if __name__ == "__main__":
    main()
