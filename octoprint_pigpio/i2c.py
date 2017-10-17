import fcntl
import io


I2C_SLAVE = 0x0703


class I2C(object):
    """I2C helper class"""

    def __init__(self, device, bus):
        self.fr = io.open("/dev/i2c-" + str(bus), "rb", buffering=0)
        self.fw = io.open("/dev/i2c-" + str(bus), "wb", buffering=0)

        # set device address
        fcntl.ioctl(self.fr, I2C_SLAVE, device)
        fcntl.ioctl(self.fw, I2C_SLAVE, device)

    def __del__(self):
        self.close()

    def read(self, size):
        return self.fr.read(size)

    def write(self, data):
        self.fw.write(data)

    def close(self):
        self.fw.close()
        self.fr.close()
