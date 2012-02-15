from Manifest import Pattern
from ledcontroller.Manifest import Buffer, Color, time

class Pulser(Pattern):
	"""
	Every sendDelay seconds, create a new Color at one end of the strip.
	Every moveDelay seconds it's on the strip, advance each dot by one LED.
	@param width number of LEDs lit by a pulse
	"""
	def __init__(self, addDelay=0.75, moveDelay=0.05,
			color=Color(rgb=(1,1,1)), width=1,
			reverse=False):
		Pattern.__init__(self)
		if addDelay <= 0:
			raise ValueError('addDelay value %s is not > 0.'
				% sendDelay)
		if moveDelay <= 0:
			raise ValueError('moveDelay value %s is not > 0.'
				% sendDelay)
		if width < 1:
			raise ValueError('width value %s is not >= 1.'
				% width)
		self.__addDelay = addDelay
		self.__moveDelay = moveDelay
		self.__width = int(width)
		self.__lastAddTime = None
		self.__reverse = reverse
		self.__color = color
		self.__pulses = []

	def __addAndUpdatePulses(self):
		"""
		Add new pulses and move existing pulses.
		If applicable, call _setChanged().
		"""
		t = time.time()

		# move pulses
		for pulse in self.__pulses:
			pos, lastMoveTime = pulse
			moveDt = t - lastMoveTime
			changed = False
			while moveDt >= self.__moveDelay:
				pos += 1
				moveDt -= self.__moveDelay
				lastMoveTime += self.__moveDelay
				changed = True
			if changed:
				self._setChanged()
				pulse[0] = pos
				pulse[1] = lastMoveTime

		# add new pulses
		addDt = 0
		force = False
		if self.__lastAddTime is None:
			self.__lastAddTime = t - self.__addDelay
		addDt = t - self.__lastAddTime
		while addDt >= self.__addDelay:
			addTime = self.__lastAddTime + self.__addDelay
			self.__pulses.append([0, addTime])
			self.__lastAddTime += self.__addDelay
			addDt -= self.__addDelay
			self._setChanged()

	def isChanged(self):
		self.__addAndUpdatePulses()
		return Pattern.isChanged(self)

	def apply(self, colorBuffer):
		"""
		Add the pulses at their current locations to the Buffer.
		Remove any pulses which are past the end of the Buffer.
		"""
		self.__addAndUpdatePulses()
		Pattern.apply(self, colorBuffer)
		colors = colorBuffer.getColors()
		pastEnd = []
		for pulse in self.__pulses:
			startPos, _ = pulse
			inStrip = False
			for i in xrange(startPos, startPos + self.__width):
				pos = i
				if self.__reverse:
					pos = (len(colors) - 1) - pos
				if pos >= 0 and pos < len(colors):
					colors[pos].add(self.__color)
					inStrip = True
			if not inStrip:
				pastEnd.append(pulse)
		for pulse in pastEnd:
			self.__pulses.remove(pulse)

