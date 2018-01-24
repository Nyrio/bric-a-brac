##############################################################################
#                                                                            #
#  Written in 2017 by Louis Sugy                                             #
#                                                                            #
#  License : CC-BY                                                           #
#                                                                            #
##############################################################################

# This program generates a 1d blue-noise file, and saves it in a csv file.

# HOWTO: just run the program and it will request the needed parameters.

# /!\ Rows are totally independant from each other ! It is not 2d noise.


# Note : using a sigma value of 1.5 works perfectly, and it is a tip given by
# Ulichney himself, who wrote the paper "the void-and-cluster method for
# dither array generation" (1993) used here.

# For the maximum distance to consider values when blurring, you have to make
# a compromise between the quality of your blue noise and the render time.


import random
import math


# The following global array, initialized in main function, will contain the
# gaussian weights for the blur, for each value dx**2, with dx the distance.
gauss = []

# Maximum distance to consider values when blurring.
# It is set by user input in main function.
blur_dist = 10

# 0: no logs, 1: some logs, 2: all logs
LOGS = 0


def main():
    """Main function : allows the user to choose the number of rows and the
       number of values per rows of blue noise.
       The user also gives a value for sigma - parameter of the Gaussian
       used in void-and-cluster algorithm."""
    global gauss
    global blur_dist

    filename = input("Filename: ")
    nb_rows = int(input("Number of rows: "))
    nb_values = int(input("Values per row: "))
    sigma = float(input("Sigma: "))
    blur_dist = int(input("Blur distance: "))

    # Pre-computation of all Gauss weights
    gauss = [math.exp(- dx_sq / (2 * sigma**2))
                for dx_sq in range((nb_values//2 + 1)**2 + 1)]

    file_content = ""
    for i in range(nb_rows):
        noise_line = blue_noise(nb_values)
        file_content += ";".join(map(str, noise_line)) + "\n"
        if LOGS == 1: print("Computed #" + str(i) + " row")

    with open(filename, 'w') as f:
        f.write(file_content)



def blue_noise(n):
    """Generates a 1d-blue noise array of n values and with values between 0
       and n - 1, using the void-and-cluster algorithm (cf Ulichney93)."""

    # Initialization of the dither array which will contain the noise values
    # between 0 and n - 1, initialized at 0.
    dither = [0]*n

    # Initialization of the prototype binary pattern (cf Ulichney93).
    # Integers instead of booleans to avoid conversion later in Gaussian.
    pbp = [0]*n

    # Initialiation of the gaussian blur array which will be updated each
    # time a value is added or removed.
    blur = [0]*n

    # We begin by adding randomly ones in pbp. This is the only
    # non-deterministic step of the process.
    nb_values = n // 10 + 1
    add_random(nb_values, pbp, blur)
    if LOGS == 2: print("Generated " + str(nb_values) + " random values")


    # We then move 1 from tightest cluster to largest void until the
    # tightest cluster creates largest void, or cpt gets too high
    # (in some cases I'd get infinite loops without it...)
    cpt = 0
    while cpt < n:
        ci = tightest_cluster(pbp, blur)
        pbp[ci] = 0
        update_map(blur, ci, -1)
        vi = largest_void(pbp, blur)
        if ci == vi:
            pbp[ci] = 1
            update_map(blur, ci, 1)
            break
        else:
            pbp[vi] = 1
            update_map(blur, vi, 1)
        cpt += 1
        if LOGS == 2: print("#" + str(cpt) + " swap - "
            + "cluster: " + str(ci) + " - " + "void: " + str(vi))

    # Phase I : we give a number to all pixels, by taking the tightest
    # cluster and removing it from a copy of the pixels map, iteratively.
    rank = nb_values - 1
    pm_copy = pbp[:]
    bm_copy = blur[:]
    while rank >= 0:
        i = tightest_cluster(pm_copy, bm_copy)
        dither[i] = rank
        if LOGS == 2: print("Phase 1: given #" + str(rank) + " to " + str(i))
        pm_copy[i] = 0
        update_map(bm_copy, i, -1)
        rank -= 1

    # Phases II and III : we insert pixels in the largest voids, iteratively.
    rank = nb_values
    while rank < n:
        i = largest_void(pbp, blur)
        dither[i] = rank
        if LOGS == 2: print("Phase 2: given #" + str(rank) + " to " + str(i))
        pbp[i] = 1
        update_map(blur, i, 1)
        rank += 1

    return dither


def add_random(nb_values, pbp, blur):
    """Adds nb_values random values in the pixels map."""

    n = len(pbp)

    for _ in range(nb_values):
        i = random.randrange(n)
        while pbp[i]:
            i = random.randrange(n)
        pbp[i] = 1
        update_map(blur, i, 1)



def tightest_cluster(pbp, blur):
    """Finds the tightest cluster using a Gaussian.
       Blurs the pixels map and finds its maximum."""

    n = len(pbp)

    vmax = -1 # A value smaller than all possible values
    im = 0

    for i in range(n):
        if pbp[i] and blur[i] > vmax:
            vmax = blur[i]
            im = i
    return im



def largest_void(pbp, blur):
    """Finds the largest void using a Gaussian.
       Blurs the pixels map and finds its minimum."""

    n = len(pbp)

    vmin = n+1 # A value greater than all possible values
    im = 0

    for i in range(n):
        if (not pbp[i]) and blur[i] < vmin:
            vmin = blur[i]
            im = i
    return im


def update_map(blur, i, value):
    """Gives the new blur map when adding (value=1) or removing (value=-1)
       a pixel at position (i, j)."""

    n = len(blur)

    for ki in range(-min(n, blur_dist) // 2, min(n, blur_dist) // 2):
        blur[(i + ki) % n] += value * gauss[ki**2]


main()