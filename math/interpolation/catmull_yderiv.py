##############################################################################
#                                                                            #
#  Written in 2017 by Louis Sugy                                             #
#                                                                            #
#  License : CC BY                                                           #
#                                                                            #
##############################################################################

# Catmull-Rom 2D with parameterization.
# 0 = uniform, 0.5 = centripetal, 1 = chordal


import matplotlib.pyplot as plt
import math

# Generate images of the derivatives to control quality of interpolation
DERIV = False

NB_VALUES = 1024
INF = 1048576

def main():
    """Asks the user for the name of a file with 2 lines : one for x values,
       one for y values, separated by spaces, and saves an interpolation in
       the picture which the user selects."""

    in_filename = input("Values filename: ")
    prefix = input("Output prefix: ")
    win_xmin = float(input("Window xmin: "))
    win_xmax = float(input("Window xmax: "))
    win_ymin = float(input("Window ymin: "))
    win_ymax = float(input("Window ymax: "))
    param = 0

    with open(in_filename, 'r') as f:
        x, y = tuple(list(map(float, line.split(" ")))
                         for line in f.readlines())

    N = len(x)
    t = [0]
    for i in range(N-1):
        t.append(t[i] + math.sqrt((x[i+1]-x[i])**2+(y[i+1]-y[i])**2) ** param)

    ti, xi = catmull_rom(t, x)
    ti, yi = catmull_rom(t, y)

    plt.plot(xi, yi, "b-")
    plt.plot(x, y, "ro")
    plt.axis([win_xmin, win_xmax, win_ymin, win_ymax])
    plt.xlabel("Catmull-Rom, parametric")
    plt.savefig(prefix + ".png")

    if not DERIV:
        return

    plt.clf()

    tderiv = []
    xderiv = []
    yderiv = []
    deriv_min = INF
    deriv_max = -INF
    for i in range(NB_VALUES-1):
        tderiv.append((ti[i] + ti[i+1]) / 2)
        xderiv.append((xi[i+1] - xi[i]) / (ti[i+1] - ti[i]))
        yderiv.append((yi[i+1] - yi[i]) / (ti[i+1] - ti[i]))
        deriv_min = min(deriv_min, xderiv[-1], yderiv[-1])
        deriv_max = max(deriv_max, xderiv[-1], yderiv[-1])

    plt.plot(tderiv, xderiv, "g-")
    plt.plot(tderiv, yderiv, "b-")

    tmin = t[0] - 0.1 * (t[N-1] - t[0])
    tmax = t[N-1] + 0.1 * (t[N-1] - t[0])
    vmarge = 0.1 * (deriv_max - deriv_min)
    plt.axis([tmin, tmax, deriv_min - vmarge, deriv_max + vmarge])

    plt.xlabel("x (green) and y (blue) derivatives")
    plt.savefig(prefix + "_derivatives.png")


def catmull_rom(t, x):
    # http://www.cemyuksel.com/research/catmullrom_param/catmullrom.pdf

    N = len(t)
    xi = []
    ti = []
    tmin = t[0]
    tmax = t[N-1]
    for i in range(NB_VALUES):
        ti.append(tmin + i * (tmax - tmin) / (NB_VALUES - 1))
        k = max(ki for ki in range(N-1) if t[ki] <= ti[-1])

        if k == 0:
            xi.append(pyramide(2*x[k]-x[k+1], x[k], x[k+1], x[k+2],
                               2*t[k]-t[k+1], t[k], t[k+1], t[k+2], ti[-1]))
        elif k == N-2:
            xi.append(pyramide(x[k-1], x[k], x[k+1], 2*x[k+1]-x[k],
                               t[k-1], t[k], t[k+1], 2*t[k+1]-t[k], ti[-1]))
        else:
            xi.append(pyramide(x[k-1], x[k], x[k+1], x[k+2],
                               t[k-1], t[k], t[k+1], t[k+2], ti[-1]))
        
    return ti, xi


def pyramide(x0, x1, x2, x3, t0, t1, t2, t3, t):
    a0 = ((t1 - t) * x0 + (t - t0) * x1) / (t1 - t0)
    a1 = ((t2 - t) * x1 + (t - t1) * x2) / (t2 - t1)
    a2 = ((t3 - t) * x2 + (t - t2) * x3) / (t3 - t2)

    b0 = ((t2 - t) * a0 + (t - t0) * a1) / (t2 - t0)
    b1 = ((t3 - t) * a1 + (t - t1) * a2) / (t3 - t1)

    c0 = ((t2 - t) * b0 + (t - t1) * b1) / (t2 - t1)

    return c0


main()