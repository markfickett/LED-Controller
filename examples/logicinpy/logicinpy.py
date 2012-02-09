"""
Demo generating colors in Python and sending them over Serial to the Arduino.
"""

import os, sys
arduinoLibPath = os.path.abspath(
	os.path.join(
		os.path.dirname(__file__),
		'..', '..'))
sys.path.append(arduinoLibPath)

from Manifest import sys, time, random, math, DataSender
from Manifest import SendingBuffer, Sequences

TRIALS = 1000

SERIAL_DEVICE = '/dev/tty.usbmodemfa141'

if __name__ == '__main__':
	dt = 0.0
	colorSequence = Sequences.GenerateRandom(limit=TRIALS,
		brightInterval=5)
	#colorSequence = Sequences.GenerateHueGradient(limit=TRIALS)

	with DataSender.SerialGuard(SERIAL_DEVICE) as arduinoSerial:
		sendingColorBuffer = SendingBuffer(outputSerial=arduinoSerial)
		for c in Sequences.GetSentinels():
			sendingColorBuffer.pushAndPop(c)

		DataSender.WaitForReady(arduinoSerial)

		for c in colorSequence:
			t = time.time()

			sendingColorBuffer.pushAndPop(c)
			sendingColorBuffer.sendAndWait()

			s = arduinoSerial.readline()
			while s:
				sys.stdout.write(s)
				s = arduinoSerial.readline()
			sys.stdout.flush()

			dt += time.time() - t
	print 'Elapsed per %d: %.2f' % (TRIALS, dt)
	print 'Updates per second: %.2f' % (TRIALS / dt)

