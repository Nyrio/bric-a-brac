##############################################################################
#                                                                            #
#  Written in 2017 by Louis Sugy                                             #
#                                                                            #
#  License : CC BY                                                           #
#                                                                            #
##############################################################################

# Uniform speed on a Bézier curve

import matplotlib.pyplot as plt
import math

NB_VALUES = 1024

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
    L = float(input("L: "))

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

    tt = 0

    while tt <= N-1:
        i = int(tt)
        t = tt % 1.0

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

        ax = ( 3 * (1-t)**2 * (cx[2*i] - x[i])
             + 6 * t * (1-t) * (cx[2*i+1] - cx[2*i])
             + 3 * t**2 * (x[i+1] - cx[2*i+1]) )

        ay = ( 3 * (1-t)**2 * (cy[2*i] - y[i])
             + 6 * t * (1-t) * (cy[2*i+1] - cy[2*i])
             + 3 * t**2 * (y[i+1] - cy[2*i+1]) )

        v = math.sqrt(ax**2 + ay**2)

        tt += L / v

    plt.plot(xi, yi, "b.")
    plt.plot(x, y, "ro")
    plt.axis([win_xmin, win_xmax, win_ymin, win_ymax])
    plt.xlabel("Bézier, uniform speed")
    plt.savefig(out_filename)


main()