##############################################################################
#                                                                            #
#  Written in 2017 by Louis Sugy                                             #
#                                                                            #
#  License : CC-BY                                                           #
#                                                                            #
##############################################################################

# This program takes an image, a bit depth per color, and one noise texture
# per color (you can use the same if you prefer). The noise textures must not
# necessarily have the same dimensions as the image, they will be repeated
# periodically.

# A noise texture must not be all black: the program would crash !

# For the moment it is impossible to specify the color palette, that could be
# a improvement of this code.

# /!\ The program only works with png images.


import png


def main():
    """Lets the user choose an image to be dithered, the targeted bit depth
       and the noise textures to use."""

    img_filename = input("Original image filename: ")
    new_filename = input("New image filename: ")
    bit_depth = int(input("Bit depth: "))

    R_filename = input("Noise texture for red: ")
    G_filename = input("Noise texture for green: ")
    B_filename = input("Noise texture for blue: ")

    try:
        img = png.Reader(filename = img_filename).asRGB()
        img_mat = list(img[2])
    except:
    	img = png.Reader(filename = img_filename).asRGBA()
    	img_mat = list(img[2])
    	img_mat = [[line[i] for i in range(len(line)) if i % 4 != 3]
                                for line in img_mat]
    old_depth = img[3]['bitdepth']

    R_noise = list(png.Reader(filename = R_filename).read()[2])
    G_noise = list(png.Reader(filename = G_filename).read()[2])
    B_noise = list(png.Reader(filename = B_filename).read()[2])

    RGB_noise = (R_noise, G_noise, B_noise)

    new_mat = dither(img_mat, RGB_noise, old_depth, bit_depth)
    save_image(new_mat, new_filename, bit_depth)



def dither(matrix, noise, old_depth, bit_depth):
    """Dithers the given matrix -in flat row flat pixel format- with the given
       bit depth and noise -3 channels format-."""

    height = len(matrix)
    width = len(matrix[0]) // 3
    noise_height = [len(noise[c]) for c in range(3)]
    noise_width = [len(noise[c][0]) // 3 for c in range(3)]

    noise_max = [max(noise[c][i][j] for i in range(noise_height[c])
                                    for j in range(noise_width[c])) 
                                    for c in range(3)]
    max_val = 2**bit_depth
    
    step = 2**(old_depth - bit_depth)

    new_matrix = [[[0]*3 for j in range(width)] for i in range(height)]

    for i in range(height):
        for j in range(width):
            for c in range(3):
                new_matrix[i][j][c] = (
                    (matrix[i][3*j + c]
                     + step * noise[c][i%noise_height[c]][j%noise_width[c]] / noise_max[c])
                    // step
                )
                if new_matrix[i][j][c] >= max_val:
                    new_matrix[i][j][c] = max_val - 1

    return new_matrix

    

def save_image(matrix, filename, bit_depth):
    """Saves the given matrix in a RGB image with the given filename."""

    png.from_array(matrix, "RGB;" + str(bit_depth)).save(filename)



main()