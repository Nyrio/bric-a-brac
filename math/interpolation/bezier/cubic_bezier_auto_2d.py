##############################################################################
#                                                                            #
#  Written in 2017 by Louis Sugy                                             #
#                                                                            #
#  License : CC BY                                                           #
#                                                                            #
##############################################################################

# Generates control points and interpolates between the given points.

import matplotlib.pyplot as plt
import math

NB_VALUES = 1024

# Setting DEBUG to True displays the control points
DEBUG = False

# Scale of control lines (relative to distance between path points)
SCALE = 0.3

def main():
    """Asks the user for the name of a file with 2 lines : one for x values,
       one for y values, separated by spaces, and saves an interpolation in
       the picture which the user selects."""

    in_filename = input("Values filename: ")
    out_filename = input("Output filename: ")
    win_xmin = float(input("Window xmin: "))
    win_xmax = float(input("Window xmax: "))
    win_ymin = float(input("Window ymin: "))
    win_ymax = float(input("Window ymax: "))

    with open(in_filename, 'r') as f:
        x, y = tuple(list(map(float, line.split(" ")))
                        for line in f.readlines())

    N = len(x)


    # Compute control points

    cx = []
    cy = []

    # First control point
    cx.append(x[0] + SCALE * (x[1] - x[0]))
    cy.append(y[0] + SCALE * (y[1] - y[0]))

    for i in range(1, N-1):
        tx = (x[i+1] - x[i-1])
        ty = (y[i+1] - y[i-1])
        d = math.sqrt(tx**2 + ty**2)

        dl = math.sqrt((x[i] - x[i-1])**2 + (y[i] - y[i-1])**2)
        dr = math.sqrt((x[i+1] - x[i])**2 + (y[i+1] - y[i])**2)

        cx.append(x[i] - SCALE * tx * dl / d)
        cy.append(y[i] - SCALE * ty * dl / d)

        cx.append(x[i] + SCALE * tx * dr / d)
        cy.append(y[i] + SCALE * ty * dr / d)

    # Last control point
    cx.append(x[N-1] - SCALE * (x[N-1] - x[N-2]))
    cy.append(y[N-1] - SCALE * (y[N-1] - y[N-2]))


    # Compute path

    xi = []
    yi = []

    for i in range(N-1):

        for j in range(NB_VALUES // (N-1)):
            t = j / (NB_VALUES // (N-1))

            xi.append(
                         (1 - t)**3 * x[i]
                         + 3 * (1 - t)**2 * t * cx[2*i]
                         + 3 * (1 - t) * t**2 * cx[2*i+1]
                         + t**3 * x[i+1]
                     )

            yi.append(
                         (1 - t)**3 * y[i]
                         + 3 * (1 - t)**2 * t * cy[2*i]
                         + 3 * (1 - t) * t**2 * cy[2*i+1]
                         + t**3 * y[i+1]
                     )

    if DEBUG: plt.plot(cx, cy, "m.")
    plt.plot(xi, yi, "b-")
    plt.plot(x, y, "ro")
    plt.axis([win_xmin, win_xmax, win_ymin, win_ymax])
    plt.xlabel("cubic bezier auto")
    plt.savefig(out_filename)


main()