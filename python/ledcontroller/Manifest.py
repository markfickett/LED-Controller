"""
Centralize imports for the LED Controller library.
"""

import sys, os, time
import random, math

SHARED_FILE_NAME = os.path.join('..', '..', 'Config.h') # relative to this file

# Adjust path and import data_sender.
DATA_RECEIVER_URL = 'https://github.com/markfickett/DataReceiver'
dataReceiverPath = os.path.abspath(
	os.path.join(os.path.dirname(__file__),
	'..', '..', '..', 'DataReceiver'))
sys.path.append(dataReceiverPath)
try:
	import data_sender
except ImportError, e:
	raise ImportError('%s: expected in %s, available from %s'
		% (e.message, dataReceiverPath, DATA_RECEIVER_URL))

# Read file shared with Arduino-side and get STRIP_LENGTH, HALF_PRECISION.
STRIP_LENGTH_NAME = 'STRIP_LENGTH'
HALF_PRECISION_NAME = 'HALF_PRECISION'
DATA_RECEIVER_COLOR_KEY_NAME = 'DATA_RECEIVER_COLOR_KEY'
sharedFilePath = os.path.join(os.path.dirname(__file__), SHARED_FILE_NAME)
with open(sharedFilePath) as sharedFile:
	sharedValues = data_sender.GetSharedValues(sharedFile,
		typeConversionMap={STRIP_LENGTH_NAME: int})
STRIP_LENGTH = sharedValues[STRIP_LENGTH_NAME]
HALF_PRECISION = sharedValues.get(HALF_PRECISION_NAME, False)
DATA_RECEIVER_COLOR_KEY = sharedValues[DATA_RECEIVER_COLOR_KEY_NAME].strip('"')

from color import Color
import serialization
from buffer import Buffer
from sending_buffer import SendingBuffer
import sequences
import patterns
from sending_pattern_list import SendingPatternList

try:
	import turtle
	from turtle_buffer import TurtleBuffer
except ImportError, e:
	print ('LED Controller: Turtle Graphics unavailable'
		' for local LED simulation.')

