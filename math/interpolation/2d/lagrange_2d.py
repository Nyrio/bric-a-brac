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


NB_VALUES = 1024

def main():
    """Asks the user for the name of a file with 2 lines : one for x values,
       one for y values, separated by spaces, and saves an interpolation in
       the picture which the user selects, with graph and expression of the
       polynomial."""
       
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

    expr_x = lagrange(t, x, N)
    expr_y = lagrange(t, y, N)

    ti = []
    xi = []
    yi = []
    for i in range(NB_VALUES):
        ti.append(i * (N - 1) / (NB_VALUES - 1))
        xi.append(calculate(expr_x, ti[-1]))
        yi.append(calculate(expr_y, ti[-1]))


    plt.plot(xi, yi, "b-")
    plt.plot(x, y, "ro")
    plt.axis([win_xmin, win_xmax, win_ymin, win_ymax])
    plt.xlabel("Lagrange")
    plt.savefig(out_filename)


def lagrange(x, y, N):
    """Computes Lagrange interpolation polynomial with given data y = f(x),
       with x and y two vectors of size N."""

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
    return "".join(
                   str(poly[i])
                   + ("*x" + ("**" + str(i) if i>1 else "") if i>0 else "")
                   + ("+" if i > 0 and poly[i-1] >= 0 else "")
                   for i in reversed(range(N))
              )


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