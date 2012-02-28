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

	def setSender(self, sender):
		"""
		Set the DataSender.Sender object used by the SendingBuffer.
		"""
		self.__sendingBuffer.setSender(sender)

	def  updateAndSend(self):
		"""
		If necessary: clear the sending buffer, apply all patterns to
			it, and send.
		@return whether an update (and send) was necessary
		"""
		if self.isChanged():
			self.__sendingBuffer.clear()
			self.apply(self.__sendingBuffer)
			self.__sendingBuffer.send(
				reverse=self.__reverse)
			return True
		else:
			return False

