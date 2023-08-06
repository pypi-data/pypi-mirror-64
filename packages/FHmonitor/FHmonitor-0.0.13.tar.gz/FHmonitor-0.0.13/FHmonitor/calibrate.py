
from FHmonitor.atm90_e32_pi import ATM90e32
from FHmonitor.error_handling import handle_exception
import json
import os
import logging
logger = logging.getLogger(__name__)
VOLTAGE = "voltage"
CURRENT = "current"


class Calibrate:
    """The Calibrate class simplifies voltage and current
    calibration of an atm90e32 energy monitor.  Known
    parameters for calibration are in calibration.json.
    The values for the parameter are read in and then
    modified based on calibration results.  Calibrating
    requires a Kill-A-Watt for voltage calibration.
    """

    def __init__(self):
        self.filepath = os.path.join(
            os.path.dirname(__file__), "calibration.json")
        self._get_stored_calibration_values()

    # -----------------------------------------------------------

    def calibrate_voltage(self, save_new_gain=True):
        """The default value that goes into the voltage calibration
        is VoltageGain = 36650.  This is the voltage calibration for
        Jameco 9VAC Power Supply, product no. = 157041.  If the
        Power Supply being used is not this one, voltage readings
        will be off unless a new VoltageGain value is calculated
        through calibration.

        In order to calibrate, an external Kill-A-Watt is used as the
        reference voltage.  The user will be asked to enter the voltage
        reading from the Kill-A-Watt.  Given this reference voltage,
        a new VoltageGain value is calculated that will be used when
        initializing the atm90e32.  Default values are held in
        calibration.json.
        """
        voltage_kill_a_watt = self._get_kill_a_watt_input(VOLTAGE)
        logger.info(f'Kill-A-watt voltage reading:    {voltage_kill_a_watt}V')
        voltage_reading = self._take_voltage_reading(self.VoltageGain)
        new_gain = int(round(voltage_kill_a_watt/voltage_reading *
                             self.VoltageGain))
        logger.info(f'New Voltage gain is {new_gain}.')
        self._take_voltage_reading(new_gain)
        if save_new_gain:
            self._save_reading_to_calibration_file('VoltageGain', new_gain)
            logger.info('Saved Reading.')
        else:
            logger.info('Did NOT save reading.')

    def calibrate_current(self, save_new_gain=True):
        # Plug in somethiing with a CT clamped on it to measure the current.

        # Get User's Kill-A-Watt reading
        current_kill_a_watt = self._get_kill_a_watt_input(CURRENT)
        current_reading = self._take_current_reading(self.CurrentGain)
        new_gain = int(round(current_kill_a_watt /
                             current_reading*self.CurrentGain))
        self._take_current_reading(new_gain)
        if save_new_gain:
            self._save_reading_to_calibration_file('CurrentGain', new_gain)
            logger.info('Saved Reading.')
        else:
            logger.info('Did NOT save reading.')

    def _take_voltage_reading(self, voltage_gain):
        """This internal method takes a voltage reading assuming the
        caller wants to try various voltage gain values.  Useful for
        voltage calibration.
        """
        energy_sensor = ATM90e32(self.lineFreq, self.PGAGain, voltage_gain,
                                 self.CurrentGain, 0, self.CurrentGain)
        voltage_reading = energy_sensor.line_voltageA
        logger.info(f'Energy monitor voltage reading: {voltage_reading}V')
        return voltage_reading

    def _take_current_reading(self, current_gain):
        energy_sensor = ATM90e32(self.lineFreq, self.PGAGain, self.VoltageGain,
                                 current_gain, 0, current_gain)
        # Figure out which port the CT is plugged into
        iA = energy_sensor.line_currentA
        iC = energy_sensor.line_currentC
        if iA > iC:
            current_reading = iA
        else:
            current_reading = iC
        logger.info(f'Energy monitor current reading: {current_reading}A')
        return current_reading

    def _save_reading_to_calibration_file(self, param_string, value):
        with open(self.filepath, "r") as json_file:
            json_data = json.load(json_file)
            json_data[param_string] = value
        with open(self.filepath, "w") as json_file:
            json.dump(json_data, json_file, indent=2)
        logger.info(f'Saved updated {param_string} to calibration.json')

    def _get_stored_calibration_values(self):
        try:

            with open(self.filepath) as json_file:
                json_data = json.load(json_file)
                self.lineFreq = self._set_calibrate_param(
                    json_data, 'lineFreq', 4485)
                self.PGAGain = self._set_calibrate_param(
                    json_data, 'PGAGain', 21)
                self.VoltageGain = json_data['VoltageGain']
                if self.VoltageGain <= 0:
                    self.VoltageGain = 36650
                    logger.warning(f'VoltageGain is <= 0.  Setting to 36650')
                self.CurrentGain = json_data['CurrentGain']
                if self.CurrentGain <= 0:
                    self.CurrentGain = 25368
                    logger.warning(
                        f'CurrentGain is <= 0.  Setting to 25368')

        except OSError as e:
            handle_exception(e)
        except Exception as e:
            handle_exception(e)

    def _set_calibrate_param(self, json_data, param_string, default_value):
        """This internal function makes sure calibration values stored in the
        calibration.json file can be resolved correctly."

        :param json_data: dict of calibration params loaded from
            calibration.json
        :param param_string: Name of the parameter (e.g.: lineFreq)
        :param default_value: Calibration settings have default values that
            are used when a value can't be determined.
        :return: The calibration value from calibration.json
        """
        try:
            value = json_data[param_string]
            if value <= 0:  # Will TypeError if value is not a number.
                value = default_value
                logger.warning(
                    f'{param_string} is <= 0.  Setting to {default_value}')
        except TypeError:
            if self._is_int(json_data[param_string]):
                value = int(json_data[param_string])
            else:
                value = default_value
                logger.warning(
                    f"""The data type for the value of {param_string} is """
                    f"""incorrect. Setting to {value}.""")
        except KeyError:
            value = default_value
            logger.warning(
                f"""The Key {param_string} was not found."""
                F"""  Setting to {default_value}.""")
        return value

    def _is_int(self, val):
        try:
            int(val)
        except ValueError:
            return False
        return True

    def _get_kill_a_watt_input(self, voltage_or_current):
        input_str = f'Enter Kill-A-Watt {voltage_or_current} reading:'
        # Input Kill-A-Watt reading for reference value.
        while True:
            try:
                value = float(input(input_str))
            except ValueError:
                print('Sorry, I didn\'t undestand that.  Please try again.')
                continue
            else:
                break

        return value
