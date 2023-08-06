# teleinfo - EDF teléinformation Python library


This library allows you to retrieve teleinfo using serial port device (USBTICLCV2).

### Example

~~~
from ticpy import Teleinfo, TeleinfoMode

with Teleinfo('/dev/tty.usbserial-DA4Y56SG', mode=TeleinfoMode.HISTORY) as teleinfo:

    frame = teleinfo.read_frame()
    print(frame.get("PAPP"))
~~~