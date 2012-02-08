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
from Manifest import STRIP_LENGTH, HALF_PRECISION
from Manifest import Color

DELAY = 0.013 # approx minimum delay for error-free receipt at 115200 baud
TRIALS = 1000

SERIAL_DEVICE = '/dev/tty.usbmodemfa141'

class ColorGenerator:
	def __init__(self, numLeds):
		self.__colors = []
		for i in xrange(numLeds):
			self.__colors.append(Color())
		#self.__setCym()
		self.__t = 0
		self.__step = math.pi/25

	def __setCym(self):
		self.__colors[0] = Color(rgb=(1, 1, 0))
		self.__colors[2] = Color(rgb=(0, 1, 1))
		self.__colors[1] = Color(rgb=(1, 0, 1))

	def __nextInGradient(self):
		self.__t += self.__step
		return Color(rgb=[
			(0.5*(1.0 + math.sin(self.__t + x)))
			for x in (math.pi/2.0, 0.0, -math.pi/2.0)
		])

	def update(self):
		#self.__colors.insert(0, self.__colorBytes.pop())
		self.__colors.pop()
		#self.__colors.insert(0, Color.CreateRandom())
		self.__colors.insert(0, self.__nextInGradient())
		
	def getColors(self):
		return self.__colors
		
def PackColorsHalved(colors):
	upper = False
	byteIndex = 0
	colorBytes = [0xFF,]*(3*int(math.ceil(len(colors)/2.0)))
	for color in colors:
		#print 'packing (0x%02X, 0x%02X, 0x%02X)' % color.getRgbBytes()
		for channel in color.getRgbBytes():
			if upper:
				#print '\tpack 0x%02X upper' % channel
				colorBytes[byteIndex] |= channel/0x10 << 4
				#print ('\tpacked into 0x%02X'
				#	% colorBytes[byteIndex])
				upper = False
				byteIndex += 1
			else:
				#print '\tpack 0x%02X lower' % channel
				colorBytes[byteIndex] = channel/0x10
				#print ('\tpacked into 0x%02X'
				#	% colorBytes[byteIndex])
				upper = True
	return ''.join([chr(c) for c in colorBytes])

def PackColors(colors):
	return ''.join(
		[''.join(
			[chr(c) for c in color.getRgbBytes()]
		) for color in colors]
	)

if __name__ == '__main__':
	dt = 0.0
	colorGenerator = ColorGenerator(STRIP_LENGTH)
	with DataSender.SerialGuard(SERIAL_DEVICE) as arduinoSerial:
		DataSender.WaitForReady(arduinoSerial)
		t = time.time()
		for i in xrange(TRIALS):
			colorGenerator.update()
			if HALF_PRECISION:
				colorBytes = PackColorsHalved(
					colorGenerator.getColors())
			else:
				colorBytes = PackColors(
					colorGenerator.getColors())
			arduinoSerial.write(
				DataSender.Format(COLORS=colorBytes))
			arduinoSerial.flush() # wait

			s = arduinoSerial.readline()
			while s:
				sys.stdout.write(s)
				s = arduinoSerial.readline()
			sys.stdout.flush()

			time.sleep(DELAY)
		dt = time.time() - t
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
