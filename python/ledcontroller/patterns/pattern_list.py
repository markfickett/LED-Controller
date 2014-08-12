from Manifest import Pattern

class PatternList(Pattern):
  """
  Encapsulate management for multiple Patterns: check for changes, apply,
  and discard expired patterns.
  """
  def __init__(self):
    Pattern.__init__(self)
    self.__patterns = []

  def Append(self, pattern):
    """Adds the given pattern to the list.

    Render order matches order of addition. Patterns are automatically removed
    once expired.
    """
    self.__patterns.append(pattern)

  def Remove(self, pattern, strict=True):
    """Removes the given pattern from the list.

    Args:
      strict whether to match the default Python behavior, or (if False) to
          silently do nothing if the pattern is not already in the list
    """
    if strict or (pattern in self.__patterns):
      self.__patterns.remove(pattern)

  def Apply(self, colorBuffer):
    for p in self.__patterns:
      p.Apply(colorBuffer)

  def IsChanged(self):
    """Returns whether any pattern in the list has changed.

    Also does garbage collection, removing expired patterns.
    """
    expired = []
    changed = False
    for p in self.__patterns:
      if p.IsExpired():
        expired.append(p)
        changed = True
      else:
        changed |= p.IsChanged()
    for p in expired:
      self.__patterns.remove(p)
    return changed

