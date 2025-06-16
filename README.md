# FIles:
## OUTPUT PULSE IS SET FOR 50ms DEFAULTLY
### multi_inputs.py:
####IMPORTANT NOTE: this file takes 5 params when calling it  
	&nbsp;- func multi_inputs_test(output, input1, input2, input3, csv_serial_number):\
		 &nbsp;&nbsp;func rising(pigpio_obj, level, tick): \
			 &nbsp;&nbsp;&nbsp; calculates input delay time, and appends it to result list. \
		 &nbsp;&nbsp;- func falling(gpio_obj, level, tick): \
			 &nbsp;&nbsp;&nbsp;calculates duration of input pulse and append it to esult list
	

### parser.py:
	- func parse_input_tracker(str: lines):
		returns list of tuples (start_time, duration) for each input
			


### visual_monitor:
####IMPORTANT NOTE: this file takes 5 params when calling it 
	&nbsp;- func render_waveform(list:input_waves, total_ms=50, width=50) #each ms considered a char \
		&nbsp;&nbsp; this method forms the visual bars \
	&nbsp;- func save_to_csv(int:serial_num, str:tracker_line): \
		&nbsp;&nbsp; this methid creates and modifies csv file that instor test identified by given serial number by the user \
	&nbsp;- class PulseApp(App): \
		 &nbsp;&nbsp; func compose(self): \
			&nbsp;&nbsp;&nbsp; visualize text \  
		 &nbsp;&nbsp; func on_button_pressed(self, event:Button.Pressed): \
			&nbsp;&nbsp;&nbsp; visualize the bars on press \


## Requirments
- pigpiod daemon to manage the GPIO
- pigpio library to use gpio obj
- time library
- sys library
- App, ComposResult from textual.app
- Button, Static from textual.containers
- cvs
- Path from pathlib
- re

## Run
```bash
python3 visual_monitor 21 26 20 19 csv_serial_number
