rona.py - a simple disease simulator
======

Run with python rona.py

I think this might need python 3.8 but idk



Features
--------
Particles bounce around collisionlessly + elastically in the box

Particles can be:
 * UNINFECTED - bounce around as normal
 * INFECTED - bounce around; if an uninfected particle passes nearby it may catch the infection.
 * RECOVERED - same as uninfected but cannot catch the disease. Immunity does not wear off
 * DEAD - do not get drawn

