from Manifest import Buffer
from Manifest import DataSender, Serialization, time, DATA_RECEIVER_COLOR_KEY

class SendingBuffer(Buffer):
	"""
	A Color buffer which also encapsulates logic for sending the Color
	data as a byte array (string) to the Arduino over Serial.
	"""
	def __init__(self, outputSerial=None, **kwargs):
		"""
		@param outputSerial the Serial output stream to be written to,
			which may be set/replaced at any point using setSerial.
		"""
		Buffer.__init__(self, **kwargs)
		self.__serial = outputSerial

	def setSerial(self, outputSerial):
		self.__serial = outputSerial

	def sendAndWait(self, reverse=False):
		"""
		Send the current contents of the color buffer to the currently
		set Serial, and wait for the send to complete to avoid read
		errors on the receiving end with immediately repeated sends.
		@param reversed if True, send Colors in reverse order
		@return any Serial response read while waiting for
			acknowledgement
		"""
		if not self.__serial:
			raise RuntimeError('Call setSerial (or provide in'
				' constructor) before sending.')
		colors = self.getColors()
		if reverse:
			colors = reversed(colors)
		senderKwargs = {
			DATA_RECEIVER_COLOR_KEY: Serialization.ToBytes(colors),
		}
		output = DataSender.SendAndWait(self.__serial, **senderKwargs)
		return output

