import enum
import logging
import sys

import serial
from serial import PARITY_EVEN, STOPBITS_ONE
from serial.tools import list_ports

LOGGER = logging.getLogger(__name__)

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


class TeleinfoMode(enum.Enum):
    STANDARD = "standard",
    HISTORY = "historique"


class TeleinfoGroup:

    def __init__(self, name, value, checksum):
        self.name = name
        self.value = value
        self.checksum = checksum

    def __repr__(self):
        return "TeleinfoGroup(name=%s, value=%s, checksum=%s)" % (self.name, self.value, self.checksum)


class TeleinfoFrame:

    def __init__(self):
        """Initialize TeleinfoFrame."""
        self.groups = []

    def get(self, name):
        """Get group by label."""
        for group in self.groups:
            if group.name == name:
                return group
        return None

    def add_group(self, name, value, checksum):
        """Add group"""
        self.groups.append(TeleinfoGroup(name, value, checksum))

    def __repr__(self):
        return ",".join([g.__repr__() for g in self.groups])


class Teleinfo:

    reader = None

    def __init__(self, port = "/dev/ttyUSB", mode:TeleinfoMode = TeleinfoMode.HISTORY, timeout=1):
        """Responsible to read TIC frame on serial port."""
        self.port = port
        self.baud_rate = 1200 if mode == TeleinfoMode.HISTORY else 9600
        self.timeout = timeout

    def _readline(self):
        """Readline from serial."""
        data = self.reader.readline()
        line = data.decode('ascii')
        return line.replace('\r', '').replace('\n', '')

    def __wait_rcv_frame_start(self):
        """Wait for frame start."""
        line = self._readline()
        FRAME_START = '\x02'
        while FRAME_START not in line:
            line = self._readline()

    def __process_frame(self):
        """Process frame."""
        STE = '\x03'
        frame = TeleinfoFrame()
        LOGGER.info(u"New frame")
        line = self._readline()
        while STE not in line:
            LOGGER.info("New group: %s", line)
            if len(line.split()) == 2:
                name, value = line.split()
                checksum = ' '
            else:
                name, value, checksum = line.split()

            if self.__is_valid_frame(line, checksum):
                frame.add_group(name, value, checksum)
            else:
                LOGGER.warning("Frame corrupted. Waiting for a new one.")
                break
            line = self._readline()
        return frame

    def read_frame(self):
        """Read a frame from serial port. """
        self.__wait_rcv_frame_start()
        frame = self.__process_frame()

        LOGGER.info("Frame: %s", frame)
        return frame

    def __is_valid_frame(self, frame, checksum):
        """Check if a frame is valid."""
        datas = ' '.join(frame.split()[0:2])
        my_sum = 0
        for cks in datas:
            my_sum = my_sum + ord(cks)
        computed_checksum = (my_sum & int("111111", 2)) + 0x20
        if chr(computed_checksum) == checksum:
            return True
        LOGGER.warning(u"Invalid checksum for %s : %s != %s", frame, computed_checksum, checksum)
        return False

    def open(self):
        """Open reader."""
        if self.reader is None:
            self.reader = serial.Serial(
                self.port,
                self.baud_rate,
                bytesize=7,
                parity=PARITY_EVEN,
                stopbits=STOPBITS_ONE,
                timeout=self.timeout
            )
        if not self.reader.isOpen():
            self.reader.open()

    def close(self):
        """Close reader."""
        if self.reader is not None and self.reader.isOpen():
            self.reader.close()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        self.close()


def serial_is_available(name):
    """ Check if a serial port is available. """
    ports = list_available_serials()
    for port in ports:
        if port.device == name:
            return True
    return False


def list_available_serials():
    """ Check if a serial port is available. """
    ports = list_ports.comports()
    return [port.device for port in ports]