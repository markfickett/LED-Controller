"""
Demonstrate generating colors in Python and using DataSender to transfer them
over Serial to the Arduino. (Optionally simulate entirely in Python.)

Low-level version, using fewer layers of abstraction (and convenience).
"""

# Set how many times to update the pattern (insert one Color) and redisplay
# on the LED strip; use None to continue forever.
TRIALS = 100

# Optionally use a dummy serial device and draw to the screen. (Drawing to the
# screen does not prevent sending to the Arduino.)
DUMMY_SERIAL = False
DRAW = False

# Change this to match your Serial device. The correct value will be in the
# Arduino app's Tools > Serial Device menu. See directions for picking your
# serial device under "Uploading" at http://arduino.cc/en/Guide/Environment .
SERIAL_DEVICE = '/dev/tty.usbmodemfa141'

from Manifest import ledcontroller

from ledcontroller.Manifest import sys, time, random, math, DataSender
from ledcontroller.Manifest import SendingBuffer, Sequences
from ledcontroller.Manifest import TurtleBuffer

if __name__ == '__main__':
	dt = 0.0

	# Use a predefined color sequence; either random colors, or a hue
	# gradient. These are Python generators, yielding Color objects.
	#colorSequence = Sequences.GenerateRandom(limit=TRIALS,
	#	brightInterval=5)
	colorSequence = Sequences.GenerateHueGradient(limit=TRIALS)

	if DUMMY_SERIAL:
		sender = DataSender.DummySender(SERIAL_DEVICE,
			silent=True)
	else:
		sender = DataSender.Sender(SERIAL_DEVICE)
	# Open the serial connection.
	with sender:

		# SendingBuffer has a list of Color objects and encapsulates
		# requisite logic for generating bytes and sending.
		# For simulating, TurtleBuffer subclasses SendingBuffer and
		# draws to the screen using Turtle Graphics as well.
		if DRAW:
			sendingColorBuffer = TurtleBuffer(sender=sender)
		else:
			sendingColorBuffer = SendingBuffer(sender=sender)

		# Put some known colors at the beginning.
		for c in Sequences.GetSentinels():
			sendingColorBuffer.insertAndPop(c)

		for c in colorSequence:
			t = time.time()

			# Insert the next color into one end of the strip (and
			# pop the oldest color from the other end).
			sendingColorBuffer.insertAndPop(c)

			# Send the updated colors to the Arduino.
			sendingColorBuffer.send()
			sys.stdout.write('.')
			sys.stdout.flush()

			sender.readAndPrint()

			dt += time.time() - t

	print 'Elapsed per %d updates: %.2fs' % (TRIALS, dt)
	print 'Updates per second: %.2f' % (TRIALS / dt)

