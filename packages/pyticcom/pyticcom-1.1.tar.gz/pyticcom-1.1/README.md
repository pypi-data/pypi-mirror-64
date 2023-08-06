# pyticcom - EDF teléinformation Python library

[![PyPI version](https://badge.fury.io/py/pyticcom.svg)](https://badge.fury.io/py/pyticcom)

This library allows you to retrieve teleinfo using serial port device (USBTICLCV2).

### Example

~~~
from pyticcom import Teleinfo, TeleinfoMode

with Teleinfo('/dev/tty.usbserial-DA4Y56SG', mode=TeleinfoMode.HISTORY) as teleinfo:

    frame = teleinfo.read_frame()
    print(frame.get("PAPP"))
~~~