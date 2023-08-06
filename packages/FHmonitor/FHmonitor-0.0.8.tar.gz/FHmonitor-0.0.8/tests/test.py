from FHmonitor.calibrate import Calibrate
import logging
logging.basicConfig(level=logging.DEBUG)

c = Calibrate()
# c.calibrate_voltage(save_new_gain=True)
c.calibrate_current(save_new_gain=True)
