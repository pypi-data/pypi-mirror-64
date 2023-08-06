
Intro
=====

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
============
Before using the FHmonitor package, you must have a running energy monitor.  The energy monitor consists of:

* `Raspberry Pi 3 Model B+ <https://www.adafruit.com/product/3055>`_
* `Circuit Setup's energy meter <https://circuitsetup.us/index.php/product/split-single-phase-real-time-whole-house-energy-meter-v1-4/>`_
* An LED of any color.  The LED helps with debugging.
* A resistor between 400 and 1K ohm.

Hardware Setup Steps
====================
- :doc:`Set up the Raspberry Pi. <rasppi>`
- :doc:`Connect the Hardware. <connect_the_hw>`

Calibrating the Meter
=====================
Getting good readings from the atm90e32 assumes the parameters defined in `calibration.json <https://github.com/BitKnitting/FHmonitor/blob/master/FHmonitor/calibration.json>`_
are set to reflect the environment in which the meter will be taking readings.
The various calibration parameters are:

- **Frequency of AC coming into your home - lineFreq**:  Since we are in North America where the AC frequency is 60Hz, We set this to **4485**.  The rest of the world is at 50Hz. If that is how your home's power is configured, change this value in `calibration.json <https://github.com/BitKnitting/FHmonitor/blob/master/FHmonitor/calibration.json>`_ to **389**.

- **Gain for the CT clamps - PGAGain**: The default setting is for homes that have 100 amp service - **21**.  Many houses are big and/or suck up more electricity than a 100 amp service provides.  The PGAGain must be set to **42** for homes with electricity service between 100-200 amps.

- **Gain adjustment for Voltage Readings - VoltageGain**: This value depends on the power 9v/12v power supply being used with the energy meter. `One of CircuitSetup's web pages <https://github.com/CircuitSetup/Split-Single-Phase-Energy-Meter#calibration>`_ provides default values for some common power supplies.  We decided to standardize on the `Jameco 9V power supply, part no. 157041 <https://www.jameco.com/shop/ProductDisplay?catalogId=10001&langId=-1&storeId=10001&productId=157041>`_.

- **Gain adjustment for Current Readings - CurrentGain**: This value depends CT (Current Transformer) being used.  We are using the SCT-016.

*NOTE: We used the command line utilities*::

   calibrate_voltage
   calibrate_current

*discussed below to set VoltageGain and CurrentGain.*
*Also Note: CircuitSetup's firmware for the energy meter uses a current gain setting for each of the CTs.  We simplified this to use just one parameter -  CurrentGain - for both CTs.*

calibrate_voltage
~~~~~~~~~~~~~~~~~
After starting up the venv and pip installing FHmonitor, the `calibrate_voltage <https://github.com/BitKnitting/FHmonitor/blob/master/FHmonitor/command_line.py#L133>`_ command is available.  This
command runs a python script that will adjust the VoltageGain value within `calibration.json <https://github.com/BitKnitting/FHmonitor/blob/master/FHmonitor/calibration.json>`_.  Prior to
using the command, you should have the energy meter plugged into a `Kill-A-Watt <https://amzn.to/2Mcjkt7>`_.  The Kill-A-Watt will
be the reference voltage.  Running the command with the -s (--save) option will figure out the new VoltageGain
value and then update `calibration.json <https://github.com/BitKnitting/FHmonitor/blob/master/FHmonitor/calibration.json>`_.
If the -s option is not specified, the new VoltageGain value will not be saved.

calibrate_current
~~~~~~~~~~~~~~~~~
`calibrate_current <https://github.com/BitKnitting/FHmonitor/blob/master/FHmonitor/command_line.py#L142>`_ is similar in concept to calibrate_voltage.  Instead of using voltage readings, current readings are used.  The
CT can be plugged into either of the CT plugs on the meter.  We use a test wire assembly to read the current
of a device (for example a lamp) using a CT.

.. image:: images/test_wiring_to_measure_current.jpg
   :width: 300

systemd service
===============
The systemd service, `FHmonitor_main.service <https://github.com/BitKnitting/FHmonitor/blob/master/FHmonitor/systemd/FHmonitor_main.service>`_
starts a shell script, `run_FHmonitor_main.sh <https://github.com/BitKnitting/FHmonitor/blob/master/FHmonitor/systemd/run_FHmonitor_main.sh>`_.
The shell script starts `FHmonitor_main.py <https://github.com/BitKnitting/FHmonitor/blob/b06dc54c94eb5ee25eb026f391f94ad468c9e77d/FHmonitor/systemd/FHmonitor_main.py>`_.

install_service
~~~~~~~~~~~~~~~

Use the command::

   (venv)$ install_service

to install the systemd service.  The code for install_service is located in `command_line.py <https://github.com/BitKnitting/FHmonitor/blob/c425001252694278b7b2280dd40f10bf63ac1929/FHmonitor/command_line.py#L114>`_.

install_service modifies:

- the ExecStart= line of FHmonitor_main.service to reference the run_FHmonitor_main.sh script located within the project's systemd directory.
- the ProjPath in run_FHmonitor_main.sh to be the absolute path to where the FHmonitor project is located.
- the permissions on the files in the systemd directory.

Then copies FHmonitor_main.service to /lib/systemd/system/.

start_service
~~~~~~~~~~~~~

Use the command::

   (venv)$ start_service

To execute the OS commands that will start the FHmonitor_main.service systemd service.  The code for `start_service <https://github.com/BitKnitting/FHmonitor/blob/c425001252694278b7b2280dd40f10bf63ac1929/FHmonitor/command_line.py#L126>`_.

stop_service
~~~~~~~~~~~~

Use the command::

   (venv)$ stop_service

To execute the OS command for stopping the FHmonitor_main.service systemd service.  The code for `stop_service <https://github.com/BitKnitting/FHmonitor/blob/c425001252694278b7b2280dd40f10bf63ac1929/FHmonitor/command_line.py#L143>`_

status_service
~~~~~~~~~~~~~~

Use the command::

   (venv)$ status_service

To execute the OS command for checking the status of the FHmonitor_main.service systemd service.  The code for `status_service <https://github.com/BitKnitting/FHmonitor/blob/c425001252694278b7b2280dd40f10bf63ac1929/FHmonitor/command_line.py#L148>`_


hello_monitor
=============

Once the:

- monitor is plugged in with the CTs strapped around the power lines.
- the venv has been installed and activated.
- the FHmonitor package has been installed.

Type::

   (venv)$hello_monitor

If all is working, you should get reasonable active and reactive power readings.

The code for `hello_monitor <https://github.com/BitKnitting/FHmonitor/blob/c425001252694278b7b2280dd40f10bf63ac1929/FHmonitor/command_line.py#L93>`_.




Monitor class
=============

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
===========
The :class:`~FHmonitor.monitor.Monitor` class uses an implementation of the :class:`~FHmonitor.store.Store` abstract class to store power readings into a datastore.  The only data store currently available is the mongo db.  We originally started with
a Firebase DB, but decided running everything on a Raspberry Pi was much easier.  Mongo db can be run on the Raspberry Pi at no additional $ cost.


.. automodule:: FHmonitor.store
   :members:
   :undoc-members:
   :show-inheritance:








