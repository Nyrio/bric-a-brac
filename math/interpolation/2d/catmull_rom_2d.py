##############################################################################
#                                                                            #
#  Written in 2017 by Louis Sugy                                             #
#                                                                            #
#  License : CC BY                                                           #
#                                                                            #
##############################################################################

# Catmull-Rom 2D interpolation


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
    te = [0]
    for i in range(N-1):
        te.append(te[i] + 1) # the interval between values doesn't matter

    xi = catmull_rom(te, x, N)
    yi = catmull_rom(te, y, N)

    plt.plot(xi, yi, "b-")
    plt.plot(x, y, "ro")
    plt.axis([win_xmin, win_xmax, win_ymin, win_ymax])
    plt.xlabel("Catmull-Rom")
    plt.savefig(out_filename)



def catmull_rom(x, y, N):
    yi = []
    xmin = x[0]
    xmax = x[N-1]
    for i in range(NB_VALUES):
        xi = xmin + i * (xmax - xmin) / (NB_VALUES - 1)
        k = max(ki for ki in range(N-1) if x[ki] <= xi) # num of the part
        t = (xi - x[k]) / (x[k+1]-x[k])

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
    return yi

main()