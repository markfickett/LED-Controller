"""
Test generating colors in Python and sending them over Serial to the Arduino.
"""

import sys, os, time, random

arduinoLibPath = os.path.abspath(
	os.path.join(
		os.path.dirname(__file__),
		'..', '..', '..',
		'DataReceiver'))
sys.path.append(arduinoLibPath)

import DataSender

NUM_LEDS = 64

DELAY = 0
TRIALS = 100

SERIAL_DEVICE = '/dev/tty.usbmodemfa141'

def ShiftAndAddRandom(colors):
	colors.pop()
	colors.insert(0,
		(	random.randint(0x00, 0xFF),
			random.randint(0x00, 0xFF),
			random.randint(0x00, 0xFF))
	)

def PackColorsHalved(colors):
	colorBytes = [0xFF,]*(3*(len(colors)/2))
	upper = False
	byteIndex = 0
	for color in colors:
		#print 'packing', color
		for channel in color:
			if upper:
				#print '\tpack', channel, 'upper'
				colorBytes[byteIndex] |= channel/0x10 << 4
				#print '\tpacked into', colorBytes[byteIndex]
				upper = False
				byteIndex += 1
			else:
				#print '\tpack', channel, 'lower'
				colorBytes[byteIndex] = channel/0x10
				#print '\tpacked into', colorBytes[byteIndex]
				upper = True
	return ''.join([chr(c) for c in colorBytes])

def PackColors(colors):
	return ''.join(
		[''.join(
			[chr(c) for c in color]
		) for color in colors]
	)

if __name__ == '__main__':
	dt = 0.0
	colors = []
	for i in xrange(NUM_LEDS):
		colors.append([0x00,]*3)
	with DataSender.SerialGuard(SERIAL_DEVICE) as arduinoSerial:
		DataSender.WaitForReady(arduinoSerial)
		t = time.time()
		for i in xrange(TRIALS):
			ShiftAndAddRandom(colors)
			colorBytes = PackColors(colors)
			#colorBytes = PackColorsHalved(colors)
			arduinoSerial.write(
				DataSender.Format(COLORS=colorBytes))
			arduinoSerial.flush() # wait
			#time.sleep(DELAY)
		dt = time.time() - t
		print 'Buffered from Arduino:'
		s = arduinoSerial.readline()
		while s:
			sys.stdout.write(s)
			s = arduinoSerial.readline()
		sys.stdout.flush()
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
	NUM_LEDS 64 -> 32
		19 Hz -> 36 Hz
	Halving bits (pack into upper and lower 4 bits of each byte):
		19 Hz -> 36 Hz
"""
