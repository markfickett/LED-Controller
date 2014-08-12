from Manifest import Pattern
from ledcontroller.Manifest import Buffer, Color, time

class Pulser(Pattern):
  """Send pulses of a color along the LED strip."""
  def __init__(self, add_delay=1.0, speed=14.0,
    """
    Args:
      color the color of the center (maximally intense part) of a pulse
      width the maximum number of LEDs affected by a pulse (diameter)
      add_delay the number of seconds between new pulses
      speed the number of LEDs down the strip a pulse travels / second
      reverse If True, pulses travel in the opposite direction; by
          default, the start from index 0.
    """
      color=Color(rgb=(1,1,1)), width=6.0,
      reverse=False):
    Pattern.__init__(self)
    if add_delay <= 0:
      raise ValueError('add_delay value %s is not > 0.'
        % add_delay)
    if speed == 0:
      raise ValueError('speed value %s is 0.')
    if width <= 0:
      raise ValueError('width value %s is not > 0.'
        % width)
    self.__add_delay = float(add_delay)
    self.__speed = float(speed)
    self.__interval = self.__speed * self.__add_delay
    self.__radius = width/2.0
    self.__reverse = reverse
    self.__color = color

    self.__t0 = None

  def IsChanged(self):
    return True

  def __GeneratePositions(self, max_index):
    t = time.time()
    if self.__t0 is None:
      self.__t0 = t
    dt = t - self.__t0
    max_pos = max_index + self.__radius
    repeats = int(dt / self.__add_delay)
    dt -= repeats*self.__add_delay
    i = 0
    p = -self.__radius + self.__speed*dt
    while i <= repeats and p <= max_pos:
      yield p
      p += self.__interval
      i += 1

  def Apply(self, color_buffer):
    """Recalculates pulse positions for the current time and add pulses."""
    Pattern.Apply(self, color_buffer)
    colors = color_buffer.GetColors()
    n = len(colors)
    for raw_center in self.__GeneratePositions(n-1):
      center = raw_center
      if self.__reverse:
        center = (n - 1) - center
      min_index = int(1 + center - self.__radius)
      max_index = int(center + self.__radius)
      for i in xrange(min_index, max_index + 1):
        if i < 0 or i >= n:
          continue
        dx = abs(center - i)
        f = min(1.0, dx / self.__radius)
        colors[i] = colors[i].scaled(f)
        colors[i].add(self.__color.scaled(1.0 - f))

