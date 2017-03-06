# Gravity-Simulator

I wrote a gravity simulator in Python to show multi-body motion. It can be run in Python3.X and uses external libraries pygame & numpy.

Each object is given the following attributes: position, mass, velocity.  (X,M,V)

These attributes are updated each interval of time:   dt.

From position & mass we calculate forces.   F = -G m M / r 2

This gives us acceleration which is used to update velocity.  Vf = Vi + a*(dt)

Velocity is then used to update position.   Xf = Xi + V*(dt)

The program uses vectorized force, each object accelerates all others. As with real macroscopic collisions, simulated collisions are inelastic conserving momentum, but not kinetic energy.
