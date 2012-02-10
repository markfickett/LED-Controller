"""
Demonstrate generating colors in Python and using DataSender to transfer them
over Serial to the Arduino.
"""

# Set up paths to include the ledcontroller Python library.
import os, sys
ledControllerLibPath = os.path.abspath(
	os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(ledControllerLibPath)

from Manifest import sys, time, random, math, DataSender
from Manifest import SendingBuffer, Sequences

# Set how many times to update the pattern (insert one Color) and redisplay
# on the LED strip; use None to continue forever.
TRIALS = 1000

# Change this to match your Serial device. The correct value will be in the
# Arduino app's Tools > Serial Device menu. See directions for picking your
# serial device under "Uploading" at http://arduino.cc/en/Guide/Environment .
SERIAL_DEVICE = '/dev/tty.usbmodemfa141'

if __name__ == '__main__':
	dt = 0.0

	# Use a predevined color sequence; either random colors, or a hue
	# gradient. These are Python generators, yielding Color objects.
	#colorSequence = Sequences.GenerateRandom(limit=TRIALS,
	#	brightInterval=5)
	colorSequence = Sequences.GenerateHueGradient(limit=TRIALS)

	# Open the serial connection.
	with DataSender.SerialGuard(SERIAL_DEVICE) as arduinoSerial:

		# SendingBuffer has a list of Color objects and encapsulates
		# requisite logic for generating bytes and sending.
		sendingColorBuffer = SendingBuffer(outputSerial=arduinoSerial)

		# Put some known colors at the beginning.
		for c in Sequences.GetSentinels():
			sendingColorBuffer.insertAndPop(c)

		# Wait until the Arduino has finished setup() before sending.
		DataSender.WaitForReady(arduinoSerial)

		for c in colorSequence:
			t = time.time()

			# Insert the next color into one end of the strip (and
			# pop the oldest color from the other end).
			sendingColorBuffer.insertAndPop(c)

			# Send the updated colors to the Arduino and wait for
			# it to finish processing (to avoid dropped data by
			# sending too fast).
			sendingColorBuffer.sendAndWait()

			# Print any response from the Arduino. (There might be
			# an error message, in this example.)
			s = arduinoSerial.readline()
			while s:
				sys.stdout.write(s)
				s = arduinoSerial.readline()
			sys.stdout.flush()

			dt += time.time() - t

	print 'Elapsed per %d: %.2f' % (TRIALS, dt)
	print 'Updates per second: %.2f' % (TRIALS / dt)

