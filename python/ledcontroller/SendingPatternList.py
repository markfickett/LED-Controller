from Manifest import SendingBuffer
from patterns.Manifest import PatternList

class SendingPatternList(PatternList):
	"""
	A PatternList which also has a SendingBuffer, simplifying managing a
	strip which is to display only a set of Python-generated patterns.
	"""
	def __init__(self, sendingBuffer=None, reverse=False):
		PatternList.__init__(self)
		if sendingBuffer:
			self.__sendingBuffer = sendingBuffer
		else:
			self.__sendingBuffer = SendingBuffer()
		self.__reverse = reverse

	def setSerial(self, outputSerial):
		"""
		Set the serial object used by the SendingBuffer.
		"""
		self.__sendingBuffer.setSerial(outputSerial)

	def  updateAndSend(self):
		"""
		If necessary: clear the sending buffer, apply all patterns to
			it, and send.
		@return whether any pattern was updated, triggering a send
		"""
		if self.isChanged():
			self.__sendingBuffer.clear()
			self.apply(self.__sendingBuffer)
			self.__sendingBuffer.sendAndWait(reverse=self.__reverse)
			return True
		else:
			return False

