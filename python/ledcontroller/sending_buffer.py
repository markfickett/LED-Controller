from Manifest import Buffer
from Manifest import data_sender, serialization, time, DATA_RECEIVER_COLOR_KEY

class SendingBuffer(Buffer):
  """
  A Color buffer which also encapsulates logic for sending the Color
  data as a byte array (string) to the Arduino over Serial.
  """
  def __init__(self, sender=None, **kwargs):
    """
    @param output_serial the Serial output stream to be written to,
      which may be set/replaced at any point using setSerial.
    """
    Buffer.__init__(self, **kwargs)
    self.__sender = sender

  def SetSender(self, sender):
    self.__sender = sender

  def Send(self, reverse=False):
    """
    Send the current contents of the color buffer using the current
    data_sender.Sender, which manages structure and synchronization.
    @param reversed if True, send Colors in reverse order
    """
    if not self.__sender:
      raise RuntimeError('Call setSender (or provide in'
        ' constructor) before sending.')
    colors = self.GetColors()
    if reverse:
      colors = reversed(colors)
    sender_kwargs = {
      DATA_RECEIVER_COLOR_KEY: serialization.ToBytes(colors),
    }
    self.__sender.send(**sender_kwargs)

