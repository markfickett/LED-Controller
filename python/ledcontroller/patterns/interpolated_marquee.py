from ledcontroller.Manifest import Buffer, time, STRIP_LENGTH, Color, patterns
from Manifest import Pattern

__all__ = [
  'InterpolatedMarquee',
]

class InterpolatedMarquee(Pattern, Buffer):
  """
  Manage timed scrolling of a color sequence, and simulate sub-integer
  locations for that movement (sub-pixel smoothing, in effect).

  Smoothness of animation is dependant on frequency of calls to Apply.

  TODO(markfickett) Apparent smoothness also depends on linearity of
  response of the LEDs; that is, how smoothly the perceived luminance
  varies with numeric color value. Nonlinear interpolation may improve
  perceived animation.
  """
  def __init__(self, color_sequence, speed=1.0):
    """
    Args:
      color_sequence an iterable of Color objects, to be scrolled. When
          the color_sequence runs out, the marquee will stop animating.
       speed the number of positions (LEDs) to advance in one second.
          For example, with a speed of 5, the first color from
          color_sequence will move (smoothly) from the start of the LED
          strip to the 5th LED.
    """
    if speed <= 0.0:
      raise ValueError('Illegal speed %s must be > 0.' % speed)
    Pattern.__init__(self)
    Buffer.__init__(self, size=STRIP_LENGTH + 2)
    self.__seq = iter(color_sequence)
    self.__speed = speed
    self.__offset = 1.0
    self.__t = None

  def IsChanged(self):
    return self.__seq is not None

  def SetSpeed(self, speed):
    self.__UpdateColorsAndOffset()
    self.__speed = float(speed)

  def __UpdateColorsAndOffset(self):
    if self.__seq is None:
      return
    if self.__t is None:
      self.__t = time.time()
    t = time.time()
    self.__offset += (t - self.__t) * self.__speed
    self.__t = t
    while self.__offset >= 1.0:
      try:
        c = self.__seq.next()
      except StopIteration:
        self.__seq = None
        break
      self.InsertAndPop(c)
      self.__offset -= 1.0

  def Apply(self, color_buffer):
    Pattern.Apply(self, color_buffer)
    self.__UpdateColorsAndOffset()
    colors = color_buffer.GetColors()
    f = self.__offset
     for i in xrange(min(len(colors), len(self._colors)-1)):
      colors[i].add(self._colors[i].scaled(f))
      colors[i].add(self._colors[i+1].scaled(1.0-f))

