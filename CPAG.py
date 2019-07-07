'''
Bash interface for palette.py and posterizer.py
'''
import time
import os
import sys

bench = time.time()

cd = os.getcwd()

params = sys.argv[1:]
capitalized_params = params
params = [str.lower(p) for p in params]

# Usage:
cmd = 0
path = 0
cmd_param = 0


def illegalin(msg: str = None):
    # illegalin is activated when an input is not allowed or an input is corrupted.
    print("Illegal input, type 'CPAG.py help' for help.")
    if msg is not None:
        print(msg)
    raise SystemExit


def combine_text(input_array):
    # Combines all array items into one string
    output_string = ''
    for i in input_array:
        output_string += i
    return output_string


def nextparam(input_index, input_args):
    # Returns the input for the current parameter
    message = input_args[input_index] + ' Requires an input after it. \n Make sure to use a space in between.'
    try:
        output_arg = input_args[input_index + 1]
        if output_arg[0] == '-':
            # if there's another parameter after this parameter:
            illegalin(message)

    except IndexError:
        illegalin(message)

    return output_arg


def input_control(input_name_list, input_param_list, default_output, exterior: str = '', entrance: str = ''):
    # Handles an input like a boss.
    # Exterior is put around the left and right of the text before it's evaluated.
    # If entrance is empty, it's replaced by exterior.
    if entrance == '':
        entrance = exterior

    for name in input_name_list:
        if name in input_param_list:
            # Input was found in the list
            return eval(entrance + nextparam(input_param_list.index(name), input_param_list) + exterior)

    # Input wasn't found in the list
    return default_output


def bool_input_control(input_name_list, input_param_list):
    # Handles bool inputs like a boss
    for name in input_name_list:
        if name in input_param_list:
            return True

    return False


if __name__ == '__main__':
    # Help command
    if len(params) == 0 or params[0] == 'help' or params[0] == 'h':
        # If user has inputted nothing or has inputted 'help' as their main command,
        # This part will be activated.
        dialogue = open(cd + '/USAGE', 'r').read()
        print(dialogue)

    else:

        # Usage:
        cmd = params[0]
        path = capitalized_params[1]
        cmd_param = params[2]
        params = params[3:]

        # Params:
        # Dimension
        dimension_params = ['-d', '--dimensions']
        dimension = input_control(dimension_params, params, 128)

        # Saturation
        saturation_params = ['-s', '--sat']
        saturation = input_control(saturation_params, params, 2)

        # Dithering pattern
        dithering_pattern_params = ['-p', '--pattern']
        dithering_pattern = input_control(dithering_pattern_params, capitalized_params, None, "'")

        # Dithering strength
        dithering_strength_params = ['-ds', '--dither']
        dithering_strength = input_control(dithering_strength_params, params, 0.3)

        # Outline palette
        outline_palette_params = ['-o', '--outpalette']
        outline_palette = input_control(outline_palette_params, params, [0, 0, 0], ')', '(')

        # Alpha outline
        alpha_outline_params = ['-a', '--alphaout']
        alpha_outline = bool_input_control(alpha_outline_params, params)

        # Color outline
        color_outline_params = ['-c', '--colorout']
        color_outline = bool_input_control(color_outline_params, params)

        # Outline value
        outline_value = max(int(alpha_outline), int(color_outline) + 1)

        # Output Dir
        save_dir = 0
        if os.path.exists(capitalized_params[-1]):
            output_path = capitalized_params[-1]
            if os.path.isfile(output_path):
                save_dir = combine_text(os.path.splitext(output_path)[:-2]) + ' Rendered.png'  # make sure it's a png
            else:
                filename = os.path.splitext(capitalized_params[1])[-2] + ' Rendered.png'
                save_dir = output_path + filename

        else:
            save_dir = combine_text(os.path.splitext(capitalized_params[1])[:-1]) + ' Rendered.png'

        # Memory boost
        if True:
            del dimension_params
            del saturation_params
            del dithering_pattern_params
            del dithering_strength_params
            del outline_palette_params
            del alpha_outline_params
            del color_outline_params

        # Path exists?
        if not(os.path.isfile(path)):
            # Wrong path
            illegalin('Non-existent path')

        from Posterizer.Posterizer import posterize
        if cmd == 'e' or cmd == 'euclidean':
            # Detect mode
            if cmd_param == '-d':
                from Posterizer.Palette import palette_generator
                cmd_param = palette_generator(path)
                del palette_generator

            # Palette readable?
            try:
                posterize(path,
                          dimension,
                          0,
                          cmd_param,
                          saturation,
                          dithering_pattern,
                          dithering_strength,
                          outline_value,
                          outline_palette)\
                .save(save_dir, 'PNG')
            except ValueError:
                # Bad palette
                illegalin('Palette is not formatted correctly')
        elif cmd == 'c' or cmd == 'channel':
            # Detect mode
            if cmd_param == '-d':
                cmd_param = [[0, 51, 102, 153, 204, 255],
                             [0, 51, 102, 153, 204, 255],
                             [0, 51, 102, 153, 204, 255]]

            # Palette readable?
            try:
                posterize(path,
                          dimension,
                          1,
                          cmd_param,
                          saturation,
                          dithering_pattern,
                          dithering_strength,
                          outline_value,
                          outline_palette)\
                    .save(save_dir, 'PNG')
            except ValueError:
                # Bad palette
                illegalin('Palette is not formatted correctly')
        elif cmd == 'd' or cmd == 'divide':
            # Detect mode
            if cmd_param == '-d':
                cmd_param = 7

            # Palette readable?
            try:
                posterize(path,
                          dimension,
                          2,
                          cmd_param,
                          saturation,
                          dithering_pattern,
                          dithering_strength,
                          outline_value,
                          outline_palette)\
                    .save(save_dir, 'PNG')
            except ValueError:
                # Bad palette
                illegalin('Palette is not formatted correctly')
        else:
            # Wrong command
            illegalin('Non-existent command')

print(float((time.time() - bench)* 1000))
