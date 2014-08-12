"""
Demonstrate generating colors in Python and using DataSender to transfer them
over Serial to the Arduino. (Optionally simulate entirely in Python.)

Use abstracting classes to manage lists of Patterns, and writing.
"""

# Configuration options.
DUMMY_SERIAL = False  # Do not write to serial (to the Arduino).
DRAW = True  # Draw using turtle graphics (on screen) as well as to LEDs.
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
    sender = SendingPatternList()
  else:
    sender = SendingPatternList(sending_buffer=TurtleBuffer())

  # Add some Patterns.
  #sender.append(InterpolatedMarquee(
  #  Sequences.GenerateRandom(bright_interval=6),
  #    speed=15))
  sender.append(InterpolatedMarquee(
    Sequences.GenerateHueGradient(repeat_interval=10)))
  sender.append(Pulser(color=Color(rgb=(0, 0, 1)), reverse=True))

  # Open the serial device (connection to the Arduino).
  if DUMMY_SERIAL:
    data_sender = data_sender.DummySender(SERIAL_DEVICE, silent=True)
  else:
    data_sender = data_sender.Sender(SERIAL_DEVICE)

  with data_sender:
    sender.SetSender(data_sender)

    t = time.time()
    actual_trials = 0

    # Continue updating until all the Patterns expire.
    # If this does not happen, wait for control-C.
    print 'Type ^C (hold control, press c) to stop.'
    try:
      while True:
        sender.UpdateAndSend()  # Uses data_sender to send the colors.
        sys.stdout.write('.')
        sys.stdout.flush()
        data_sender.ReadAndPrint()  # Reads any responses from the Arduino.
        actual_trials += 1
    except KeyboardInterrupt:
      traceback.print_exc()
      print 'Got ^C, exiting.'

    dt = time.time() - t

  print 'Elapsed per %d updates: %.2fs' % (actual_trials, dt)
  print 'Updates per second: %.2f' % (actual_trials / dt)

