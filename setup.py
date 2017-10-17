# coding=utf-8
import setuptools


plugin_identifier = "pigpio"
plugin_package = "octoprint_%s" % plugin_identifier
plugin_name = "OctoPrint-Pi-Gpio"
plugin_version = "0.1.0"
plugin_description = "Raspberry Pi / OctoPrint GPIO plugin"
plugin_author = "Aleksandr Volkov"
plugin_author_email = "alex@aheadautomatics.com"
plugin_url = "https://github.com/alexosmp/OctoPrint-Pi-Gpio"
plugin_license = "AGPLv3"
plugin_additional_data = []


def package_data_dirs(source, sub_folders):
    import os
    dirs = []

    for d in sub_folders:
        folder = os.path.join(source, d)
        if not os.path.exists(folder):
            continue

        for dirname, _, files in os.walk(folder):
            dirname = os.path.relpath(dirname, source)
            for f in files:
                dirs.append(os.path.join(dirname, f))

    return dirs


def params():
    # Our metadata, as defined above
    identifier = plugin_identifier
    name = plugin_name
    version = plugin_version
    description = plugin_description
    author = plugin_author
    author_email = plugin_author_email
    url = plugin_url
    license = plugin_license

    # We only have our plugin package to install
    packages = [plugin_package]

    # We might have additional data files in sub folders that need to be
    # installed too
    package_data = {
        plugin_package: package_data_dirs(plugin_package,
                                          ["static", "templates",
                                           "translations"] +
                                          plugin_additional_data)
    }
    include_package_data = True

    # If you have any package data that needs to be accessible on the file
    # system, such as templates or static assets
    # this plugin is not zip_safe.
    zip_safe = False

    # Read the requirements from our requirements.txt file
    install_requires = open("requirements.txt").read().split("\n")

    # Hook the plugin into the "octoprint.plugin" entry point, mapping the
    # plugin_identifier to the plugin_package.
    # That way OctoPrint will be able to find the plugin and load it.
    entry_points = {
        "octoprint.plugin": ["%s = %s" % (plugin_identifier, plugin_package)]
    }

    return locals()


setuptools.setup(**params())
