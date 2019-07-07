'''
Costumizable
 Pixel
  Art
   Generator
     2000

Made by Parsa Shahzeidi,
@JamieJacker1, @JamieJacker at Twitter,
@JamieJacker at Telegram,
@JamieJacker at Instagram,
and ParsaShahzeidi@Gmail.com at G-mail.

CPAG is licensed under the UNLicense license,
 meaning that ANYTHING is ok, until you pretend that you were the creator of this app.

(Refer to Palette.py for palette detection and a bunch of other cool stuff that I programmed.)

HAVE FUN TRYING TO UNDERSTAND THE CODE!!!
'''
from PIL import Image
from PIL import ImageEnhance
from PIL import ImageChops
from PIL import ImageFilter

import os
import time
import cv2
try:
    import cython  # Faster debugging, remove for memory performance if you want.
except ModuleNotFoundError:
    pass

cd = os.getcwd()

#  Notes:
# A palette cant have alpha: [(230, 111, 120, 0),(203, 303, 103, 0),(0, 0, 0, 0)] is false.
# Outline colour cant have alpha: (0, 0, 0, 0) is false.
# Outline colour needs to come in the form of a tuple and not a list: [0, 0, 0] is false.


def posterize(file: str, output_size, interpolation: int, palette, saturation: int, dither_file=None, dither_strength=1., outline_type=2, outline_color=(0, 0, 0)):
    # If the output size is an int, we make it a tuple.
    if type(output_size) == int:
        output_size = [output_size, output_size]

    # Opening
    base = Image.open(file)

    # Calculating size
    x, y = base.size
    if x > output_size[0]:
        y = int(max(y * output_size[0] / x, 1))
        x = int(output_size[0])
    if y > output_size[1]:
        x = int(max(x * output_size[1] / y, 1))
        y = int(output_size[1])
    output_size = x, y

    alpha = 0
    if base.mode == 'RGBA':  # Alpha Controlling
        base = base.convert(base.mode[:-1])
        alpha = Image.open(file).split()[3].resize(output_size, Image.NEAREST)

    base = Image.open(file).resize(output_size, Image.NEAREST)

    # Dithering
    if type(dither_file) is str:
        dither_t = tile(Image.open(dither_file).convert('RGBA'), base.size, base.mode)
        # Tiling the Dither Map if input is a image location
        base = dither(base, dither_t, dither_strength)

    elif type(dither_file) is list:
        for d in dither_file:
            dither_t = tile(Image.open(d).convert('RGBA'), base.size, base.mode)
            # Tiling the Dither Map if input is a list or tuple
            base = dither(base, dither_t, dither_strength / len(dither_file))

    saturated = ImageEnhance.Color(base)  # Saturating
    saturated = saturated.enhance(saturation)

    data = saturated.load()
    width, height = saturated.size  # Loading into memory

    if interpolation == 0:  # Integration 0, Euclidean
        for x in range(width):
            for y in range(height):
                data[x, y] = euclidean(palette, data[x, y])

    elif interpolation == 1:  # Integration 1, Channel based
        pr = palette[0]
        pg = palette[1]
        pb = palette[2]

        for x in range(width):
            for y in range(height):
                pixel = data[x, y]
                data[x, y] = (closest_distance(pr, pixel[0]),
                              closest_distance(pg, pixel[1]),
                              closest_distance(pb, pixel[2]))

    elif interpolation == 2:  # Integration 2, Automated Range
        palette = int(256 / palette)
        additive = int(256 / palette / 2)
        for x in range(width):
            for y in range(height):
                pixel = data[x, y]
                data[x, y] = (int(pixel[0] / palette) * palette + additive,
                              int(pixel[1] / palette) * palette + additive,
                              int(pixel[2] / palette) * palette + additive)

    if outline_type != 0:
        outline_image = Image.new('L', saturated.size, 0)
        if alpha != 0:
            saturated.putalpha(alpha)  # Alpha Controlling

            outline_image = alpha_outlining(alpha)

        if outline_type == 2:
            base = base.filter(ImageFilter.SMOOTH_MORE())
            outline_image = ImageChops.add(canny_outlining(base),
                                           outline_image)

        saturated = ImageChops.composite(Image.new(saturated.mode, saturated.size, outline_color),
                                         saturated,
                                         outline_image)  # Combining the base and a new image with a mask.

    return saturated


def dither(input_image, dither_map, strength=1.):
    dither_map = dither_map.convert(input_image.mode)
    dither_map = ImageChops.blend(Image.new(input_image.mode, input_image.size, (255, 255, 255)), dither_map, strength)
    return ImageChops.multiply(dither_map, input_image)


def canny_outlining(input_image):
    input_image.save(cd + '/tmp.png', 'PNG')

    cannied_image = cv2.imread('tmp.png', 0)

    cannied_image = cv2.Canny(cannied_image, 100, 200)
    cv2.imwrite('tmp.png', cannied_image)

    return Image.open(cd + '/tmp.png').convert('L')


def alpha_outlining(input_alpha):  # Alpha Outlining

    outline_image = Image.new('L', input_alpha.size)
    outline_data = outline_image.load()

    # Offsetting the image by 1 pixel from the top and left to prevent errors
    alpha_long = Image.new('L', (input_alpha.size[0] + 2, input_alpha.size[1] + 2), 0)
    alpha_long_data = alpha_long.load()
    alpha_long.paste(input_alpha, (0, 0))

    width, height = input_alpha.size
    for x in range(width):
        for y in range(height):
            if alpha_long_data[x, y] < 255:
                if alpha_long_data[x + 1, y] is 255:
                    outline_data[x, y] = 255  # Bottom pixel
                    continue

                if alpha_long_data[x + 1, y + 2] is 255:
                    outline_data[x, y] = 255  # Top pixel
                    continue

                if alpha_long_data[x, y + 1] is 255:
                    outline_data[x, y] = 255  # Left pixel
                    continue

                if alpha_long_data[x + 2, y + 1] is 255:
                    outline_data[x, y] = 255  # Right pixel
                    continue

    return outline_image


def closest_distance(array, number):  # Integration 1, Channel based

    dis = []

    for item in array:
        val = item - number
        if val < 0:
            val = -val

        dis.append(val)
    return array[dis.index(sorted(dis)[0])]


def euclidean(palette, color):  # Integration 0, Euclidean
    '''
    palette is referring to your palette
    color is referring to the current pixel
    '''
    dis = []
    index = 0

    for p in palette:
        dis.append((p[0] - color[0]) ** 2
                   + (p[1] - color[1]) ** 2
                   + (p[2] - color[2]) ** 2)

        if dis[index] == 0:
            return p

        index += 1

    return tuple(palette[dis.index(sorted(dis)[0])])


def tile(untiled, output_resolution, newmode, offset=(0, 0)):

    untiled_data = untiled.load()
    tiled = Image.new(newmode, output_resolution)  # Loading into memory
    data = tiled.load()
    untiled_width, untiled_height = untiled.size
    width, height = tiled.size

    for x in range(width):
        for y in range(height):
            data[x, y] = untiled_data[(x + offset[0]) % untiled_width, (y + offset[1]) % untiled_height]
    return tiled.split()[0]


def invert_check(integer):
    if integer < 0:
        integer = -integer  # inverting an inverted value and returning the normal.
    return integer


if __name__ == '__main__':  # Examples:

    filename = ['Tree.png', 'Anime.jpg', 'MumboB.png', 'MumboS.png', 'Flower1.png', 'Flower2.png', 'Flower3.png']
    f = 1
    while f != -1:
        if os.path.isfile(cd + '/Inputs/UI' + str(f) + '.jpg'):
            filename.append('UI' + str(f) + '.jpg')
        elif os.path.isfile(cd + '/Inputs/UI' + str(f) + '.png'):
            filename.append('UI' + str(f) + '.png')
        elif not(os.path.isfile(cd + '/Inputs/UI' + str(f) + '.png') or os.path.isfile(cd + '/Inputs/UI' + str(f) + '.jpg')):
            f = -2
        f = f + 1

    resolution = 256
    resolution = (resolution, resolution)

    palette_euclidean = [(0, 0, 0), (42, 42, 42), (84, 84, 84), (126, 126, 126), (168, 168, 168), (210, 210, 210)]
    palette_channel_based = [[0, 53, 127, 201, 255], [0, 50, 124, 199, 253], [10, 73, 127, 181, 220]]
    palette_range = 5

    saturation_amount = 1
    dither_amount = .5

    dithering_path = cd + '/DP/Plus.png'

    for i in range(len(filename)):
        current_path = cd + '/Inputs/' + filename[i]
        output_extension = '.png'

        bench = time.time()

        # First interpolation :
        posterize(current_path,
                  resolution,
                  0,  # Interpolation
                  palette_euclidean,
                  saturation_amount,
                  dithering_path,
                  dither_amount,
                  2,  # Outline type
                  (0, 0, 0))\
            .save(cd + '/Outputs/Normal' + str(i) + output_extension, output_extension[1:])

        # First Time print
        print(str(int((time.time() - bench) * 1000)) + 'E')
        bench = time.time()

        # Second interpolation:
        posterize(current_path,
                  resolution,
                  1,  # Interpolation
                  palette_channel_based,
                  saturation_amount,
                  dithering_path,
                  dither_amount,
                  2,  # Outline type
                  (0, 0, 0))\
            .save(cd + '/Outputs/Channel' + str(i) + output_extension, output_extension[1:])

        # Second Time print
        print(str(int((time.time() - bench) * 1000)) + 'C')
        bench = time.time()

        # Third interpolation
        posterize(current_path,
                  resolution,
                  2,  # Interpolation
                  palette_range,
                  saturation_amount,
                  dithering_path,
                  dither_amount,
                  2,  # Outline type
                  (0, 0, 0))\
            .save(cd + '/Outputs/Divide' + str(i) + output_extension, output_extension[1:])

        # Third Time print
        print(str(int((time.time() - bench) * 1000)) + 'D')
