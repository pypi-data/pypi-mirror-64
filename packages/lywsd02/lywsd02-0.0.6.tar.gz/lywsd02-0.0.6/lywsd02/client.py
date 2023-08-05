import collections
import contextlib
import logging
import struct
import time
from datetime import datetime

from bluepy import btle

_LOGGER = logging.getLogger(__name__)

UUID_UNITS = 'EBE0CCBE-7A0A-4B0C-8A1A-6FF2997DA3A6'     # 0x00 - F, 0x01 - C    READ WRITE
UUID_HISTORY = 'EBE0CCBC-7A0A-4B0C-8A1A-6FF2997DA3A6'   # Last idx 152          READ NOTIFY
UUID_TIME = 'EBE0CCB7-7A0A-4B0C-8A1A-6FF2997DA3A6'      # 5 or 4 bytes          READ WRITE
UUID_DATA = 'EBE0CCC1-7A0A-4B0C-8A1A-6FF2997DA3A6'      # 3 bytes               READ NOTIFY


class SensorData(
        collections.namedtuple('SensorDataBase', ['temperature', 'humidity'])):
    __slots__ = ()


class Lywsd02Client:
    UNITS = {
        b'\x01': 'F',
        b'\xff': 'C',
    }
    UNITS_CODES = {
        'C': b'\xff',
        'F': b'\x01',
    }

    def __init__(self, mac, notification_timeout=5.0):
        self._mac = mac
        self._peripheral = btle.Peripheral()
        self._notification_timeout = notification_timeout
        self._handles = {}
        self._tz_offset = None
        self._data = SensorData(None, None)
        self._history_data = collections.OrderedDict()
        self._connected = False

    @contextlib.contextmanager
    def connect(self):
        # Store connecion status
        conn_status = self._connected
        if not conn_status:
            _LOGGER.debug('Connecting to %s', self._mac)
            self._peripheral.connect(self._mac)
            self._connected = True
        try:
            yield self
        finally:
            if not conn_status:
                _LOGGER.debug('Disconnecting from %s', self._mac)
                self._peripheral.disconnect()
                self._connected = False

    @property
    def temperature(self):
        return self.data.temperature

    @property
    def humidity(self):
        return self.data.humidity

    @property
    def data(self):
        self._get_sensor_data()
        return self._data

    @property
    def units(self):
        with self.connect():
            ch = self._peripheral.getCharacteristics(uuid=UUID_UNITS)[0]
            value = ch.read()
        return self.UNITS[value]

    @units.setter
    def units(self, value):
        if value.upper() not in self.UNITS_CODES.keys():
            raise ValueError(
                'Units value must be one of %s' % self.UNITS_CODES.keys())

        with self.connect():
            ch = self._peripheral.getCharacteristics(uuid=UUID_UNITS)[0]
            ch.write(self.UNITS_CODES[value.upper()], withResponse=True)

    @property
    def battery(self):
        with self.connect():
            ch = self._peripheral.getCharacteristics(
                uuid=btle.AssignedNumbers.battery_level)[0]
            value = ch.read()
        return ord(value)

    @property
    def time(self):
        with self.connect():
            ch = self._peripheral.getCharacteristics(uuid=UUID_TIME)[0]
            value = ch.read()
        if len(value) == 5:
            ts, tz_offset = struct.unpack('Ib', value)
        else:
            ts = struct.unpack('I', value)[0]
            tz_offset = 0
        return datetime.fromtimestamp(ts), tz_offset

    @time.setter
    def time(self, dt: datetime):
        if self._tz_offset is not None:
            tz_offset = self._tz_offset
        else:
            tz_offset = int(-time.timezone / 3600)

        data = struct.pack('Ib', int(dt.timestamp()), tz_offset)
        with self.connect():
            ch = self._peripheral.getCharacteristics(uuid=UUID_TIME)[0]
            ch.write(data, withResponse=True)

    @property
    def tz_offset(self):
        return self._tz_offset

    @tz_offset.setter
    def tz_offset(self, tz_offset: int):
        self._tz_offset = tz_offset

    @property
    def history_data(self):
        self.get_history_data()
        return self._history_data

    def _get_sensor_data(self):
        with self.connect():
            self._subscribe(UUID_DATA, self._process_sensor_data)

            if not self._peripheral.waitForNotifications(
                    self._notification_timeout):
                raise TimeoutError('No data from device for {}'.format(
                    self._notification_timeout))

    def get_history_data(self):
        with self.connect():
            self._subscribe(UUID_HISTORY, self._process_history_data)

            while True:
                if not self._peripheral.waitForNotifications(
                        self._notification_timeout):
                    break

    def handleNotification(self, handle, data):
        func = self._handles.get(handle)
        if func:
            func(data)

    def _subscribe(self, uuid, callback):
        self._peripheral.setDelegate(self)
        ch = self._peripheral.getCharacteristics(uuid=uuid)[0]
        self._handles[ch.getHandle()] = callback
        desc = ch.getDescriptors(forUUID=0x2902)[0]

        desc.write(0x01.to_bytes(2, byteorder="little"), withResponse=True)

    def _process_sensor_data(self, data):
        temperature, humidity = struct.unpack_from('HB', data)
        temperature /= 100

        self._data = SensorData(temperature=temperature, humidity=humidity)

    def _process_history_data(self, data):
        (id, ts, max_temp, max_hum, min_temp, _, min_hum) = struct.unpack_from(
            'IIHBBBB', data)
        ts = datetime.fromtimestamp(ts)
        max_temp /= 10
        min_temp /= 10
        self._history_data[id] = [ts, max_temp, max_hum, min_temp, min_hum]
