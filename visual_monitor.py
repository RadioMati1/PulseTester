from multi_inputs import multi_inputs_test
from parser import parse_input_tracker
from textual.app import App, ComposeResult
from textual.widgets import Button, Static
from textual.containers import Vertical
import sys
import csv
from pathlib import Path

if len(sys.argv) != 6:
	print("wrong number of arguments")
	exit(1)

OUTPUT = int(sys.argv[1])
INPUT1 = int(sys.argv[2])
INPUT2 = int(sys.argv[3])
INPUT3 = int(sys.argv[4])
serial_num = sys.argv[5]


def render_waveform(data, total_ms = 50, width = 50):
	ms_per_char = total_ms / width
	lines = []
	output_line = "OUTPUT : " + "\u2588" * width
	lines.append(output_line)

	for i, (start, duration) in enumerate(data, 1):
		offset_chars = int(start / ms_per_char)
		width_chars = int(duration / ms_per_char)
		line = f"INPUT{i}:  " + " " * offset_chars +  "\u2588" * width_chars
		lines.append(line)

	return lines

def save_to_csv(serial_num, tracker_line):
	csv_path = Path(__file__).parent / "records.csv"
	with open(csv_path, mode="a", newline="") as f:
		writer = csv.writer(f)
		writer.writerow([serial_num, tracker_line])

class PulseApp(App):
	CSS_PATH = None

	def compose(self):
		yield Button("TEST ON", id = "test_btn")
		yield Static("\nPress TEST ON to begin", id = "instructions", markup = False)
		yield Static("\n\n waiting for waveform", id = "wave_output", markup = False)

	def on_button_pressed(self, event: Button.Pressed):
		if event.button.id == "test_btn":
			raw_list, input_tracker = multi_inputs_test(OUTPUT, INPUT1, INPUT2, INPUT3)
	
			parsed = parse_input_tracker(raw_list)

			waveform_lines = render_waveform(parsed)
			tracker_line = f"input_tracker: {input_tracker}"
			save_to_csv(serial_num, tracker_line)
			result_text = "\n".join(waveform_lines) +  "\n\n" + tracker_line
			self.query_one("#wave_output", Static).update(result_text)

if __name__ ==  "__main__":
	app = PulseApp()
	app.run()
