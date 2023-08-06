FHmonitor package
=================

Intro
~~~~~

The FHmonitor package runs on a
Raspberry Pi that is communicating with an atm90e32 chip over SPI.
We use `Circuit Setup's energy meter <https://circuitsetup.us/index.php/product/split-single-phase-real-time-whole-house-energy-meter-v1-4/>`_,
which uses the atm90e32.  Current Transformers (CTs) that are plugged into the energy meter clamp onto the power lines.  The CTs provide a signal to the elecriticy monitor that is then interpreted into power line measurements like voltage and current.

The FHmonitor package:

   -  reads power readings from the electricity monitor.
   -  stores readings into the mongodb running on the Raspberry Pi.

.. image:: images/Electricity_Monitor_Rasp_Pi.png
   :width: 300

The Hardware
~~~~~~~~~~~~
Before using the FHmonitor package, you must have a running energy monitor.  The energy monitor consists of:

* `Raspberry Pi 3 Model B+ <https://www.adafruit.com/product/3055>`_
* `Circuit Setup's energy meter <https://circuitsetup.us/index.php/product/split-single-phase-real-time-whole-house-energy-meter-v1-4/>`_
* An LED of any color.  The LED helps with debugging.
* A resistor between 400 and 1K ohm.

Hardware Setup Steps
~~~~~~~~~~~~~~~~~~~~
- :doc:`Set up the Raspberry Pi. <rasppi>`
- :doc:`Connect the Hardware. <connect_the_hw>`

TODO: CONNECT THE CTs....


Say hello
~~~~~~~~~

Once you install the FHmonitor package within your virtualenv, just say hello::

(venv)$hello

hello is a command that runs the following script:
::

   from FHmonitor.monitor import Monitor

   m = Monitor()
   m.init_sensor()  # You will most likely need to adjust.
   pA, pR = m.take_reading()

Calibration
~~~~~~~~~~~

Readings will be off unless the energy monitor is calibrated.  The most
important thing to calibrate is the voltage reading.

**Note: You need only calibrate if you are unsure if the Power Transformer
used with the energy monitor has not been already calibrated.**

To calibrate:
- Plug the Power Transformer into a `Kill-A-Watt <https://amzn.to/2Mcjkt7>`_.  The Kill-A-Watt will
be the reference voltage.

Note: Make sure you understand the energy sensor initialization
parameters of the :meth:`~FHmonitor.monitor.Monitor.init_sensor` method.  You
could be using a different Power Transformer and/or Current Transformers.
Some default values are discussed in `Circuit Setup's documentation <https://github.com/CircuitSetup/Split-Single-Phase-Energy-Meter#calibration>`_.


Calibrating the Monitor
~~~~~~~~~~~~~~~~~~~~~~~

At a minimum, the voltage should be calibrated prior to using a new
Power Transformer with the energy monitor.  If the same Power Transformer
is used on other energy monitors, the calibration values should be fine with it.


- Measure the voltage reading from the energy monitor::

   from FHmonitor.atm90_e32_pi import ATMATM90e32
   energy_sensor = ATM90e32(lineFreq, PGAGain, VoltageGain,
                            CurrentGainCT1, 0, CurrentGainCT2)
   m.init_sensor() # Initialize with the current values.
   voltage_reading = m.
Variables for setting monitor calibration are found within :meth:`~FHmonitor.monitor.Monitor.init_sensor`.
Readings will most likely be off unless you calibrate what the atm90e32
chip assumes about the Power Tranformer and Current Tranformers you are using.
We use the default values for::

   lineFreq = 4485  # 4485 for 60 Hz (North America)
   PGAGain = 21     # 21 for 100A (2x), 42 for >100A (4x)

What is left to calibrate are the voltage and current gain values.
These are important, because they can cause havoc with the accuracy of the voltage, current, power readings.

Voltage Calibration
~~~~~~~~~~~~~~~~~~~

The gain value is tied to the transformer we are using.  We decided to standardize on the `Jameco 9V power supply, part no. 157041 <https://www.jameco.com/shop/ProductDisplay?catalogId=10001&langId=-1&storeId=10001&productId=157041>`_.  The default voltage gain for a 9V AC transformer was 42080.  With this setting for voltage gain, our readings were over 15 watts higher than what the actual voltage was.

To determine the actual voltage, we used the extremely useful `Kill-A-Watt <https://amzn.to/2Mcjkt7>`_
as the voltage reference.

To calibrate the voltage gain, we used the formula/info in `the app note <https://github.com/BitKnitting/energy_monitor_firmware/blob/master/docs/Atmel-46103-SE-M90E32AS-ApplicationNote.pdf>`_
See section 4.2.6 Voltage/Current Measurement
Calibration where it discusses using existing voltage gain.

where:

- reference voltage = reading from Kill-A-Watt
- voltage measurement value = the reading for voltage we got from initializing the atm90e32 instance with the voltage gain value and reading the `line_voltageA` property.

new `VoltageGain` = reference voltage/voltage measurement * current voltage gain

e.g. using a different 9V transformer:
- Kill-A-Watt shows V = 121.5
- reading shows voltage at 117.5
- current `VoltageGain` is 36650

new `Voltage Gain = 121.5/117.5*36650 = 37898`

Calculate the value, and change the `VoltageGain` to the calculated value.

Current Calibration
~~~~~~~~~~~~~~~~~~~

We found the default current gain gave current readings close to what we
got with the Kill-A-Watt.  Because it was easy to do so, we set the
`CurrentGainCT1` and `CurrentGainCT2` values to our calculation,
using the current readings in place of the voltage readings as discussed
in the app note.


Monitor class
-------------

The class you will use the most is :class:`~FHmonitor.monitor.Monitor`.
This class contains methods to:

* Take an active and reactive power reading (see :meth:`~FHmonitor.monitor.Monitor.take_reading`).

   * Before taking a reading, the energy meter must be initialized (see :meth:`~FHmonitor.monitor.Monitor.init_sensor`).
* Store the reading into the mongo db running on the Raspberry Pi (see :meth:`~FHmonitor.monitor.Monitor.store_reading`).

   * Before storing readings, the mongo db must be opened (see :meth:`~FHmonitor.monitor.Monitor.open_db`).

.. automodule:: FHmonitor.monitor
   :members:
   :undoc-members:

Store class
-----------
The :class:`~FHmonitor.monitor.Monitor` class uses an implementation of the :class:`~FHmonitor.store.Store` abstract class to store power readings into a datastore.  The only data store currently available is the mongo db.  We originally started with
a Firebase DB, but decided running everything on a Raspberry Pi was much easier.  Mongo db can be run on the Raspberry Pi at no additional $ cost.


.. automodule:: FHmonitor.store
   :members:
   :undoc-members:
   :show-inheritance:








