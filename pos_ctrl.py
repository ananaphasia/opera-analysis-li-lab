import user_input as usin

def pos_ctrl():
    pos_ctrl_x = pos_ctrl_y = []

    # ask user for inputs
    num_pos_ctrls = usin.num_pos_ctrls()

    # Catch non-int, out of bounds user input exceptions
    try:
        num = int(num_pos_ctrls)
    except ValueError:
        raise ValueError('Number of positive controls must a number')
    else:
        num = int(num_pos_ctrls)

    if num < 0 or num > 96:
        raise ValueError('Number of positive controls must be between 0-96')

    for i in range(num):
        print("In which well is positive control #{}?".format(i+1))
        # change well name to 0-indexed x, y coordinates
        pos_ctrl_x_input, pos_ctrl_y_input = usin.convert_letters_numbers()

        # Throw errors if number > 12 and letter not between A-G
        if pos_ctrl_x_input > 7 or pos_ctrl_x_input < 0:
            raise ValueError('Well Row must be between A-G')
        if pos_ctrl_y_input > 11 or pos_ctrl_y_input < 0:
            raise ValueError('Well Column must be between 1-12')

        pos_ctrl_x.append(pos_ctrl_x_input)
        pos_ctrl_y.append(pos_ctrl_y_input)

    return pos_ctrl_x, pos_ctrl_y
