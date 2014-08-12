from Manifest import Color, STRIP_LENGTH

class Buffer:
  """Encapsulation of a list of Colors."""
  def __init__(self, size=STRIP_LENGTH):
    """
    Initializes a list of default (black) Colors.
    Args:
      size Optionally specifies a size for the buffer. By default, it is the
        same size as the LED strip (from the STRIP_LENGTH shared constant).
    """
    self._colors = []
    for i in xrange(size):
      self._colors.append(Color())

  def GetSize(self):
    return len(self._colors)

  def GetColors(self):
    """Returns the internal list of Colors, for modification."""
    return self._colors

  def Clear(self):
    """Resets all the colors to blank (black)."""
    for c in self._colors:
      c.Clear()

  def SetFromBuffer(self, buffer):
    """Sets the contents of this buffer to match another buffer (deep copy)."""
    for local_color, other_color in zip(
      self._colors, buffer.GetColors()):
      local_color.set(other_color)

  def AddBuffer(self, buffer):
    """Adds another buffer's colors to this'.

    Zips from index 0, and does not affect or use colors past the end of the
    shorter buffer.
    """
    for local_color, other_color in zip(
      self._colors, buffer.GetColors()):
      local_color.add(other_color)

  def InsertAndPop(self, color):
    """
    Inserts the given Color into the beginning (index 0) of the color
    list, and pop a Color from the end (maintaining size).
    """
    self._colors.insert(0, color)
    return self._colors.pop()

