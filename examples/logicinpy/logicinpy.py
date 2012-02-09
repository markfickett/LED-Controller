"""
Test generating colors in Python and sending them over Serial to the Arduino.
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

"""
Timing/reliability is affected by:
	baud rate: main impact on timing
		28800	14 Hz
		38400	19 Hz
		57600	29 Hz, unreliable
	Python- or Arduino-side color processing, sending:
		no observable impact on 3 100th Hz
	Shortening key from COLORS to C or CL
		only first trial is reliable
		(but not by shortening to COL)
		(but not by lengthening to COLORES)
	calling .flush() after send
		lower speed
		huge increase in reliability
Halving the transferred data:
	STRIP_LENGTH 64 -> 32
		19 Hz -> 36 Hz
	Halving bits (pack into upper and lower 4 bits of each byte):
		19 Hz -> 36 Hz
"""
