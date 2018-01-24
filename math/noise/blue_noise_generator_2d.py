##############################################################################
#                                                                            #
#  Written in 2017 by Louis Sugy                                             #
#                                                                            #
#  License : CC-BY                                                           #
#                                                                            #
##############################################################################

# This program generates a blue-noise texture, which can be used for many
# purposes in computer graphics : dithering, texture generation, procedural
# generation, etc.

# HOWTO: just run the program and it will request the needed parameters.
# For the moment it can only generate a PNG image.


# Note : using a sigma value of 1.5 works perfectly, and it is a tip given by
# Ulichney himself, who wrote the paper "the void-and-cluster method for
# dither array generation" (1993) used here.

# For the maximum distance to consider pixels when blurring, you have to make
# a compromise between the quality of your blue noise and the render time.


import png
import random
import math


# The following global array, initialized in main function, will contain the
# gaussian weights for the blur, for each value r**2, with r the distance.
gauss = []

# Maximum distance to consider pixels when blurring (on each axis)
# It is set by user input in main function
blur_dist = 10

# True if you want the program to print logs, False if not.
# Logs can be useful when you try to compute very wide textures.
LOGS = False


def main():
    """Main function : allows the user to choose the dimensions of the
       resulting texture and the filename, computes it and saves it.
       The user also gives a value for sigma - parameter of the Gaussian
       used in void-and-cluster algorithm."""
    global gauss
    global blur_dist

    filename = input("Filename: ")
    width = int(input("Width: "))
    height = int(input("Height: "))
    sigma = float(input("Sigma: "))
    blur_dist = int(input("Blur distance: "))

    # Pre-computation of all Gauss weights
    gauss = [math.exp(- r_sq / (2 * sigma**2))
                for r_sq in range((width//2 + 1)**2 + (height//2 + 1)**2 + 1)]

    noise_map = blue_noise(width, height)
    
    save_image(noise_map, filename)


def blue_noise(width, height):
    """Generates a blue noise matrix of given width and heights and with
       values between 0 and width*height - 1, using the void-and-cluster
       algorithm (cf Ulichney93 paper)."""

    # Initialization of the width*height dither map which will contain the
    # noise values between 0 and width*height - 1, initialized at 0.
    dither_map = [[height*width-1]*width for _ in range(height)]

    # Initialization of the prototype binary pattern (cf Ulichney93).
    # Integers instead of booleans to avoid conversion later in Gaussian.
    pixels_map = [[0]*width for _ in range(height)]

    # Initialiation of the gaussian blur map which will be updated each
    # time a pixel is added or removed.
    blur_map = [[0]*width for _ in range(height)]

    # We begin by adding randomly pixels in pixel map. This is the only
    # non-deterministic step of the process.
    nb_values = (width*height) // 8
    add_random(nb_values, pixels_map, blur_map)
    if LOGS: print("Generated " + str(nb_values) + " random values")


    # We then move pixel from tightest cluster to largest void until the
    # tightest cluster creates largest void.
    cpt = 0
    while True:
        (ci, cj) = tightest_cluster(pixels_map, blur_map)
        pixels_map[ci][cj] = 0
        update_map(blur_map, ci, cj, -1)
        (vi, vj) = largest_void(pixels_map, blur_map)
        if ci == vi and cj == vj:
            pixels_map[ci][cj] = 1
            update_map(blur_map, ci, cj, 1)
            break
        else:
            pixels_map[vi][vj] = 1
            update_map(blur_map, vi, vj, 1)
        cpt += 1
        if LOGS: print("#" + str(cpt) + " swap - "
            + "cluster: (" + str(ci) + ", " + str(cj) + ") - "
            + "void: (" + str(vi) + ", " + str(vj) + ")")


    # Phase I : we give a number to all pixels, by taking the tightest
    # cluster and removing it from a copy of the pixels map, iteratively.
    rank = nb_values - 1
    pm_copy = [pixels_map[i][:] for i in range(height)]
    bm_copy = [blur_map[i][:] for i in range(height)]
    while rank >= 0:
        (i, j) = tightest_cluster(pm_copy, bm_copy)
        dither_map[i][j] = rank
        if LOGS: print("Phase 1: given #" + str(rank)
            + " to (" + str(i) + ", " + str(j) + ")")
        pm_copy[i][j] = 0
        update_map(bm_copy, i, j, -1)
        rank -= 1

    # Phases II and III : we insert pixels in the largest voids, iteratively.
    rank = nb_values
    while rank < width*height:
        (i, j) = largest_void(pixels_map, blur_map)
        dither_map[i][j] = rank
        if LOGS: print("Phase 2: given #" + str(rank)
            + " to (" + str(i) + ", " + str(j) + ")")
        pixels_map[i][j] = 1
        update_map(blur_map, i, j, 1)
        rank += 1

    return dither_map


def add_random(nb_values, pixels_map, blur_map):
    """Adds nb_values random values in the pixels map."""

    width = len(pixels_map[0])
    height = len(pixels_map)

    for _ in range(nb_values):
        i = random.randrange(height)
        j = random.randrange(width)
        while pixels_map[i][j]:
            i = random.randrange(height)
            j = random.randrange(width)
        pixels_map[i][j] = 1
        update_map(blur_map, i, j, 1)



def tightest_cluster(pixels_map, blur_map):
    """Finds the tightest cluster using a Gaussian.
       Blurs the pixels map and finds its maximum."""

    width = len(pixels_map[0])
    height = len(pixels_map)

    vmax = -1 # A value smaller than all possible values
    im = 0
    jm = 0

    for i in range(height):
        for j in range(width):
            if pixels_map[i][j] and blur_map[i][j] > vmax:
                vmax = blur_map[i][j]
                im = i
                jm = j
    return im, jm



def largest_void(pixels_map, blur_map):
    """Finds the largest void using a Gaussian.
       Blurs the pixels map and finds its minimum."""

    width = len(pixels_map[0])
    height = len(pixels_map)

    vmin = width*height+1 # A value greater than all possible values
    im = 0
    jm = 0

    for i in range(height):
        for j in range(width):
            if (not pixels_map[i][j]) and blur_map[i][j] < vmin:
                vmin = blur_map[i][j]
                im = i
                jm = j
    return im, jm


def update_map(blur_map, i, j, value):
    """Gives the new blur map when adding (value=1) or removing (value=-1)
       a pixel at position (i, j)."""

    width = len(blur_map[0])
    height = len(blur_map)

    for ki in range(-min(height, blur_dist) // 2, min(height, blur_dist) // 2):
        for kj in range(-min(width, blur_dist) // 2, min(width, blur_dist) // 2):
            blur_map[(i + ki) % height][(j + kj) % width] += (
                value * gauss[ki**2 + kj**2] )


def save_image(matrix, filename):
    """Saves the given matrix in a greyscale image with the given filename."""

    max_mat = max(matrix[i][j]
                      for i in range(len(matrix))
                          for j in range(len(matrix[0])))

    matrix = [[(65535 * matrix[i][j]) // max_mat
                   for j in range(len(matrix[i]))]
                       for i in range(len(matrix))]

    png.from_array(matrix, "L;16").save(filename)


main()