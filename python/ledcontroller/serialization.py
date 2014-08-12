"""
Pack Colors into strings (byte arrays) for transfer to the Arduino.
"""

__all__ = [
  'ToBytes',
]

from Manifest import HALF_PRECISION
from Manifest import math

def ToBytes(colors):
  """
  Convert the given list of Colors to a string (byte array), suitable
  for sending to the Arduino. This uses Color.GetRgbBytes, and then packs
  those bytes into a string either directly or (if HALF_PRECISION is True)
  alternately into the upper and lower 4 bits of each byte.

  @return a string with color values packed into it
  """
  if HALF_PRECISION:
    return ToBytesHalf(colors)
  else:
    return ToBytesFull(colors)


def ToBytesFull(colors):
  return ''.join(
    [''.join(
      [chr(c) for c in color.GetRgbBytes()]
    ) for color in colors]
  )

def ToBytesHalf(colors):
  upper = False
  byte_index = 0
  color_bytes = [0xFF,]*(3*int(math.ceil(len(colors)/2.0)))
  for color in colors:
    for channel in color.GetRgbBytes():
      if upper:
        color_bytes[byte_index] |= channel/0x10 << 4
        upper = False
        byte_index += 1
      else:
        color_bytes[byte_index] = channel/0x10
        upper = True
  return ''.join([chr(c) for c in color_bytes])

