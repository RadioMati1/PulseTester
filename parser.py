import re

def parse_input_tracker(str_lines):

	result = []

	for i in range(0, len(str_lines), 2):
		start = float(str_lines[i])
		duration = float(str_lines[i+1])
		result.append((start, duration))
	return result

if __name__ == "__main__":
	res = parse_input_tracker(['0.559', '9.81', '26.2790', '10.205', '39.9390', '10.798'])
	print(res) 
