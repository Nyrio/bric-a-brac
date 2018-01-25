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

# Generate images of the derivatives to control quality of interpolation
DERIV = False

NB_VALUES = 1024

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

    with open(in_filename, 'r') as f:
        x, y = tuple(list(map(float, line.split(" ")))
                         for line in f.readlines())

    # Sort lists according to x
    x, y = zip(*sorted(zip(x, y)))

    N = len(x)

    spline = natural_spline(x, y, N)

    xmin = x[0]
    xmax = x[N-1]

    xi = []
    yi = []
    for i in range(NB_VALUES):
        xi.append(xmin + i * (xmax - xmin) / (NB_VALUES - 1))
        k = max(ki for ki in range(N-1) if x[ki] <= xi[-1]) # num of the part
        a, b, c, d = spline[k]
        yi.append(a+b*(xi[-1]-x[k])+c*(xi[-1]-x[k])**2+d*(xi[-1]-x[k])**3)

    plt.plot(xi, yi, "b-")
    plt.plot(x, y, "ro")
    plt.axis([win_xmin, win_xmax, win_ymin, win_ymax])
    plt.xlabel("cubic spline")
    plt.savefig(prefix + ".png")


    if not DERIV:
        return

    plt.clf()

    deriv = []
    xderiv = []
    deriv_min = None
    deriv_max = None
    for i in range(NB_VALUES-1):
        deriv.append((yi[i+1] - yi[i]) / (xi[i+1] - xi[i]))
        if (deriv_min is None) or deriv_min > deriv[-1]:
            deriv_min = deriv[-1]
        if (deriv_max is None) or deriv_max < deriv[-1]:
            deriv_max = deriv[-1]
        xderiv.append((xi[i] + xi[i+1]) / 2)

    plt.plot(xderiv, deriv, "b-")

    marge = 0.1 * (deriv_max - deriv_min)
    plt.axis([win_xmin, win_xmax, deriv_min - marge, deriv_max + marge])
    plt.xlabel("derivative")
    plt.savefig(prefix + "_derivative.png")


    plt.clf()

    curv = []
    xcurv = []
    curv_min = None
    curv_max = None
    for i in range(NB_VALUES-2):
        curv.append((deriv[i+1] - deriv[i]) / (xi[i+1] - xi[i]))
        if (curv_min is None) or curv_min > curv[-1]:
            curv_min = curv[-1]
        if (curv_max is None) or curv_max < curv[-1]:
            curv_max = curv[-1]
        xcurv.append((xderiv[i] + xderiv[i+1]) / 2)

    plt.plot(xcurv, curv, "b-")

    marge = 0.1 * (curv_max - curv_min)
    plt.axis([win_xmin, win_xmax, curv_min - marge, curv_max + marge])
    plt.xlabel("second derivative")
    plt.savefig(prefix + "_second_derivative_.png")


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