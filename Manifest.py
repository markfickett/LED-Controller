"""
Centralize imports for the LED Controller library.
"""

SHARED_FILE_NAME = 'Config.h' # relative to this file

import sys, os, time
import random, math

# Adjust path and import DataSender.
DATA_RECEIVER_URL = 'https://github.com/markfickett/DataReceiver'
dataReceiverPath = os.path.abspath(
	os.path.join(os.path.dirname(__file__), '..', 'DataReceiver'))
sys.path.append(dataReceiverPath)
try:
	import DataSender
except ImportError, e:
	raise ImportError('%s: expected in %s, available from %s'
		% (e.message, dataReceiverPath, DATA_RECEIVER_URL))

# Read file shared with Arduino-side and get STRIP_LENGTH, HALF_PRECISION.
STRIP_LENGTH_NAME = 'STRIP_LENGTH'
HALF_PRECISION_NAME = 'HALF_PRECISION'
sharedFilePath = os.path.join(os.path.dirname(__file__), SHARED_FILE_NAME)
with open(sharedFilePath) as sharedFile:
	sharedValues = DataSender.GetSharedValues(sharedFile,
		typeConversionMap={STRIP_LENGTH_NAME: int})
STRIP_LENGTH = sharedValues[STRIP_LENGTH_NAME]
HALF_PRECISION = sharedValues.get(HALF_PRECISION_NAME, False)

