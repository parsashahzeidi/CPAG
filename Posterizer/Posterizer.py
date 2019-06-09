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

HAVE FUN TRYING TO UNDERSTAND THE CODE!!!

'''
from PIL import Image
from PIL import ImageEnhance
from PIL import ImageChops

import os
import time

cd = os.getcwd()


# TODO: A palette cant have alpha: [(230, 111, 120, 0),(203, 303, 103, 0),(0, 0, 0, 0)].
# TODO: Outline colour needs to remove alpha.
# TODO: Outline colour needs to come in the form of a tuple not a list.



def posterize(file: str, item, saturation: int, interpolation: int, size=(128, 128), dither_map=None, strength=1, outline=2, outline_color=(255, 255, 255)):
    # Opening
    base = Image.open(file)
    base.thumbnail(size)

    alpha = 0
    if base.mode == 'RGBA':  # Alpha Controlling
        base = base.convert(base.mode[:-1])
        alpha = Image.open(file).split()[3].resize(base.size, Image.NEAREST)

    base = Image.open(file).resize(base.size, Image.NEAREST)

    # Dithering
    if type(dither_map) is str:
        dither_t = tile(Image.open(dither_map).convert('RGBA'), base.size, base.mode)  # Tiling the Dither Map if input is a text
        base = dither(base, dither_t, strength)

    elif type(dither_map) is list:
        for d in dither_map:
            dither_t = tile(Image.open(d).convert('RGBA'), base.size, base.mode)  # Tiling the Dither Map if input is a list or tuple
            base = dither(base, dither_t, strength / len(dither_map))

    saturated = ImageEnhance.Color(base)  # Saturating
    del base
    saturated = saturated.enhance(saturation)

    data = saturated.load()
    width, height = saturated.size  # Loading into memory
    try:
        pr = item[0]
        pg = item[1]
        pb = item[2]

    except TypeError:
        pass

    if interpolation == 0:  # Integration 0, Euclidean
        for x in range(width):
            for y in range(height):
                pixel = data[x, y]
                data[x, y] = euclidean(item, pixel)

    elif interpolation == 1:  # Integration 1, Channel based
        for x in range(width):
            for y in range(height):
                pixel = data[x, y]
                data[x, y] = (closest_distance(pr, pixel[0]), closest_distance(pg, pixel[1]), closest_distance(pb, pixel[2]) - 1)

    elif interpolation == 2:  # Integration 2, Automated Range
        range_split = []
        for r in range(item):
            range_split.append(int((256 / item) * r - (256 / item / 2)))  # Making a palette
        range_split.append(255)
        range_split.append(0)

        for x in range(width):
            for y in range(height):
                pixel = data[x, y]
                valr = []
                valg = []
                valb = []
                for r in range(len(range_split)):
                    if pixel[0] <= range_split[r]:  # Red
                        valr.append(range_split[r])

                for r in range(len(range_split)):
                    if range_split[r] >= pixel[1]:  # Green
                        valg.append(range_split[r])

                for r in range(len(range_split)):
                    if range_split[r] >= pixel[2]:  # Blue
                        valb.append(range_split[r])

                data[x, y] = (min(valr), min(valg), min(valb))

    if alpha != 0:
        saturated.putalpha(alpha)  # Alpha Controlling

        if outline != 0:
            outline_image = Image.new('RGBA', saturated.size, (0, 0, 0, 0))  # outlining
            outline_data = outline_image.load()
            alpha_long = Image.new('L', (saturated.size[0] + 1, saturated.size[1] + 1), (0))
            alpha_long_data = alpha_long.load()
            alpha_long.paste(alpha, (0, 0))
            for x in range(width):
                for y in range(height):
                    if alpha_long_data[x, y] < 255:
                        if alpha_long_data[x, invert_check(y - 1)] is 255:
                            outline_data[x, y] = outline_color  # Bottom pixel
                            continue

                        if alpha_long_data[x, y + 1] is 255:
                            outline_data[x, y] = outline_color  # Top pixel
                            continue

                        if alpha_long_data[invert_check(x - 1), y] is 255:
                            outline_data[x, y] = outline_color  # Left pixel
                            continue

                        if alpha_long_data[x + 1, y] is 255:
                            outline_data[x, y] = outline_color  # Right pixel
                            continue

            saturated = Image.alpha_composite(saturated, outline_image)  # Combining outline_data pixels for alpha



    return saturated


def dither(base, dither, strength=1):
    dither = dither.convert(base.mode)
    dither = ImageChops.blend(Image.new(base.mode, base.size, (255, 255, 255)), dither, strength)
    return ImageChops.multiply(dither, base)


def closest_distance(array, number):  # Integration 1, Channel based

    dis = []

    for i in array:
        val = i - number
        if val < 0:
            val = -val

        dis.append(val)
    return array[dis.index(sorted(dis)[0])]


def euclidean(palette, color):  # Integration 0, Euclidean

    dis = []
    index = 0

    for p in palette:
        dis.append((p[0] - color[0]) ** 2 + (p[1] - color[1]) ** 2 + (p[2] - color[2]) ** 2)
        if dis[index] is 0:
            return p

        index += 1

    return tuple(palette[dis.index(sorted(dis)[0])])


def tile(untiled, resolution, newmode, offset=(0, 0)):

    untiled_data = untiled.load()
    tiled = Image.new(newmode, resolution)  # Loading into memory
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

    resolution = 512
    resolution = (resolution, resolution)
    bench = time.time()
    try:
        for i in range(len(filename)):
            # first interpolation :
            posterize(cd + '/Inputs/' + filename[i],
                      [(0, 0, 0), (0, 84, 255), (0, 95, 255), (0, 103, 255), (0, 105, 255), (0, 107, 255), (0, 115, 255), (0, 155, 255), (0, 160, 255), (0, 182, 255), (0, 186, 255), (0, 189, 255), (0, 195, 255), (0, 196, 255), (0, 200, 255), (0, 211, 255), (0, 245, 255), (0, 255, 245), (84, 0, 255), (96, 192, 192), (102, 0, 255), (252, 255, 255), (255, 0, 0), (255, 0, 85), (255, 31, 0), (255, 255, 255)]
                      , 1, 0, resolution, cd + '/DP/Vertical.png', .5, 2).save(cd + '/Outputs/' + str(i) + '. Normal ' + os.path.splitext(filename[i])[0] + '.png', 'png')
            # posterize(cd + '/Inputs/' + filename[i], [[3, 0, 38], [53, 50, 73], [127, 124, 127], [201, 199, 181], [255, 253, 220]], 1, 0, resolution, cd + '/DP/Plus.png', .5, 2).save(cd + '/Outputs/' + str(i) + '. Normal ' + os.path.splitext(filename[i])[0] + '.png', 'png')
            # posterize(image,       [[palette0], [ palette1 ], [   palette2  ],
            #                        [   palette3  ], [  palette4 ]], sat, 0, size)
            print(int((time.time() - bench) * 1000))
            bench = time.time()

            # second interpolation:
            posterize(cd + '/Inputs/' + filename[i], [[3, 53, 127, 201, 255], [0, 50, 124, 199, 253], [38, 73, 127, 181, 220]], 2, 1, resolution, cd + '/DP/Vertical.png', .5, 2).save(cd + '/Outputs/' + str(i) + '. Color ' + os.path.splitext(filename[i])[0] + '.png', 'png')
            # posterize(image,       [[     palette red    ], [    palette green   ],
            #                        [    palette blue   ]], sat, 1, size)
            print(int((time.time() - bench) * 1000))
            bench = time.time()

            posterize(cd + '/Inputs/' + filename[i], 4, 2, 2, resolution, cd + '/DP/Vertical.png', .5, 2).save(cd + '/Outputs/' + str(i) + '. RangeM ' + os.path.splitext(filename[i])[0] + '.png', 'png')
            # posterize(image,                     Range,sat, 2, size)
            print(int((time.time() - bench) * 1000))
            bench = time.time()
    except FileNotFoundError:
        raise FileNotFoundError('Jame missed the easiest part of the code.')
