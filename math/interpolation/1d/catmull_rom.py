##############################################################################
#                                                                            #
#  Written in 2017 by Louis Sugy                                             #
#                                                                            #
#  License : CC BY                                                           #
#                                                                            #
##############################################################################

# Uniform Catmull-Rom interpolation
# Non-parametric version : the derivative is not continuous

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

    xmin = x[0]
    xmax = x[N-1]

    xi = []
    yi = []
    for i in range(NB_VALUES):
        xi.append(xmin + i * (xmax - xmin) / (NB_VALUES - 1))
        k = max(ki for ki in range(N-1) if x[ki] <= xi[-1]) # num of the part
        t = (xi[-1] - x[k]) / (x[k+1] - x[k])

        if k == 0:
            yi.append(0.5 * (2*y[k]
                             + (-2*y[k] + 2*y[k+1]) * t
                             + (-y[k] + 2*y[k+1] - y[k+2]) * t**2
                             + (y[k] - 2*y[k+1] + y[k+2]) * t**3
                            )
                     )
        elif k == N-2:
            yi.append(0.5 * (2*y[k]
                             + (-y[k-1] + y[k+1]) * t
                             + (2*y[k-1] - 4*y[k] + 2*y[k+1]) * t**2
                             + (-y[k-1] + 2*y[k] - y[k+1]) * t**3
                            )
                     )
        else:
            yi.append(0.5 * (2*y[k]
                             + (-y[k-1] + y[k+1]) * t
                             + (2*y[k-1] - 5*y[k] + 4*y[k+1] - y[k+2]) * t**2
                             + (-y[k-1] + 3*y[k] - 3*y[k+1] + y[k+2]) * t**3
                            )
                     )


    plt.plot(xi, yi, "b-")
    plt.plot(x, y, "ro")
    plt.axis([win_xmin, win_xmax, win_ymin, win_ymax])
    plt.xlabel("Catmull-Rom")
    plt.savefig(prefix + ".png")


    if not DERIV:
        return

    plt.clf()

    deriv = []
    xderiv = []
    deriv_min = None
    deriv_max = None
    for i in range(NB_VALUES-1):
        if sum(1 if x[j] >= xi[i] and x[j] <= xi[i+1] else 0 for j in range(N)):
            plt.plot(xderiv, deriv, "b-")
            deriv.clear()
            xderiv.clear()
            continue
        deriv.append((yi[i+1] - yi[i]) / (xi[i+1] - xi[i]))
        if (deriv_min is None) or deriv_min > deriv[-1]:
            deriv_min = deriv[-1]
        if (deriv_max is None) or deriv_max < deriv[-1]:
            deriv_max = deriv[-1]
        xderiv.append((xi[i] + xi[i+1]) / 2)

    if deriv:
        plt.plot(xderiv, deriv, "b-")

    marge = 0.1 * (deriv_max - deriv_min)
    plt.axis([win_xmin, win_xmax, deriv_min - marge, deriv_max + marge])
    plt.xlabel("derivative")
    plt.savefig(prefix + "_derivative.png")


main()