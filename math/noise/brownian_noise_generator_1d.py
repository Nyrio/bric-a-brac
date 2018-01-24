##############################################################################
#                                                                            #
#  Written in 2017 by Louis Sugy                                             #
#                                                                            #
#  License : CC-BY                                                           #
#                                                                            #
##############################################################################

# This program generates a 1d blue-noise file, and saves it in a csv file.
# The values are between 0 and s-1 where s is the size of a row.

# HOWTO: just run the program and it will request the needed parameters.

# /!\ Rows are totally independant from each other ! It is not 2d noise.


import random


def main():
    out_filename = input("Filename: ")
    nb_rows = int(input("Number of rows: "))
    nb_values = int(input("Values per row: "))

    file_content = ""
    for i in range(nb_rows):
	    white = [random.uniform(0, nb_values-1) for i in range(nb_values)]
	    brownian = smoother(white)
	    file_content += ";".join(map(str, brownian)) + "\n"

    with open(out_filename, 'w') as f:
        f.write(file_content)


def smoother(noise):
    output = []
    for i in range(len(noise)):
        output.append(int(0.5 * (noise[i] + noise[(i+1) % len(noise)])))
    return output


main()