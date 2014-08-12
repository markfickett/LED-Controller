# Set up paths to include the ledcontroller Python library.
import os, sys
led_controller_lib_path = os.path.abspath(
  os.path.join(os.path.dirname(__file__), '..', '..', 'python'))
sys.path.append(led_controller_lib_path)

import ledcontroller

