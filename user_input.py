# All user inputs. Does NOT catch errors.

def file_locations():
    print("What is the path to the top folder of the PRE file (what is the location of folder containing Evaluation1 and indexfile.txt for PRE analysis)?  \nLeave blank if it is in this folder (if left blank, make sure that there is only one folder containing PRE in this directory, and the folder must have PRE in its name).")
    pre_input = input()

    print("What is the path to the top folder of the POST file (what is the location of the folder containing Evaluation1 and indexfile.txt for POST analysis)? \nLeave blank if it is in this folder (if left blank, make sure that there is only one folder containing POST in this directory, and the folder must have POST in its name).")
    post_input = input()

    return pre_input, post_input

def library_names():
    print("What is the name of the first library?")
    library_1_name = input()
    print("What is the name of the second library?")
    library_2_name = input()
    return library_1_name, library_2_name

def repeat_candidate_name(i):
    print("What is the name of candidate #{}?".format(i+1))
    repeat_candidate_name = input()
    return repeat_candidate_name

def num_pos_ctrls():
    print("How many positive controls? Leave blank if none.")
    num_pos_ctrls = input()
    if num_pos_ctrls == '':
        num_pos_ctrls = 0
    return num_pos_ctrls

def convert_letters_numbers():
    user_input = input()
    x = ord(user_input[:1].upper()) - 65
    y = int(user_input[1:]) - 1
    return x, y

def graph_title():
    print("What is the title for the graph?")
    graph_title = input()
    return graph_title
