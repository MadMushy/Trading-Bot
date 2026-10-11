# Calculate average
def calculate_sma(prices, period):
	if len(prices) >= period >= 1:
		segment = prices[-period:]
		total = sum(segment)
		average = total / len(segment)
		return average
	else:
		raise ValueError("Invalid SMA period")

#Generate a buy hold or sell signal based on average
def generate_signal(prices, fast_period=5, slow_period=20):
	if (slow_period > fast_period >= 1) and (len(prices) >= slow_period + 1):
		current_fast = calculate_sma(prices, fast_period)
		current_slow = calculate_sma(prices, slow_period)
		previous_fast = calculate_sma(prices[:-1], fast_period)
		previous_slow = calculate_sma(prices[:-1], slow_period)

		if (previous_fast <= previous_slow) and (current_fast > current_slow):
			return "BUY"
		elif (previous_fast >= previous_slow) and (current_fast < current_slow):
			return "SELL"
		else:
			return "HOLD"
	else:
		raise ValueError("Invalid period. Must be greater then 0 and slow period greater than fast")






