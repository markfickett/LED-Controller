# Set up paths to include the ledcontroller Python library.
import os, sys
ledControllerLibPath = os.path.abspath(
	os.path.join(os.path.dirname(__file__), '..', '..', 'python'))
sys.path.append(ledControllerLibPath)

def PrintResponsesFromArduino(arduinoSerial):
	"""
	Print any response from the Arduino. (There might be an error message,
	in these examples.)
	"""
	s = arduinoSerial.readline()
	while s:
		sys.stdout.write(s)
		s = arduinoSerial.readline()
	sys.stdout.flush()

import ledcontroller

