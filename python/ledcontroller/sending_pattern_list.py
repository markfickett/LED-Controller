from Manifest import SendingBuffer
from patterns.Manifest import PatternList

class SendingPatternList(PatternList):
  """
  A PatternList which also has a SendingBuffer, simplifying managing a
  strip which is to display only a set of Python-generated patterns.
  """
  def __init__(self, sending_buffer=None, reverse=False):
    PatternList.__init__(self)
    if sending_buffer:
      self.__sending_buffer = sending_buffer
    else:
      self.__sending_buffer = SendingBuffer()
    self.__reverse = reverse

  def SetSender(self, sender):
    """
    Set the data_sender.Sender object used by the SendingBuffer.
    """
    self.__sending_buffer.SetSender(sender)

  def  UpdateAndSend(self):
    """
    If necessary: clear the sending buffer, apply all patterns to
      it, and send.
    @return whether an update (and send) was necessary
    """
    if self.IsChanged():
      self.__sending_buffer.Clear()
      self.Apply(self.__sending_buffer)
      self.__sending_buffer.Send(
        reverse=self.__reverse)
      return True
    else:
      return False

