from PIL import Image
from PIL import ImageOps

from multiprocessing import Pool
import multiprocessing
import os
import random
import colorsys
from Posterizer import posterize

cd = os.getcwd()
cpus = multiprocessing.cpu_count()


def avg(input_array):
    # Returns the average of a tuple or an array
    return sum(input_array) / len(input_array)


def argmin(input_array):
    # Returns the index of the smallest number
    return input_array.index(min(input_array))


def argmax(input_array):
    # Returns the index of the biggest number
    return input_array.index(max(input_array))


def float_to_rgb(input_float):
    # Returns a conversion of 1 to 255
    return input_float * 255


def rgb_to_float(input_rgb):
    # Returns a conversion of 255 to 1
    return int(input_rgb / 255)


def func_multiplier(input_function, input_array, before_inputs: str = None, after_inputs: str = None):
    # Basically Pool(#).map(F, A) but without pools and using EVAL().
    try:
        if before_inputs.strip()[0] is not '(':
            before_inputs = '(' + before_inputs
    except Exception:
        before_inputs = '('

    try:
        if before_inputs.strip()[-1] is not ',':
            if before_inputs is not '(':
                before_inputs += ','
    except Exception:
        pass

    try:
        if after_inputs.strip()[0] is not ',':
            if after_inputs is not None:
                after_inputs = ',' + after_inputs
    except Exception:
        pass

    try:
        if after_inputs.strip()[-1] is not ')':
            if after_inputs is not None:
                after_inputs += ')'
    except Exception:
        after_inputs = ')'

    output_array = []
    for item in input_array:
        output_array.append(eval('input_function' + before_inputs + str(item) + after_inputs + '\n'))

    return output_array


def image_maxer(input_image):
    # Returns the brightest pixel in an image
    maximized = (0, 0, 0)
    maximized_average = 0
    input_image_data = input_image.load()
    width, height = input_image.size

    for x in range(width):
        for y in range(height):
            current_pixel = input_image_data[x, y]
            if maximized_average < avg(current_pixel):
                maximized = current_pixel
                maximized_average = avg(maximized)

    return maximized


def image_miner(input_image):
    # Returns the darkest pixel in an image
    minimized = (255, 255, 255)
    minimized_average = 0
    input_image_data = input_image.load()
    width, height = input_image.size

    for x in range(width):
        for y in range(height):
            current_pixel = input_image_data[x, y]
            if minimized_average > avg(current_pixel):
                minimized = current_pixel
                minimized_average = avg(minimized)

    return minimized


def top_colour(input_image):
    # Returns the top most used colours
    palette_output = []
    histogram_red = [0] * 256
    histogram_green = [0] * 256
    histogram_blue = [0] * 256
    input_image_modified = ImageOps.posterize(input_image, 3)
    input_image_data = input_image_modified.load()
    width, height = input_image.size

    for x in range(width):
        for y in range(height):
            current_pixel = input_image_data[x, y]
            histogram_red[current_pixel[0]] += 1
            histogram_green[current_pixel[1]] += 1
            histogram_blue[current_pixel[2]] += 1

    palette_output.append((argmax(histogram_red), argmax(histogram_green), argmax(histogram_blue)))

    return palette_output


fifty_shades_of_grey_number_of_shades = 0


def looping_shades(colour):
    return fiftyshadesofgrey(colour, fifty_shades_of_grey_number_of_shades)


def fiftyshadesofgrey(input_palette, number_of_shades):
    # Gives different shadings to (a) colour(s).

    global fifty_shades_of_grey_number_of_shades
    if type(input_palette) is list:
        if number_of_shades / 2 is not int(number_of_shades / 2):
            number_of_shades += 1

        fifty_shades_of_grey_number_of_shades = number_of_shades
        palette_shades = Pool(cpus).map(looping_shades, input_palette)

        palette_output = []
        for colour in palette_shades:
            palette_output.extend(colour)

        return palette_output

    elif type(input_palette) is tuple:
        input_palette = colorsys.rgb_to_hls(input_palette[0], input_palette[1], input_palette[2])
        palette_output = []

        for lum in range(number_of_shades):
            current_colour = list(input_palette)
            current_colour[1] = (1 / number_of_shades) * lum
            palette_output.append(func_multiplier(float_to_rgb, colorsys.hls_to_rgb(current_colour[0], current_colour[1], current_colour[2])))
            current_colour = palette_output[len(palette_output) - 1]
            palette_output[len(palette_output) - 1] = tuple(func_multiplier(int, current_colour))

        return palette_output


def random_hued(input_image, count):
    # Grabs some random pixels, then neutralizes their colour.
    input_image_data = input_image.load()
    width, height = input_image.size
    palette_output = []
    for c in range(count):
        random.seed(input_image_data[0, c])
        palette_output.append(input_image_data[random.randint(0, width), random.randint(0, height)])

    return palette_output


if __name__ == '__main__':
    file_name = 'Flower1.png'
    palette = [(0, 0, 0), (255, 255, 255)]
    resolution = 512
    resolution = (resolution, resolution)
    current_image = Image.open(cd + '/Inputs/' + file_name)

    print('start')
    palette.append(image_miner(current_image))
    print('Min done.')
    palette.append(image_maxer(current_image))
    print('Max done.')
    palette.extend(top_colour(current_image))
    print('Top done.')
    palette.extend(fiftyshadesofgrey(random_hued(current_image, 40), 6))
    print('Rand done.')

    # print(palette)
    print(sorted(list(set(palette))))

    posterize(cd + '/Inputs/' + file_name, palette, 2, 0, resolution, cd + '/DP/Plus.png', .5, 1, [0, 0, 0]).save(cd + '/Outputs/' + os.path.splitext(file_name)[0] + '.png', 'png')

    current_image.show()
