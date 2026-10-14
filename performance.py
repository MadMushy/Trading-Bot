def calculate_return(initial_value, final_value):

    if initial_value >= 0:
        percent_return = float(((final_value - initial_value) / initial_value) * 100)
    else:
        raise ValueError("Inital value must be positive")
    return percent_return

def calculate_max_drawdown(equity_curve):
    
    if equity_curve == []:
        raise ValueError("No data avalible for processing")

    peak = equity_curve[0]
    max_drawdown = 0

    for value in equity_curve:
        if value > peak:
            peak = value
        else:
            calculate_drawdown = float(((peak - value) / peak) * 100)
            if calculate_drawdown > max_drawdown:
                max_drawdown = calculate_drawdown

    return max_drawdown
