from Manifest import Buffer
from Manifest import DataSender, Serialization, time

# TODO(markfickett) Get an ack from DataSender? Have flush work?
DELAY = 0.013 # approx minimum delay for error-free receipt at 115200 baud

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

	def sendAndWait(self):
		"""
		Send the current contents of the color buffer to the currently
		set Serial, and wait for the send to complete to avoid read
		errors on the receiving end with immediately repeated sends.
		"""
		if not self.__serial:
			raise RuntimeError('Call setSerial (or provide in'
				' constructor) before sending.')
		self.__serial.write(
			DataSender.Format(
				COLORS=Serialization.ToBytes(self.getColors())))
		self.__serial.flush()
		time.sleep(DELAY)

