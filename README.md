rona.py - a simple disease simulator
======

usage: rona.py [-h] [--width WIDTH] [--height HEIGHT] [--speed SPEED]
               [--radius RADIUS] [--infection_chance INFECTION_CHANCE]
               [--death_chance DEATH_CHANCE] [--recovery_chance RECOVERY_CHANCE]
               [--num NUM]

Run python rona.py --help for more

I think this might need python 3.8 but idk



Features
--------
Particles bounce around collisionlessly + elastically in the box

Particles can be:
 * UNINFECTED - bounce around as normal
 * INFECTED - bounce around; if an uninfected particle passes nearby it may catch the infection.
 * RECOVERED - same as uninfected but cannot catch the disease. Immunity does not wear off
 * DEAD - do not get drawn

