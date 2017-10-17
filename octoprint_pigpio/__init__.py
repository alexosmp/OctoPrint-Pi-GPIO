# coding=utf-8
from __future__ import absolute_import


__plugin_name__ = "Pi GPIO"

import sys
import flask
import octoprint.plugin
from octoprint.util import RepeatedTimer
from .htu21d import HTU21D


class PiGpioPlugin(octoprint.plugin.StartupPlugin,
                   octoprint.plugin.TemplatePlugin,
                   octoprint.plugin.AssetPlugin,
                   octoprint.plugin.SettingsPlugin,
                   octoprint.plugin.SimpleApiPlugin):
    """The plugin class"""

    PERIPHERALS = {
        "htu21d": "HTU21D"
    }
    SENSOR_QUERY_INTERVAL = 30.0  # seconds

    def __init__(self):
        self.__is_rpi = False
        # Settings
        self.__navbar_widget = ""
        # Peripherals
        self.__sensor_query_timer = None
        self.__sensors = {}
        self.__sensor_data = {}

    def __del__(self):
        if self.__sensor_query_timer is not None:
            self.__sensor_query_timer.cancel()
        for s in self.__sensors:
            self.__sensors[s].__del__()

    def __send_plugin_message(self, message):
        self._plugin_manager.send_plugin_message(self._identifier, message)

    def __send_plugin_message1(self):
        self.__send_plugin_message({
            "type": "ui_data",
            "is_rpi": self.__is_rpi,
            "navbar_widget": self.__navbar_widget,
            "navbar_widget_title": (self.PERIPHERALS[self.__navbar_widget]
                                    if self.__navbar_widget in self.PERIPHERALS
                                    else "No widget")
        })

    def __send_plugin_message2(self):
        self.__send_plugin_message({
            "type": "sensor_data",
            "sensor_data": self.__sensor_data
        })

    def __query_sensors(self):
        for s in self.__sensors:
            self.__sensor_data[s] = self.__sensors[s].read_data()
        self.__send_plugin_message2()

    # ~~ StartupPlugin
    def on_after_startup(self):
        if sys.platform != "linux2":
            self._logger.info("This plugin requires a linux2 platform")
            sys.exit(1)

        # Check for something like "Hardware	: BCM2835"
        with open("/proc/cpuinfo") as cpuinfo_file:
            for line in cpuinfo_file:
                if line.startswith("Hardware") and ":" in line:
                    hardware = line.split(":", 1)[1].strip()
                    if hardware in ["BCM2708", "BCM2709",
                                    "BCM2835", "BCM2836", "BCM2837"]:
                        self.__is_rpi = True
                        break
        if not self.__is_rpi:
            self._logger.info("This plugin requires a Raspberry Pi")
            sys.exit(1)

        self.__navbar_widget = self._settings.get(["navbar_widget"])

        # Add sensors
        if self.__navbar_widget == "htu21d":
            self.__sensors[self.__navbar_widget] = HTU21D()

        self.__sensor_query_timer = RepeatedTimer(self.SENSOR_QUERY_INTERVAL,
                                                  self.__query_sensors,
                                                  run_first=True)
        self.__sensor_query_timer.start()

    # ~~ TemplatePlugin
    def get_template_configs(self):
        return [{"type": "settings", "template": "pigpio_settings.jinja2"}]

    # ~~ AssetPlugin
    def get_assets(self):
        return {
            "js": ["js/pigpio.js"],
            "css": ["css/pigpio.css"]
        }

    # ~~ SettingsPlugin
    def get_settings_defaults(self):
        return {
            "navbar_widget": self.__navbar_widget
        }

    def on_settings_save(self, data):
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)

        self.__navbar_widget = self._settings.get(["navbar_widget"])

        # Update sensors
        for s in self.__sensors:
            self.__sensors[s].__del__()
        self.__sensors.clear()
        self.__sensor_data.clear()
        #
        if self.__navbar_widget == "htu21d":
            self.__sensors[self.__navbar_widget] = HTU21D()

        self.__send_plugin_message1()

    # ~~ SimpleApiPlugin
    def get_api_commands(self):
        return {
            "init_ui": []
        }

    def on_api_command(self, command, data):
        if command == "init_ui":
            self.__send_plugin_message1()
            self.__send_plugin_message2()
            return flask.jsonify({
                "result": 0
            })

    # ~~ Softwareupdate hook
    def get_update_information(self):
        return {
            "pigpio": {
                "displayName": self._plugin_name,
                "displayVersion": self._plugin_version,

                "type": "github_release",
                "user": "alexosmp",
                "repo": "OctoPrint-Pi-Gpio",
                "release_compare": "semantic",
                "current": self._plugin_version,

                "pip": "https://github.com/alexosmp/OctoPrint-Pi-Gpio/archive"
                       "/{target_version}.zip"
            }
        }


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = PiGpioPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config":
            __plugin_implementation__.get_update_information
    }
