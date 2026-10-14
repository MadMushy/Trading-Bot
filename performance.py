def calculate_return(initial_value, final_value):

    if initial_value >= 0:
        percent_return = float(((final_value - initial_value) / initial_value) * 100)
    else:
        raise ValueError("Inital value must be positive")
    return percent_return
