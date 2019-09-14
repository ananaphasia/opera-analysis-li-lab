# Created by Antony Simonoff. 9/14/2019.

import numpy as np
from pos_ctrl import *
from graphing import *
from output import *
import user_input as usin
import csv, os, re

print("Created by Antony Simonoff. 9/14/2019.")
pre_input, post_input = usin.file_locations()

# Find results locations. Assumes only one measurement per folder. Assumes only one subdirectory with PRE/POST each.
if pre_input == '' and post_input == '':
    # Regex in order to match location of pre and post measurements, catch mislabeled errors
    directory = os.listdir()
    r_pre = re.compile(r"pre", flags=re.IGNORECASE)
    r_post = re.compile(r"post", flags=re.IGNORECASE)

    pre_file_top = list(filter(r_pre.search, directory))
    post_file_top = list(filter(r_post.search, directory))

    if pre_file_top == [] or post_file_top == []:
        raise Exception("Make sure PRE and POST files include 'pre' and 'post' (case insensitive) in their name.")
else:
    pre_file_top = post_file_top = []

    pre_file_top.append(pre_input)
    post_file_top.append(post_input)


pre_file_dir = pre_file_top[0] + '/Evaluation1/PlateResults.txt'
post_file_dir = post_file_top[0] + '/Evaluation1/PlateResults.txt'

# import data from pre and post analysis files
with open(pre_file_dir, newline='') as pre:
    pre_read = csv.reader(pre, delimiter='\t')
    pre_list = list(pre_read)

with open(post_file_dir, newline='') as post:
    post_read = csv.reader(post, delimiter='\t')
    post_list = list(post_read)

# delete column titles and descriptions
# leaves only numerical data
del pre_list[:9]
del post_list[:9]

# initalize matrices
pre_matrix = np.zeros((8, 12))
post_matrix = np.zeros((8, 12))
max_brightness_mat = np.zeros((8, 12))
delF_mat = np.zeros((8, 12))

# filter out empty values from data set lists
pre_list[:] = [list(filter(None, entry)) for entry in pre_list]
post_list[:] = [list(filter(None, entry)) for entry in post_list]

# convert strings in data set lists to floats
pre_list[:] = [list(map(float, entry)) for entry in pre_list]
post_list[:] = [list(map(float, entry)) for entry in post_list]

# convert data set lists to matrices, x and y values
for post in post_list:
    row = int(post[0]) - 1
    col = int(post[1]) - 1
    max_brightness_mat[row][col] = post[4]
for (pre, post) in zip(pre_list, post_list):
    x = (post[4] - pre[4])/(pre[4])
    row = int(post[0]) - 1
    col = int(post[1]) - 1
    delF_mat[row][col] = x

# TODO: label specific points

# TODO: output max_brightness_mat, delF_mat, standard devation, etc to excel file
title = usin.graph_title()

# Find positive control locations and values
pos_ctrl_x_input, pos_ctrl_y_input = pos_ctrl()
pos_ctrl_x = []
pos_ctrl_y = []
for pos_ctrl_x_input, pos_ctrl_y_input in zip(pos_ctrl_x_input, pos_ctrl_y_input):
    x = max_brightness_mat[pos_ctrl_x_input][pos_ctrl_y_input]
    y = delF_mat[pos_ctrl_x_input][pos_ctrl_y_input]
    pos_ctrl_x.append(x)
    pos_ctrl_y.append(y)
pos_ctrls = (pos_ctrl_x, pos_ctrl_y)

print("Is this for preliminary screening (2 libraries)? Y/N")
prelim_screen_yn = input().upper()
colors = ("green", "red", "cyan", "magenta", "yellow", "black", "purple", "blue", "xkcd:azure", "xkcd:chocolate", "xkcd:gold", "xkcd:maroon", "xkcd:plum", "xkcd:silver", "xkcd:teal", "xkcd:chartreuse", "xkcd:cyan", "xkcd:fuchsia", "xkcd:lightblue", "xkcd:magenta")
if prelim_screen_yn == 'Y':
    print("Do you want to graph one library at a time? Y/N")
    one_library = input().upper()

    # Make standard graph for two libraries
    library_1_name, library_2_name = usin.library_names()
    # Use all data, graph
    lib_1 = (max_brightness_mat[:6], delF_mat[:6])
    lib_2 = (max_brightness_mat[6:], delF_mat[6:])

    if one_library == "Y":
        data = (lib_1, )
        labels = (library_1_name, )
        if len(pos_ctrl_x) > 0:
            labels = (library_1_name, "Positive Controls",)
            data = (lib_1, pos_ctrls)
        graph_prelim(data, labels, colors, library_1_name)

        data = (lib_2, )
        labels = (library_2_name)
        if len(pos_ctrl_x) > 0:
            labels = (library_2_name, "Positive Controls",)
            data = (lib_2, pos_ctrls)
        graph_prelim(data, labels, colors, library_2_name)
        output_to_excel(title, max_brightness_mat, delF_mat, two_lib=True, library_1_name=library_1_name, library_2_name=library_2_name)
    else:
        data = (lib_1, lib_2, pos_ctrls)
        labels = (library_1_name, library_2_name)
        # Output to graph
        graph_prelim(data, labels, colors, title)
        output_to_excel(title, max_brightness_mat, delF_mat)

else:
    data = ()
    labels = ()
    # Ask how many repeat candidates
    print("How many repeat candidates?")
    num_repeats = int(input())
    for i in range(num_repeats):
        name = usin.repeat_candidate_name(i)
        print("Where is the top left corner of repeat candidate #{}?".format(i+1))
        top_left = usin.convert_letters_numbers()
        print("Where is the bottom right corner of repeat candidate #{}?".format(i+1))
        bottom_right = usin.convert_letters_numbers()

        x = np.mean(max_brightness_mat[top_left[1]:bottom_right[1]+1, top_left[0]:bottom_right[0]+1])
        y = np.mean(delF_mat[top_left[1]:bottom_right[1]+1, top_left[0]:bottom_right[0]+1])
        x_std = np.std(max_brightness_mat[top_left[1]:bottom_right[1]+1, top_left[0]:bottom_right[0]+1])
        y_std = np.std(delF_mat[top_left[1]:bottom_right[1]+1, top_left[0]:bottom_right[0]+1])


        data = data + ((x, y, x_std, y_std), )
        labels = labels + (name, )

    if len(pos_ctrl_x) > 1:
        x = np.mean(pos_ctrls[0])
        y = np.mean(pos_ctrls[1])
        x_std = np.std(pos_ctrls[0])
        y_std = np.std(pos_ctrls[1])
        data = data + ((x, y, x_std, y_std, ), )
        labels = labels + ("Positive Control",)

    output_to_excel(title, max_brightness_mat, delF_mat, rpt=True, data=data, labels=labels)

    graph_rpt(data, labels, colors, title)
