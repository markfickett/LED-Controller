"""Centralize imports for the LED Controller library."""

import sys, os, time
import random, math

SHARED_FILE_NAME = os.path.join('..', '..', 'Config.h') # relative to this file

# Adjust path and import data_sender.
DATA_RECEIVER_URL = 'https://github.com/markfickett/DataReceiver'
data_receiver_path = os.path.abspath(
  os.path.join(os.path.dirname(__file__),
  '..', '..', '..', 'DataReceiver'))
sys.path.append(data_receiver_path)
try:
  import data_sender
except ImportError, e:
  raise ImportError('%s: expected in %s, available from %s'
    % (e.message, data_receiver_path, DATA_RECEIVER_URL))

# Read file shared with Arduino-side and get STRIP_LENGTH, HALF_PRECISION.
STRIP_LENGTH_NAME = 'STRIP_LENGTH'
HALF_PRECISION_NAME = 'HALF_PRECISION'
DATA_RECEIVER_COLOR_KEY_NAME = 'DATA_RECEIVER_COLOR_KEY'
shared_file_path = os.path.join(os.path.dirname(__file__), SHARED_FILE_NAME)
with open(shared_file_path) as shared_file:
  shared_values = data_sender.GetSharedValues(shared_file,
    type_conversion_map={STRIP_LENGTH_NAME: int})
STRIP_LENGTH = shared_values[STRIP_LENGTH_NAME]
HALF_PRECISION = shared_values.get(HALF_PRECISION_NAME, False)
DATA_RECEIVER_COLOR_KEY = shared_values[DATA_RECEIVER_COLOR_KEY_NAME].strip('"')

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
  print 'LED Controller: Turtle Graphics unavailable for local LED simulation.'

