"""
Functions to generate sequences of Colors in useful or pretty patterns.
"""

__all__ = [
	'GetSentienls',

	'GenerateRandom',
	'GenerateHueGradient',
]

from Manifest import Color, STRIP_LENGTH, math

DEFAULT_DIM = 0.1
def GetSentinels():
	"""
	Get a list of known colors, for a familiar test pattern:
		cyan
		yellow
		magenta
		dim red
	"""
	return [
		Color(rgb=(0.0, 1.0, 1.0)),
		Color(rgb=(1.0, 1.0, 0.0)),
		Color(rgb=(1.0, 0.0, 1.0)),
		Color(rgb=(DEFAULT_DIM, 0.0, 0.0)),
	]

def GenerateRandom(limit=None,
		brightInterval=None,
		scaleBright=1.0,
		scaleDim=DEFAULT_DIM):
	"""
	Generate a sequence of random Colors.
	@param limit the number of random Colors to generate; or None (default),
		to continue forever
	@param brightInterval If given, every brightInterval colors will be
		scaled by scaleBright, and the rest scaled by scaleDim.
	"""
	n = 0
	while (limit is None) or n < limit:
		c = Color.CreateRandom()
		if brightInterval is not None:
			if n % brightInterval == 0:
				c = c.scaled(scaleBright)
			else:
				c = c.scaled(scaleDim)
		n += 1
		yield c

HUE_CHANNEL_OFFSETS = (math.pi/2.0, 0.0, -math.pi/2.0)
def GenerateHueGradient(repeatInterval=STRIP_LENGTH, limit=None):
	"""
	Generate a gradient through hues.
	@param repeatInterval how many Colors before cycling back to the start,
		defaulting to the STRIP_LENGTH shared constant
	@param limit the number of Colors to generate; or None (default), to
		continue forever
	"""
	n = 0
	t = 0.0
	step = 2.0 * math.pi / repeatInterval
	while (limit is None) or n < limit:
		c = Color(rgb=[
			(0.5*(1.0 + math.sin(t + x)))
			for x in HUE_CHANNEL_OFFSETS
		])
		t += step
		n += 1
		yield c

