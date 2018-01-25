##############################################################################
#                                                                            #
#  Written in 2017 by Louis Sugy                                             #
#                                                                            #
#  License : CC BY                                                           #
#                                                                            #
##############################################################################

# Lagrange interpolation of a set of points


# Polynomials are represented by a list of monomials' coefficients ordered
# from low to high degrees.


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

    # Compute Lagrange basis polynomials
    basis = []
    for i in range(N):
        li = [1]
        for j in range(N):
            if i == j:
                continue
            li = prod_poly(li, prod_scal([-x[j], 1], 1/(x[i]-x[j])))
        basis.append(li)

    # Compute the final polynomial
    poly = [0]
    for i in range(N):
        poly = sum_poly(poly, prod_scal(basis[i], y[i]))

    # Python expression of the polynomial
    expr = "".join(
                   str(poly[i])
                   + ("*x" + ("**" + str(i) if i>1 else "") if i>0 else "")
                   + ("+" if i > 0 and poly[i-1] >= 0 else "")
                   for i in reversed(range(N))
               )

    xmin = x[0]
    xmax = x[N-1]

    xi = []
    yi = []
    for i in range(NB_VALUES):
        xi.append(xmin + i * (xmax - xmin) / (NB_VALUES - 1))
        yi.append(calculate(expr, xi[-1]))


    label = "".join(
                    str(round(poly[i], 2))
                    + ("*x" + ("^" + str(i) if i>1 else "") if i>0 else "")
                    + ("+" if i > 0 and poly[i-1] >= 0 else "")
                    for i in reversed(range(N))
                )
    plt.plot(xi, yi, "b-")
    plt.plot(x, y, "ro")
    plt.axis([win_xmin, win_xmax, win_ymin, win_ymax])
    plt.xlabel(label)
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


def prod_poly(p1, p2):
    """Multiplies 2 polynomials."""
    pr = [0] * (len(p1) + len(p2) - 1)
    for i in range(len(p1)):
        for j in range(len(p2)):
            pr[i+j] += p1[i]*p2[j]
    return pr


def prod_scal(p, s):
    """Multiplies a polynomial by a scalar."""
    return [c*s for c in p]


def sum_poly(p1, p2):
    """Adds 2 polynomials."""
    pr = []
    for i in range(min(len(p1), len(p2))):
        pr.append(p1[i] + p2[i])
    for i in range(min(len(p1), len(p2)), max(len(p1), len(p2))):
        pr.append(p1[i] if len(p1) > len(p2) else p2[i])
    return pr


def calculate(expression, x):
    """Calculates the given expression with the given value of x."""

    expr2 = expression
    expr2.replace("x", str(x))

    return eval(expr2)

main()