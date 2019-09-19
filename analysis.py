# Created by Antony Simonoff. 9/14/2019.

import numpy as np
from graphing import *
from output import *
import user_input as usin
import csv, os, re, ast

# Print inital statements
print("Created by Antony Simonoff. 9/19/2019.")
print("Maintained on https://github.com/as4mo3/opera-analysis-li-lab/")

# Get file locations from user
pre_input, post_input = usin.file_locations()

# Check if colors file exists for custom colors. If not, initalize stardard list of colors.
if os.path.exists('colors.txt') == True:
    with open('colors.txt') as f:
        colors = ast.literal_eval(f.readline())
else:
    colors = ("green", "red", "cyan", "magenta", "yellow", "black", "purple", "blue", "xkcd:azure", "xkcd:chocolate", "xkcd:gold", "xkcd:maroon", "xkcd:plum", "xkcd:silver", "xkcd:teal", "xkcd:chartreuse", "xkcd:cyan", "xkcd:fuchsia", "xkcd:lightblue", "xkcd:magenta", "xkcd:goldenrod", "darkred", "darkkhaki", "steelblue", "deepskyblue", "darkturquoise", "fuchsia", "mediumvioletred", "deeppink", "slateblue", "limegreen", "dimgrey", "darkcyan")

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
    pre_file_top = []
    post_file_top = []

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
pre_matrix = np.empty((8, 12))
post_matrix = np.empty((8, 12))
max_brightness_mat = np.empty((8, 12))
delF_mat = np.empty((8, 12))

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

title = usin.graph_title()

# Find positive control locations and values
print("Are there positive controls? Y/N")
num_pos_ctrls = input().upper()

pos_ctrl_x = []
pos_ctrl_y = []

if num_pos_ctrls == 'Y':
    print("Where is the top left corner of the positive controls?")
    top_left = usin.convert_letters_numbers()
    print("Where is the bottom right corner of the positive controls?")
    bottom_right = usin.convert_letters_numbers()

    for i in max_brightness_mat[top_left[0]:bottom_right[0]+1, top_left[1]:bottom_right[1]+1]:
        for j in i:
            pos_ctrl_x.append(j)

    for i in delF_mat[top_left[0]:bottom_right[0]+1, top_left[1]:bottom_right[1]+1]:
        for j in i:
            pos_ctrl_y.append(j)

    pos_ctrls = (pos_ctrl_x, pos_ctrl_y)

# Check for preliminary vs repeat graphing
print("Is this for preliminary screening (2 libraries)? Y/N")
prelim_screen_yn = input().upper()

if prelim_screen_yn == 'Y':
    print("Do you want to graph one library at a time? Y/N")
    one_library = input().upper()

    # Make standard graph for two libraries
    library_1_name, library_2_name = usin.library_names()
    # Split data into two libraries
    lib_1 = (max_brightness_mat[:6], delF_mat[:6])
    lib_2 = (max_brightness_mat[6:], delF_mat[6:])

    if one_library == "Y":
        # Graph each library, one at a time

        data = (lib_1, )
        labels = (library_1_name, )
        if len(pos_ctrl_x) > 0:
            labels = (library_1_name, "Positive Controls", )
            data = (lib_1, pos_ctrls)
        graph_prelim(data, labels, colors, library_1_name)

        data = (lib_2, )
        labels = (library_2_name)
        if len(pos_ctrl_x) > 0:
            labels = (library_2_name, "Positive Controls", )
            data = (lib_2, pos_ctrls)
        graph_prelim(data, labels, colors, library_2_name)

    else:
        # Graph both libraries on the same graph
        data = (lib_1, lib_2, pos_ctrls)
        labels = (library_1_name, library_2_name)
        if len(pos_ctrl_x) > 0:
            labels = labels + ("Positive Controls", )
            data = data + (pos_ctrls, )
        graph_prelim(data, labels, colors, title)

    # Output data to excel file
    output_to_excel(title, max_brightness_mat, delF_mat, two_lib=True, library_1_name=library_1_name, library_2_name=library_2_name)

else:
    data = ()
    labels = ()

    # Take data from each repeat candidate
    # Assume standard plate arrangement: 3 wells / candidate, horizontal
    # 32 possible repeat candidates total

    print("Do you want to label candidates? If not, they will be labeled sequentially. Y/N")
    labeling = input().upper()

    # Add positive controls first due to long list of candidates.
    if len(pos_ctrl_x) > 1:
        x = np.mean(pos_ctrls[0])
        y = np.mean(pos_ctrls[1])
        x_std = np.std(pos_ctrls[0])
        y_std = np.std(pos_ctrls[1])
        data = data + ((x, y, x_std, y_std, ), )
        labels = labels + ("Positive Control", )

    rpt_candidate_number = 0

    # Iterate over each 3-horizontal well location of each candidate
    # Find average and standard deviation.
    for row in range(0, 8):
        for candidate_index in range(0, 4):
            x = np.mean(max_brightness_mat[row:row+1, candidate_index*3:candidate_index*3+3])
            y = np.mean(delF_mat[row:row+1, candidate_index*3:candidate_index*3+3])
            x_std = np.std(max_brightness_mat[row:row+1, candidate_index*3:candidate_index*3+3])
            y_std = np.std(delF_mat[row:row+1, candidate_index*3:candidate_index*3+3])

            data = data + ((x, y, x_std, y_std), )

            if labeling == 'Y':
                rpt_candidate_number += 1

                # FIXME: off by one error.
                name = usin.repeat_candidate_name(rpt_candidate_number-1)
                if name == '':
                    name = "Rpt Candidate #{}".format(rpt_candidate_number)
                labels = labels + (name, )
            else:
                rpt_candidate_number += 1
                labels = labels + ("Rpt Candidate #{}".format(rpt_candidate_number), )


    output_to_excel(title, max_brightness_mat, delF_mat, rpt=True, data=data, labels=labels)

    graph_rpt(data, labels, colors, title)
