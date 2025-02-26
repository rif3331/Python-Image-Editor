#################################################################
# FILE : image_editor.py
# WRITER : reef menaged , rifmenaged , 211396528
# EXERCISE : intro2cs ex5 2022-2023
# DESCRIPTION: ex5 intro
#################################################################
# from daal4py import qr

##############################################################################
#                                   Imports                                  #
##############################################################################
from ex5_helper import *
import math
import sys
import random
from typing import Optional

##############################################################################
#                                  Functions                                 #
##############################################################################

NUMBERS_STRING = "123456789"
NO_VALID = "not valid value"
ERR_MSG = "The operation is not done,"
ARG_MSG = "enter number action: "
RED = 0.299
GREEN = 0.587
BLUE = 0.114

def separate_channels(image: ColoredImage) -> List[SingleChannelImage]:
    """The function takes a three-dimensional list with three color channels and separates
     it into a list with single color channels"""
    rows = len(image)
    columns = len(image[0])
    channel = len(image[0][0])
    list_rank3 = []
    for i in range(channel):
        list_rank2 = []
        for j in range(rows):
            list_rank1 = []
            for k in range(columns):
                list_rank1.append(image[j][k][i])
            list_rank2.append(list_rank1)
        list_rank3.append(list_rank2)
    return list_rank3


def combine_channels(channels: List[SingleChannelImage]) -> ColoredImage:
    """The function takes a one-dimensional boilerplate
     list that contains color channels and returns a three-dimensional list with a number of color channels"""
    rows = len(channels)
    columns = len(channels[0])
    channel = len(channels[0][0])
    list_rank3 = []
    for i in range(columns):
        list_rank2 = []
        for j in range(channel):
            list_rank1 = []
            for k in range(rows):
                list_rank1.append(channels[k][i][j])
            list_rank2.append(list_rank1)
        list_rank3.append(list_rank2)
    return list_rank3


def RGB2grayscale(colored_image: ColoredImage) -> SingleChannelImage:
    """The function takes a 3D image and converts it to 2D and basically turns it into black and white"""
    rows = len(colored_image)
    columns = len(colored_image[0])
    channel = len(colored_image[0][0])
    list_rank2 = []
    for i in range(rows):
        list_rank1 = []
        for j in range(columns):
            count = 0
            multiplication = 0
            for k in range(channel):
                if k == 0:
                    multiplication = RED
                elif k == 1:
                    multiplication = GREEN
                else:
                    multiplication = BLUE
                count += float(colored_image[i][j][k]) * multiplication
            list_rank1.append(round(count))
        list_rank2.append(list_rank1)
    return list_rank2


def blur_kernel(size: int) -> Kernel:
    """The function builds the smoothing kernel of the selected size"""
    rows = size
    columns = size
    list_rank2 = []
    for i in range(rows):
        list_rank1 = []
        for j in range(columns):
            list_rank1.append(1/(size**2))
        list_rank2.append(list_rank1)
    return list_rank2


def apply_kernel(image: SingleChannelImage, kernel: Kernel) -> SingleChannelImage:
    """The function blurs black and white image using the smoothing kernel"""
    max_number = 255
    rows = len(image)
    columns = len(image[0])
    middle_kernel = (len(kernel)-1)//2
    list_rank2 = []
    for i in range(rows):
        list_rank1 = []
        for j in range(columns):
            count = 0
            for k in range(-middle_kernel, 1+middle_kernel):
                for t in range(-middle_kernel, 1+middle_kernel):
                    if k + i < 0 or k + i >= rows or t + j < 0 or t + j >= columns:
                        count += float(image[i][j]) * kernel[k+middle_kernel][t+middle_kernel]
                    else:
                        count += float(image[k+i][t+j]) * kernel[k+middle_kernel][t+middle_kernel]
            if count < 0:
                count = 0
            elif count > max_number:
                count = max_number
            list_rank1.append(round(count))
        list_rank2.append(list_rank1)
    return list_rank2


def bilinear_interpolation(image: SingleChannelImage, y: float, x: float) -> int:
    """The function returns the color value of a square in the image in a different size"""
    trin_y = y - int(y)
    trin_x = x - int(x)
    min_index_x = int(x)
    min_index_y = int(y)
    if y - int(y) == 0:
        trin_y = 1
        min_index_y -= 1
    if x - int(x) == 0:
        trin_x = 1
        min_index_x -= 1
    a = image[min_index_y][min_index_x]
    b = image[min_index_y+1][min_index_x]
    c = image[min_index_y][min_index_x+1]
    d = image[min_index_y+1][min_index_x+1]
    return round(a * (1 - trin_x) * (1 - trin_y) + b * trin_y*(1 - trin_x) + c * trin_x * (1 - trin_y) + d * trin_x * trin_y)


def resize(image: SingleChannelImage, new_height: int, new_width: int) -> SingleChannelImage:
    """The function changes black and white image size"""
    old_rows = len(image) - 1
    old_columns = len(image[0]) - 1
    list_rank2 = []
    for i in range(new_height):
        list_rank1 = []
        for j in range(new_width):
            if i == 0 and j == 0:
                list_rank1.append(image[0][0])
            elif i == 0 and j == new_width-1:
                list_rank1.append(image[0][old_columns])
            elif i == new_height-1 and j == 0:
                list_rank1.append(image[old_rows][0])
            elif i == new_height - 1 and j == new_width-1:
                list_rank1.append(image[old_rows][old_columns])
            else:
                relative_x_new = j / (new_width - 1)
                relative_y_new = i / (new_height - 1)
                fit_old_image_height = relative_y_new * old_rows
                fit_old_image_width = relative_x_new * old_columns
                list_rank1.append(bilinear_interpolation(image, fit_old_image_height, fit_old_image_width))
        list_rank2.append(list_rank1)
    return list_rank2


def rotate_90(image: Image, direction: str) -> Image:
    """The function turns the image to the right or left by 90 degrees"""
    rows = len(image)
    columns = len(image[0])
    list_rank3 = []
    if direction == 'R':
        column_iter = list(range(columns))
        row_iter = list(reversed(range(rows)))
    else:
        column_iter = list(reversed(range(columns)))
        row_iter = list(range(rows))

    for i in column_iter:
        list_rank2 = []
        for j in row_iter:
            if type(columns) == list:
                list_rank1 = []
                for k in range(len(image[0][0])):
                    list_rank1.append(image[j][i][k])
                list_rank2.append(list_rank1)
            else:
                list_rank2.append(image[j][i])
        list_rank3.append(list_rank2)
    return list_rank3


def get_edges(image: SingleChannelImage, blur_size: int, block_size: int, c: float) -> SingleChannelImage:
    """The function returns the borders of the image in black and white"""
    black = 0
    white = 255
    rows = len(image)
    columns = len(image[0])
    blurred_image = apply_kernel(image, blur_kernel(blur_size))
    temp_image = apply_kernel(blurred_image, blur_kernel(block_size))
    list_rank2 = []
    for i in range(rows):
        list_rank1 = []
        for j in range(columns):
            threshold = temp_image[i][j] - c
            if threshold > blurred_image[i][j]:
                list_rank1.append(black)
            else:
                list_rank1.append(white)
        list_rank2.append(list_rank1)
    return list_rank2


def quantize(image: SingleChannelImage, N: int) -> SingleChannelImage:
    """The function reduces the number of shades of the black and white image by giving a similar value to similar colors"""
    max_value = 255
    rows = len(image)
    columns = len(image[0])
    list_rank2 = []
    for i in range(rows):
        list_rank1 = []
        for j in range(columns):
            list_rank1.append(round(math.floor(image[i][j]*(N/(max_value+1)))*(max_value/(N-1))))
        list_rank2.append(list_rank1)
    return list_rank2


def quantize_colored_image(image: ColoredImage, N: int) -> ColoredImage:
    """The function reduces the number of shades of the colored image by giving a similar value to similar colors"""
    color_list = separate_channels(image)
    list_rank1 = []
    for i in range(len(color_list)):
        list_rank1.append(quantize(color_list[i], N))
    return combine_channels(list_rank1)


def apply_kernel_color_image(image, kernel):
    """The function blurs the colored image using the smoothing kernel"""
    color_list = separate_channels(image)
    list_rank1 = []
    for i in range(len(color_list)):
        list_rank1.append(apply_kernel(color_list[i], kernel))
    return combine_channels(list_rank1)


def resize_color_image(image, new_height, new_width):
    """The function changes colored image size"""
    color_list = separate_channels(image)
    list_rank1 = []
    for i in range(len(color_list)):
        list_rank1.append(resize(color_list[i], new_height, new_width))
    return combine_channels(list_rank1)


def action1(temp_image):
    """If the input is correct, the function converts the image to black and white"""
    if type(temp_image[0][0]) != list:
        print(ERR_MSG, "it is required to insert a color image")
        return temp_image
    else:
        return RGB2grayscale(temp_image)


def action2(temp_image):
    """If the input is correct, the function blurs the image"""
    kernel_size = input("kernel size: ")
    if kernel_size.isnumeric():
        if int(kernel_size) % 2 == 1 and int(kernel_size) > 0:
            if type(temp_image[0][0]) != list:
                return apply_kernel(temp_image, blur_kernel(int(kernel_size)))
            else:
                return apply_kernel_color_image(temp_image, blur_kernel(int(kernel_size)))
    print(ERR_MSG + " " + NO_VALID)
    return temp_image

def print_2d_table(table):
    for i in range(len(table)):
        row_string = "["
        for j in range(len(table[0])):
            per_cell = len(str(table[i][j]))
            if per_cell == 3:
                row_string += str(table[i][j])
            elif per_cell == 2:
                row_string += " "+str(table[i][j])
            elif per_cell == 1:
                row_string += " "+str(table[i][j])+" "
            row_string += ", "
        print(row_string[0:len(row_string)-2]+"]")

def print_3d_table(table):
    for i in range(len(table)):
        for j in range(len(table[0])):
            end_var = ""
            if j == len(table[0])-1:
                end_var = "\n"
            channels_text = "("
            for k in range(len(table[0][0])):
                text = str(table[i][j][k])
                if len(text) == 3:
                    channels_text += text+":"
                elif len(text) == 2:
                    channels_text += " "+text+":"
                elif len(text) == 1:
                    channels_text += " "+text+" :"

            print(channels_text[0:len(channels_text)-1]+")", end=end_var)

def action3(temp_image):
    """If the input is correct the function changes the image size"""
    # string_new_size = input("height,width: ")
    string_new_size = len(temp_image), len(temp_image[0])
    string_new_size = list(string_new_size)
    while string_new_size[0] > 256 or string_new_size[1] > 256:
        string_new_size[0] *= 0.5
        string_new_size[1] *= 0.5

    string_new_size = math.floor(string_new_size[0]), math.floor(string_new_size[1])
    height = math.floor(string_new_size[0])
    width = math.floor(string_new_size[1])
    if (int(height) % 1 == 0 and int(height) > 1 and
    int(width) % 1 == 0 and int(width) > 1):
        if type(temp_image[0][0]) != list:
            return resize(temp_image, int(height), int(width))
        else:
            return resize_color_image(temp_image, int(height), int(width))
    print(ERR_MSG + " " + NO_VALID)
    return temp_image


def action4(temp_image):
    """If the input is correct, the function turns the image to the right or left"""
    input_string = input("L/R: ")
    if input_string == "L" or input_string == "R":
        return rotate_90(temp_image, input_string)
    print(ERR_MSG + " " + NO_VALID)
    return temp_image


def action5(temp_image):
    """If the input is correct the function returns the black and white outline of the function"""
    # string_new_size = input("blur size,block size,c: ")
    string_new_size = "5,9,5"
    if len(string_new_size) >= 5 and string_new_size.count(",") == 2:
        values = string_new_size.split(",")
        blur_s = values[0]
        block_s = values[1]
        c_to_formula = values[2]
        if blur_s.isnumeric() and block_s.isnumeric() and c_to_formula.isnumeric():
            if (int(blur_s) % 2 == 1 and int(blur_s) >= 1 and
            int(block_s) % 2 == 1 and int(block_s) >= 1 and
            int(c_to_formula) >= 0):
                if type(temp_image[0][0]) == list:
                    temp_image = RGB2grayscale(temp_image)
                return get_edges(temp_image, int(blur_s), int(block_s), int(c_to_formula))
    print(ERR_MSG + " " + NO_VALID)
    return temp_image


def action6(temp_image):
    """If the input is correct the function reduces similar color shades"""
    # input_coloring = input("count coloring: ")
    input_coloring = "5"
    if input_coloring.isnumeric():
        if int(input_coloring) % 1 == 0 and int(input_coloring) > 1:
            if type(temp_image[0][0]) != list:
                return quantize(temp_image, int(input_coloring))
            else:
                return quantize_colored_image(temp_image, int(input_coloring))
    print(ERR_MSG + " " + NO_VALID)
    return temp_image



def action7(temp_image):
    """The function displays the image"""
    show_image(temp_image)
    return temp_image


def actions(temp_image, number):
    """The function routes to the correct action on the image according to the user's choice"""
    if number == "1":
        return action1(temp_image)
    if number == "2":
        return action2(temp_image)
    if number == "3":
        return action3(temp_image)
    if number == "4":
        return action4(temp_image)
    if number == "5":
        return action5(temp_image)
    if number == "6":
        return action6(temp_image)
    if number == "7":
        return action7(temp_image)

def analize_picture(image):
    image = action3(image)
    # show_image(image)
    non_color_image = action1(image)
    # show_image(non_color_image)
    similer_color_image = action6(image)
    # show_image(similer_color_image)
    shadow_image = action5(image)
    show_image(shadow_image)
    print_2d_table(shadow_image)
    # print_3d_table(similer_color_image)
    # show_image(image)



if __name__ == '__main__':
    analize_picture(load_image("diff.png"))
    analize_picture(load_image("cucum.jpg"))
