"""
---
name: l298.py
description: MicroPython L298 Dual Full-Bridge Driver Control package
copyright: 2017-2019 Marcio Pessoa
people:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
change-log:
  2019-03-10:
  - version: 0.09
    fixed: stop() method was not stopping.
  2019-03-04:
  - version: 0.08
    changed: method name power() to power()
    added: get_power() method.
  2019-02-12:
  - version: 0.07
    fixed: Minor updates.
  2019-02-09:
  - version: 0.06
    fixed: Some mistakes.
  2019-02-06:
  - version: 0.05
    added: Ported from C++ to MicroPython.
  2017-11-04
  - version: 0.01
    added: Experimental version.
"""

from pyb import Pin, Timer  # pylint: disable=import-error


class L298():  # pylint: disable=too-many-instance-attributes
    """
    description: Driver L298 object constructor.
    """

    def __init__(self):
        self._version = 0.09
        self.__pins = [None, None, None, None]
        self.__timers = [None, None, None, None]
        self.__channels = [None, None, None, None]
        self.__frequencies = [None, None, None, None]
        self.__values = [0, 0, 0, 0]
        self.__pwm = [None, None, None, None]
        self.__power = 100  # Percent
        self.__enable = False

    def on(self):  # pylint: disable=invalid-name
        """
        description: Turn driver on.
        """
        self.__enable = True

    def off(self):
        """
        description: Turn driver off.
        """
        self.__enable = False

    def pins(self, pins):
        """
        description: Set MCU pins connected to driver.
        args:
        - pins (list): A list with 4 elements (pins names), example
            ['X1', 'X2', 'X3', 'X4']
        """
        for i, value in enumerate(pins):
            self.__pins[i] = Pin(value)

    def timer(self, timers):
        """
        description: Set MCU timers to be used with PWM.
        args:
        - timers (list): A list with 4 elements (timer numbers), example
            ['5', '5', '5', '5']
        """
        self.__timers = timers

    def channel(self, channels):
        """
        description: Set MCU timer channels to be used with PWM.
        args:
        - channels (list): A list with 4 elements (channel numbers), example
            ['1', '2', '3', '4']
        """
        self.__channels = channels

    def frequency(self, frequencies):
        """
        description: Set MCU frequencies to be used with PWM.
        args:
        - frequencies (list): A list with 4 elements (frequencies), example
            ['1000', '1000', '1000', '1000']
        """
        self.__frequencies = frequencies

    def value(self, values=None):
        """
        description: Set MCU values to be used with PWM.
        args:
        - values (list): A list with 4 elements (frequencies), example
            ['1000', '1000', '1000', '1000']
        returns:
        - values (list): If no arguments is passed.
          bool:
          - true: Problems found
          - false: No errors
        """
        if values is None:
            return self.__values
        self.__values = values
        return False

    def attach(self):
        """
        description: Attach driver motor and start all PWM timers.
        """
        for i in range(len(self.__pins)):
            tim = Timer(self.__timers[i], freq=self.__frequencies[i])
            channel = tim.channel(self.__channels[i],
                                  Timer.PWM, pin=self.__pins[i])
            self.__pwm[i] = channel
        self.update()

    def update(self):
        """
        description: Update driver output pins based on received values.
        """
        if not self.__enable:
            for i in self.__pwm:
                i.pulse_width_percent(0)
            return False
        for i in range(len(self.__pwm)):
            self.__pwm[i].pulse_width_percent(self.__values[i] * self.__power)
        return False

    def power(self, power=None):
        """
        description: Set driver power level.
        args:
        - power (int): The power level (percent), a number from 0 to 100.
        returns:
        - power (int): If no arguments is passed.
          bool:
          - true: Problems found
          - false: No errors
        """
        if power is None:
            return self.__power
        self.__power = power
        return False
