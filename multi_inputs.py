import pigpio 
import time
import sys

if len(sys.argv) != 6:
	print(f"Inaccurate number of parameters. got {len(sys.argv)} instead of 6")
	sys.exit(1)


OUTPUT = int(sys.argv[1])
INPUT1 = int(sys.argv[2])
INPUT2 = int(sys.argv[3])
INPUT3 = int(sys.argv[4])
INPUT4 = int(sys.argv[5])


def multi_inputs_test(OUTPUT, INPUT1, INPUT2, INPUT3):
	INPUT_LIST =  [INPUT1, INPUT2, INPUT3]
	CB = [None] * 6

	pi = pigpio.pi()
	if not pi.connected:
		print("Could not connect to pigpio daemon")
		sys.exit(1)

	output_start_time_us = None
	delay_us, delay_ms = None, None
	start_time = None
	duration_ms, duration_us = None, None
	last_cb_flag = False
	input_tracker = [] # even cells contain pulse start time, odd cells contain pulse duration)
	ms_string = [] # output result for monitoring

	def rising(pigpio, level, tick):
		nonlocal delay_us, delay_ms, start_time
		if output_start_time_us is not None:
			start_time = tick
			delay_us = tick - output_start_time_us
			delay_ms = 1_000 * (delay_us / 1_000_000)
			input_tracker.append(f"{pigpio}: rise after {delay_ms:.4f} ms")
			ms_string.append(f"{delay_ms:.4f}")

	def falling(gpio, level, tick):
		nonlocal duration_ms, duration_us, start_time
		duration_us = tick - start_time # in Microseconds
		duration_ms = 1_000 * (duration_us / 1_000_000) # convert to milliseconds
		input_tracker.append(f"duration: {duration_ms:.4f} ms")
		ms_string.append(f"{duration_ms:.4f}")
		if len(input_tracker) == 6:
			last_cb_flag = True

	# creating callback for rising and falling for each input
	for i in range(0, len(CB), 2):
		CB[i] = pi.callback(INPUT_LIST[i//2], pigpio.RISING_EDGE, rising)
		CB[i+1] = pi.callback(INPUT_LIST[i//2], pigpio.FALLING_EDGE, falling)

	# OUTPUT section
	pi.write(OUTPUT, 1)
	output_start_time_us = pi.get_current_tick()
	time.sleep(0.05)
	pi.write(OUTPUT, 0)

	# checking last falling occured:
	duration_us = pi.get_current_tick() - start_time
	duration_ms = 1_000 * (duration_us / 1_000_000)
	if last_cb_flag == False and len(input_tracker) < 6:
		input_tracker.append(f"duration: {duration_ms:.4f} ms")
		ms_string.append(f"{duration_ms:.4f}")

	print(f"{input_tracker}")
	return ms_string, input_tracker 
	pi.stop()

if __name__ == "__main__":
	res = multi_inputs_test(OUTPUT, INPUT1, INPUT2, INPUT3)
	print(res)
