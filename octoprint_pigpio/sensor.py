from abc import ABCMeta, abstractmethod


class Sensor(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def read_data(self):
        """Read sensor data"""
