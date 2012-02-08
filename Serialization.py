"""
Pack Colors into strings (byte arrays) for transfer to the Arduino.
"""

__all__ = [
	'ToBytes',
]

from Manifest import HALF_PRECISION
from Manifest import math

def ToBytesFull(colors):
	return ''.join(
		[''.join(
			[chr(c) for c in color.getRgbBytes()]
		) for color in colors]
	)

def ToBytesHalf(colors):
	upper = False
	byteIndex = 0
	colorBytes = [0xFF,]*(3*int(math.ceil(len(colors)/2.0)))
	for color in colors:
		for channel in color.getRgbBytes():
			if upper:
				colorBytes[byteIndex] |= channel/0x10 << 4
				upper = False
				byteIndex += 1
			else:
				colorBytes[byteIndex] = channel/0x10
				upper = True
	return ''.join([chr(c) for c in colorBytes])

if HALF_PRECISION:
	ToBytes = ToBytesHalf
else:
	ToBytes = ToBytesFull

