class Pattern:
  """
  Base class for (animating) color patterns.
  """
  def __init__(self):
    self.__changed = True
    self.__expired = False

  def Apply(self, color_buffer):
    """Typically, adds the colors from the pattern to the given buffer.

    More generally, modifies the given color buffer according to this
    pattern's current state.
    """
    self._ClearChanged()

  def IsChanged(self):
    """
    Returns:
      whether this Pattern has changed since last rendered. Specifically,
          whether a re-render is necessary on account of this Pattern
    """
    return self.__changed

  def _SetChanged(self):
    self.__changed = True

  def _ClearChanged(self):
    self.__changed = False

  def IsExpired(self):
    """Returns True if calls to apply will never again have an effect."""
    return self.__expired

  def Expire(self):
    self.__expired = True

