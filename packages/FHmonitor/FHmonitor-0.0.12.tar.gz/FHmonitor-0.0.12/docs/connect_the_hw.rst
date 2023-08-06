Connect The Hardware
====================

We'll wire:

- SPI between the Raspberry Pi and the electricity monitor.
- LED + resistor to the Raspberry Pi.

SPI
---

Raspberry Pi Pins
~~~~~~~~~~~~~~~~~
The diagram below point out the Raspberry Pi's pinout:

.. image:: images/RaspPi_pinout.png
   :width: 500

- MOSI: pin 19
- MISO: pin 21
- CLK:  pin 23
- GND: pin 25

We'll use GPIO 5 (pin 29) for CS.

Circuit Setup Pins
~~~~~~~~~~~~~~~~~~

.. image:: images/CircuitSetupPins.png
   :width: 300

Wire the MOSI, MISO, SCLK, GND, CS lines from the Rasp Pi to the Energy monitor.

LED
---

The schematic for wiring an LED is quite simple.

.. image:: images/led_wiring.png
   :width: 300

We used a 470 ohm resistor.  Anything from 400 ohm to 1K ohm works.

`Good Reminder <https://thepihut.com/blogs/raspberry-pi-tutorials/27968772-turning-on-an-led-with-your-raspberry-pis-gpio-pins#:~:text=>`_ -
`You must ALWAYS use resistors to connect LEDs up to the GPIO pins of the
Raspberry Pi. mportant to use a resistor.The Raspberry Pi can only supply a
small current (about 60mA). The LEDs will want to draw more, and if allowed
to they will burn out the Raspberry Pi. Therefore putting the resistors in the
circuit will ensure that only this small current will flow and the Raspberry Pi
will not be damaged.`

GPIO Pin for LED
~~~~~~~~~~~~~~~~

We tell the LED to blink by calling the Monitor class's :meth:`~FHmonitor.monitor.Monitor.blink` method.
The default GPIO pin is set within the Monitor's __init__() method to GPIO #18 (pin 12).  This can be
changed during :class:`~FHmonitor.monitor.Monitor` class initialization.








