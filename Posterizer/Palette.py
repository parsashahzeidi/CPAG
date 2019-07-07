'''
Costumizable
 Pixel
  Art
   Generator
     2000
      (Palette Generator)

Made by Parsa Shahzeidi,
@JamieJacker1, @JamieJacker at Twitter,
@JamieJacker at Telegram,
@JamieJacker at Instagram,
and ParsaShahzeidi@Gmail.com at G-mail.

CPAG is licensed under the UNLicense license,
 meaning that ANYTHING is ok, until you pretend that you were the creator of this app.

(Refer to Posterizer.py for the main posterization algorithms.)

HAVE FUN TRYING TO UNDERSTAND THE CODE!!!
'''
from PIL import Image
from PIL import ImageOps

from multiprocessing import Pool
import multiprocessing
import os
import random
import colorsys
from Posterizer.Posterizer import posterize  # Possible false alarm, conflicts between Python and PyCharm.

cd = os.getcwd()
cpus = multiprocessing.cpu_count()


def avg(input_array):
    # Returns the average of a tuple or an array
    return sum(input_array) / len(input_array)


def euclidean(input_array):
    # Returns the Euclidean distance in the array coordinates from O
    return sum([i ** 2 for i in input_array]) ** (1./2.)


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
    except AttributeError:
        before_inputs = '('

    try:
        if before_inputs.strip()[-1] is not ',':
            if before_inputs is not '(':
                before_inputs += ','
    except AttributeError:
        pass

    try:
        if after_inputs.strip()[0] is not ',':
            if after_inputs is not None:
                after_inputs = ',' + after_inputs
    except AttributeError:
        pass

    try:
        if after_inputs.strip()[-1] is not ')':
            if after_inputs is not None:
                after_inputs += ')'
    except AttributeError:
        after_inputs = ')'

    output_array = []
    for item in input_array:
        output_array.append(eval('input_function' + before_inputs + str(item) + after_inputs + '\n'))
    return output_array


def palette_to_image(input_palette, width_per_colour, height):
    # Simple conversion from a palette to an image.
    width = len(input_palette)
    palette_image = Image.new('RGB', (width, 1))
    output_image_data = palette_image.load()
    for i in range(width):
        output_image_data[i, 0] = input_palette[i]

    palette_image = palette_image.resize((width * width_per_colour, height), Image.NEAREST)

    return palette_image


def palette_sorter(input_palette):
    # Sorts a palette with the euclidean algorithm (BubbleSort)
    palette_average = [euclidean(p) for p in input_palette]
    maximum_number = argmax(palette_average)
    palette_sorted = []
    for i in range(len(palette_average) - 1):
        # Appending the current highest item
        palette_sorted.append(input_palette[maximum_number])

        # Removal of the current highest item
        del palette_average[maximum_number]
        del input_palette[maximum_number]

        # Resetting maximum_number
        maximum_number = argmax(palette_average)

    return palette_sorted


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
    # Returns the top most used color
    palette_output = []
    histogram_red = [0] * 256
    histogram_green = [0] * 256
    histogram_blue = [0] * 256
    input_image_modified = ImageOps.posterize(input_image.convert('RGB'), 8)
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


fifty_shades_of_grey_number_of_shades = 0  # Multiprocessing requirement.


def looping_shades(colour):
    return fiftyshadesofgrey(colour, fifty_shades_of_grey_number_of_shades)  # Multiprocessing requirement.


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
    # Grabs some random pixels from an image.
    input_image_data = input_image.load()
    width, height = input_image.size
    palette_output = []
    for c in range(count):
        random.seed(input_image_data[0, c])  # We don't want different outputs per run, do we?
        palette_output.append(input_image_data[random.randint(0, width - 1),
                                               random.randint(0, height - 1)])

    return palette_output


def palette_generator(image_path, depth=5, count=200):
    input_image = Image.open(image_path)
    output_palette = []
    output_palette.append(image_miner(input_image))
    output_palette.append(image_maxer(input_image))
    output_palette.extend(top_colour(input_image))
    output_palette.extend(fiftyshadesofgrey(random_hued(input_image, count), depth))
    return output_palette


if __name__ == '__main__':
    # Main 'launcher'

    # Setting the parameters
    file_name = input('Insert Image Name: ') + '.jpg'

    # Changing the extension to .png if non existent.
    if not(os.path.isfile(cd + '/Inputs/' + file_name)):
        file_name = os.path.splitext(file_name)[0] + '.png'

    file_path = cd + '/Inputs/' + file_name

    saturation_amount = 1
    dither_amount = .5
    dithering_path = cd + '/DP/Plus.png'

    palette = [(0, 0, 0), (255, 255, 255)]
    resolution = 256
    resolution = (resolution, resolution)
    current_image = Image.open(cd + '/Inputs/' + file_name).convert('RGB')

    # Palette detection start.
    print('start.')
    palette.append(image_miner(current_image))
    print('Min done.')
    palette.append(image_maxer(current_image))
    print('Max done.')
    palette.extend(top_colour(current_image))
    print('Top done.')
    palette.extend(fiftyshadesofgrey(random_hued(current_image, 200), 6))
    print('Rand done.')

    # Cleaning the palette
    palette = list(set(palette))
    palette = palette_sorter(palette)
    print(palette)

    # Previewing the palette
    palette_preview = palette_to_image(palette, 5, 100)
    palette_preview.show()
    palette_preview.save(cd + '/Outputs/' + ' Palette.png', 'PNG')

    current_image.show()  # Rendering a view for the original image

    # Posterizing.
    output_image = posterize(file_path, resolution, 0, palette, saturation_amount, dithering_path, dither_amount, 0, (0, 0, 0))
    output_image.save(cd + '/Outputs/' + 'Rendered.png', 'PNG')

    output_image.show()  # Rendering a view for the posterized image
