"""
Demonstrate generating colors in Python and using DataSender to transfer them
over Serial to the Arduino. (Optionally simulate entirely in Python.)

Use abstracting classes to manage lists of Patterns, and writing.
"""

# Configuration options.
# Do not write to serial (to the Arduino).
DUMMY_SERIAL = False
# Draw using turtle graphics (on screen) as well as to LEDs. Note that this
# slows things down significantly.
DRAW = False
SERIAL_DEVICE = '/dev/tty.usbmodemfa141'

import traceback

from Manifest import ledcontroller, sys

from ledcontroller.Manifest import time, data_sender
from ledcontroller.Manifest import SendingPatternList, Color, \
  TurtleBuffer, sequences
from ledcontroller.patterns.Manifest import InterpolatedMarquee, Pulser

if __name__ == '__main__':
  # A SendingPatternList holds the list of Patterns (which create the
  # colors), and manages writing them to the Arduino.
  if not DRAW:
    # Create a SendingBuffer with defaults.
    color_sender = SendingPatternList()
  else:
    color_sender = SendingPatternList(sending_buffer=TurtleBuffer())

  # Add some Patterns.
  #color_sender.Append(InterpolatedMarquee(
  #  sequences.GenerateRandom(bright_interval=6),
  #    speed=15))
  color_sender.Append(InterpolatedMarquee(
    (c.Scaled(0.1) for c in
     sequences.GenerateHueGradient(repeat_interval=50)),
    speed=5.0))
  color_sender.Append(Pulser(
      color=Color(rgb=(0, 0, 1)),
      reverse=True,
      add_delay=3.0))

  # Open the serial device (connection to the Arduino).
  if DUMMY_SERIAL:
    serial_sender = data_sender.DummySender(SERIAL_DEVICE, silent=True)
  else:
    serial_sender = data_sender.Sender(SERIAL_DEVICE)

  with serial_sender:
    color_sender.SetSender(serial_sender)

    t = time.time()
    actual_trials = 0
    exc_count = 0

    # Continue updating until all the Patterns expire.
    # If this does not happen, wait for control-C.
    print 'Type ^C (hold control, press c) to stop.'
    try:
      while True:
        actual_trials += 1
        try:
          color_sender.UpdateAndSend()  # Uses serial_sender to send the colors.
          serial_sender.ReadAndPrint()  # Reads any responses from the Arduino.
        except data_sender.TimeoutException as e:
          print 'Timeout waiting for acknowledgement during read/write.'
          exc_count += 1
          if exc_count >= 50:
            print 'Giving up after too many timeouts.'
            raise
        if actual_trials % 100 == 0:
          sys.stdout.write('.')
          sys.stdout.flush()
    except KeyboardInterrupt:
      traceback.print_exc()
      print 'Got ^C, exiting.'

    dt = time.time() - t

  print 'Elapsed per %d updates: %.2fs' % (actual_trials, dt)
  print 'Updates per second: %.2f' % (actual_trials / dt)

