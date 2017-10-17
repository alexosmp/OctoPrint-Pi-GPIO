# coding=utf-8
import array
import time
from .sensor import Sensor
from .i2c import I2C


HTU21D_BUS = 1
HTU21D_ADDR = 0x40  # Unshifted 7-bit I2C address for the sensor
HTU21D_DELAY = 0.1  # 100 ms
# CMD_READ_TEMP_HOLD = "\xE3"
# CMD_READ_HUM_HOLD = "\xE5"
CMD_READ_TEMP_NOHOLD = "\xF3"
CMD_READ_HUM_NOHOLD = "\xF5"
# CMD_WRITE_USER_REG = "\xE6"
# CMD_READ_USER_REG = "\xE7"
CMD_SOFT_RESET = "\xFE"
RESULT_IO_ERROR = 998
RESULT_CRC_ERROR = 999


class HTU21D(Sensor):
    """HTU21D sensor class
    Ported from SparkFun HTU21D Breakout Arduino Library
    (https://github.com/sparkfun/HTU21D_Breakout)
    """

    def __init__(self):
        self.dev = I2C(HTU21D_ADDR, HTU21D_BUS)
        self.dev.write(CMD_SOFT_RESET)
        time.sleep(HTU21D_DELAY)

    def __del__(self):
        self.dev.close()

    def read_data(self):
        return u"%.1f°C / %.1f%%" % (
            self.read_temperature(), self.read_humidity())

    def read_temperature(self):
        raw_temp = self._read_value(CMD_READ_TEMP_NOHOLD)
        if raw_temp == RESULT_IO_ERROR or raw_temp == RESULT_CRC_ERROR:
            return raw_temp
        return raw_temp * (175.72 / 65536.0) - 46.85

    def read_humidity(self):
        raw_hum = self._read_value(CMD_READ_HUM_NOHOLD)
        if raw_hum == RESULT_IO_ERROR or raw_hum == RESULT_CRC_ERROR:
            return raw_hum
        return raw_hum * (125.0 / 65536.0) - 6.0

    def _read_value(self, cmd):
        self.dev.write(cmd)
        time.sleep(HTU21D_DELAY)

        data = self.dev.read(3)  # (data_msb, data_lsb, checksum)
        buf = array.array("B", data)
        if len(buf) != 3:
            return RESULT_IO_ERROR

        value = (buf[0] << 8) | buf[1]
        if not self._verify_crc(value, buf[2]):
            return RESULT_CRC_ERROR

        return value & 0xFFFC  # drop the status bits

    @staticmethod
    def _verify_crc(value, crc):
        remainder = (value << 8) | crc
        # POLYNOMIAL = 0x0131 = x^8 + x^5 + x^4 + 1
        # 0x0131 polynomial shifted to the farthest left of three bytes:
        divisor = 0x988000

        for i in range(0, 16):
            if remainder & 1 << (23 - i):
                remainder ^= divisor
            divisor >>= 1

        return remainder == 0
