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
		bright_interval=None,
		scale_bright=1.0,
		scale_dim=DEFAULT_DIM):
	"""
	Generate a sequence of random Colors.
	@param limit the number of random Colors to generate; or None (default),
		to continue forever
	@param bright_interval If given, every bright_interval colors will be
		scaled by scale_bright, and the rest scaled by scale_dim.
	"""
	n = 0
	while (limit is None) or n < limit:
		c = Color.CreateRandom()
		if bright_interval is not None:
			if n % bright_interval == 0:
				c = c.Scaled(scale_bright)
			else:
				c = c.Scaled(scale_dim)
		n += 1
		yield c

HUE_CHANNEL_OFFSETS = (math.pi/2.0, 0.0, -math.pi/2.0)
def GenerateHueGradient(repeat_interval=STRIP_LENGTH, limit=None):
	"""
	Generate a gradient through hues.
	@param repeat_interval how many Colors before cycling back to the start,
		defaulting to the STRIP_LENGTH shared constant
	@param limit the number of Colors to generate; or None (default), to
		continue forever
	"""
	n = 0
	t = 0.0
	step = 2.0 * math.pi / repeat_interval
	while (limit is None) or n < limit:
		c = Color(rgb=[
			(0.5*(1.0 + math.sin(t + x)))
			for x in HUE_CHANNEL_OFFSETS
		])
		t += step
		n += 1
		yield c

