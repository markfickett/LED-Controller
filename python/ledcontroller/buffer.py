from Manifest import Color, STRIP_LENGTH

class Buffer:
  """
  Encapsulate a list of Colors.
  """
  def __init__(self, size=STRIP_LENGTH):
    """
    Initialize a list of default (black) Colors.
    @param size Optionally specifies a size for the buffer. By default, it
      is the same size as the LED strip (from the STRIP_LENGTH
      shared constant).
    """
    self._colors = []
    for i in xrange(size):
      self._colors.append(Color())

  def GetSize(self):
    return len(self._colors)

  def GetColors(self):
    """
    @return the internal list of Colors, for modification.
    """
    return self._colors

  def Clear(self):
    """
    Reset all the colors to blank (black).
    """
    for c in self._colors:
      c.Clear()

  def SetFromBuffer(self, buffer):
    """
    Set the contents of this buffer to match another buffer.
    """
    for local_color, other_color in zip(
      self._colors, buffer.GetColors()):
      local_color.set(other_color)

  def AddBuffer(self, buffer):
    """
    Add another buffer's colors to this'. Zip from index 0, and do
    not affect or use colors past the end of the shorter buffer.
    """
    for local_color, other_color in zip(
      self._colors, buffer.GetColors()):
      local_color.add(other_color)

  def InsertAndPop(self, color):
    """
    Insert the given Color into the beginning (index 0) of the color
    list, and pop a Color from the end (maintaining size).
    """
    self._colors.insert(0, color)
    return self._colors.pop()

