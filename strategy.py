def calculate_sma(prices, period):
	if len(prices) >= period >= 1:
		segment = prices[-period:]
		total = sum(segment)
		average = total / len(segment)
		return average
	else:
		raise ValueError("Invalid SMA period")





