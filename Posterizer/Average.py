from PIL import Image
from PIL import ImageOps
import os
import random

cd = os.getcwd()


def avg(input_array):
    # Returns the average of a tuple or an array
    return sum(input_array) / len(input_array)


def argmin(input_array):
    # Returns the index of the smallest number
    return input_array.index(min(input_array))


def argmax(input_array):
    # Returns the index of the biggest number
    return input_array.index(max(input_array))


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

    palette_output.append((argmin(histogram_red), argmin(histogram_green), argmin(histogram_blue)))
    palette_output.append((argmax(histogram_red), argmin(histogram_green), argmin(histogram_blue)))
    palette_output.append((argmin(histogram_red), argmax(histogram_green), argmin(histogram_blue)))
    palette_output.append((argmin(histogram_red), argmin(histogram_green), argmax(histogram_blue)))
    palette_output.append((argmax(histogram_red), argmin(histogram_green), argmax(histogram_blue)))
    palette_output.append((argmax(histogram_red), argmax(histogram_green), argmin(histogram_blue)))
    palette_output.append((argmin(histogram_red), argmax(histogram_green), argmax(histogram_blue)))
    palette_output.append((argmax(histogram_red), argmax(histogram_green), argmax(histogram_blue)))

    return palette_output


def randomized(input_image):
    random_palette = []
    input_image_data = input_image.load()
    seeds = [input_image_data[i, 0] for i in range(15)]
    width, height = input_image.size
    for item in seeds:
        random.seed(item)
        random_palette.append(input_image_data[random.randint(0, width), random.randint(0, height)])

    return random_palette


def hued(function, input_image):
    input_image = input_image.convert('HSV')
    width, height = input_image.size
    input_image_splitted = input_image.split()
    hued_image = Image.new('HSV', input_image.size)
    hued_image_data = hued_image.load()
    for 
    function()


if __name__ == '__main__':
    file_name = 'UI3.jpg'
    palette = [(0, 0, 0), (255, 255, 255)]
    current_image = Image.open(cd + '/Inputs/' + file_name)
    current_image_data = current_image.load()
    width, height = current_image.size

    palette.append((0, 0, 0))
    palette.append((255, 255, 255))
    palette.append(image_miner(current_image))
    palette.append(image_maxer(current_image))
    palette.extend(top_colour(current_image))
    palette.extend(hued(randomized, current_image))

    print(sorted(list(set(palette))))

    current_image.show()
