rona.py - a simple disease simulator
======

usage: rona.py [-h] [--width WIDTH] [--height HEIGHT] [--speed SPEED]
               [--radius RADIUS] [--chance CHANCE] [--num NUM]

Run particle infection simulator

optional arguments:
  * -h, --help       show this help message and exit
  * --width WIDTH    Box width
  * --height HEIGHT  Box height
  * --speed SPEED    Max particle speed
  * --radius RADIUS  Radius below which particles may catch the infection
  * --chance CHANCE  Chance to catch the infection per timestep
  * --num NUM        Number of particles to simulate


I think this might need python 3.8 but idk



Features
--------
Particles bounce around collisionlessly + elastically in the box

Particles can be:
 * UNINFECTED - bounce around as normal
 * INFECTED - bounce around; if an uninfected particle passes nearby it may catch the infection.
 * RECOVERED - same as uninfected but cannot catch the disease. Immunity does not wear off
 * DEAD - do not get drawn

