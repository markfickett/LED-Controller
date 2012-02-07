"""
Test generating colors in Python and sending them over Serial to the Arduino.
"""

import sys, os, time, random, math

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

class ColorGenerator:
	def __init__(self, numLeds):
		self.__colorBytes = []
		for i in xrange(numLeds):
			self.__colorBytes.append([0x00,]*3)
		self.__t = 0
		self.__step = math.pi/50.0

	def __makeRandom(self):
		return (	random.randint(0x00, 0xFF),
				random.randint(0x00, 0xFF),
				random.randint(0x00, 0xFF),
		)

	def __nextInGradient(self):
		self.__t += self.__step
		return [
			int(0xFF * (0.5*(1.0 + math.sin(self.__t + x))))
			for x in (math.pi/2.0, 0.0, -math.pi/2.0)
		]

	def update(self):
		self.__colorBytes.pop()
		#self.__colorBytes.insert(0, self.__makeRandom())
		self.__colorBytes.insert(0, self.__nextInGradient())
		
	def getColorBytes(self):
		return self.__colorBytes
		
def PackColorsHalved(colors):
	upper = False
	byteIndex = 0
	colorBytes = [0xFF,]*(3*(len(colors)/2))
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
	#quantize = 0x10
	quantize = 1
	return ''.join(
		[''.join(
			[chr((c/quantize)*quantize) for c in color]
		) for color in colors]
	)

if __name__ == '__main__':
	dt = 0.0
	colorGenerator = ColorGenerator(NUM_LEDS)
	with DataSender.SerialGuard(SERIAL_DEVICE) as arduinoSerial:
		DataSender.WaitForReady(arduinoSerial)
		t = time.time()
		#for i in xrange(TRIALS):
		while True:
			colorGenerator.update()
			colorBytes = PackColors(
				colorGenerator.getColorBytes())
			#colorBytes = PackColorsHalved(
			#	colorGenerator.getColorBytes())
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
