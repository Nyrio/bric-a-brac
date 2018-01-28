##############################################################################
#                                                                            #
#  Written in 2017 by Louis Sugy                                             #
#                                                                            #
#  License : CC BY                                                           #
#                                                                            #
##############################################################################

# Cubic spline
# != Catmull-Rom : calculated with all the points
# (quite complex and unreadable algorithm)

import matplotlib.pyplot as plt


NB_VALUES = 1024

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

    t = list(range(N))
    spline_x = natural_spline(t, x, N)
    spline_y = natural_spline(t, y, N)

    ti = []
    xi = []
    yi = []
    for i in range(NB_VALUES):
        ti.append(i * (N - 1) / (NB_VALUES - 1))
        k = (i * (N-1)) // NB_VALUES # num of the part

        ax, bx, cx, dx = spline_x[k]
        xi.append(ax+bx*(ti[-1]-t[k])+cx*(ti[-1]-t[k])**2+dx*(ti[-1]-t[k])**3)

        ay, by, cy, dy = spline_y[k]
        yi.append(ay+by*(ti[-1]-t[k])+cy*(ti[-1]-t[k])**2+dy*(ti[-1]-t[k])**3)


    plt.plot(xi, yi, "b-")
    plt.plot(x, y, "ro")
    plt.axis([win_xmin, win_xmax, win_ymin, win_ymax])
    plt.xlabel("cubic spline")
    plt.savefig(out_filename)


def natural_spline(x, y, N):
    """Returns a list of spline parts' parameters (ai, bi, ci, di)
       Si(x) = ai + bi*(x-xi)**1 + ci*(x-xi)**2 + di*(x-xi)**3
    """

    # Adapted from https://en.wikipedia.org/wiki/Spline_(mathematics)

    a = y[:]
    b = [0]*(N-1)
    d = [0]*(N-1)
    h = [x[i+1] - x[i] for i in range(N-1)]
    alpha = [0] + [3 * ((a[i+1]-a[i])/h[i] - (a[i]-a[i-1])/h[i-1])
                      for i in range(1, N-1)]
    c = [0]*N
    L = [1] + [0]*(N-1)
    m = [0]*N
    z = [0]*N

    for i in range(1, N-1):
        L[i] = 2*(x[i+1]-x[i-1]) - h[i-1]*m[i-1]
        m[i] = h[i] / L[i]
        z[i] = (alpha[i] - h[i-1]*z[i-1]) / L[i]

    c[N-1] = 0
    L[N-1] = 1
    z[N-1] = 0

    for i in reversed(range(N-1)):
        c[i] = z[i] - m[i]*c[i+1]
        b[i] = (a[i+1] - a[i]) / h[i] - h[i]*(c[i+1]+2*c[i]) / 3
        d[i] = (c[i+1] - c[i]) / (3*h[i])

    return [(a[i], b[i], c[i], d[i]) for i in range(N-1)]


main()