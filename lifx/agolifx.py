#!/usr/bin/python
AGO_LIFX_VERSION = '0.0.1'
############################################
#
# LIIFX support for ago control
#
__author__ = 'Joakim Lindbom'
__copyright__ = 'Copyright 2013-2016, Joakim Lindbom'
__date__ = '2016-11-19'
__credits__ = ['Joakim Lindbom', 'The ago control team']
__license__ = 'GPL Public License Version 3'
__maintainer__ = 'Joakim Lindbom'
__email__ = 'Joakim.Lindbom@gmail.com'
__status__ = 'Experimental'
__version__ = AGO_LIFX_VERSION
############################################

import agoclient
import threading
import time


class ConfigurationError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


class AgoLIFX(agoclient.AgoApp):
    """AgoControl device with support for the LIFX protocol"""
    def app_cmd_line_options(self, parser):
        """App-specific command line options"""
        parser.add_argument('-T', '--test', action="store_true",
                            help="This can be set or not set")

        parser.add_argument('--set-parameter', 
                            help="Set this to do set_config_option with the value upon startup")

    def setup_app(self):
        """ Set-up of app"""
        self.connection.add_handler(self.message_handler)

        if self.args.test:
            self.log.info("Test argument was set")
        else:
            self.log.warning("Test argument was NOT set")

        api = self.get_config_option('API', 'Cloud', section='lifx', app='lifx')
        self.log.info("Configuration parameter 'API'=%s", api)
        if "Cloud" in api:
            from lifxnet import LifxNet
            api_key = self.get_config_option('APIKEY', 'NoKey', section='lifx', app='lifx')
            self.log.info("Configuration parameter 'APIKEY'={}".format(api_key))
            self.lifx = LifxNet(self)
            self.lifx.init(API_KEY=api_key)
        elif "LAN" in api:
            self.NumLights = self.get_config_option('NumLights', 1, section='lifx', app='lifx')  # Speeds init up
            from lifxlan2 import LifxLAN2
            self.lifx = LifxLAN2(self)
            self.lifx.init(self.NumLights)
        else:
            raise ConfigurationError("Unsupported API selected. Typo on conf file?")

        self.PollDelay = self.get_config_option('PollDelay', 10, section='lifx', app='lifx')
        self.log.info("Configuration parameter 'PollDelay={}".format(self.PollDelay ))


        if self.args.set_parameter:
            self.log.info("Setting configuration parameter 'some_key' to %s", self.args.set_parameter)
            self.set_config_option("some_key", self.args.set_parameter)

            param = self.get_config_option("some_key", "0")
            self.log.info("Configuration parameter 'some_key' is now set to %s", param)

        # Get devices, wait until bulbs are discovered
        self.log.debug('Looking for devices')
        self.switches = None
        while self.switches is None or self.switches is {}: #len(self.switches) == 0:
            self.switches = self.lifx.listSwitches()
            if len(self.switches) == 0:
                self.log.debug('Not found, retrying')
                time.sleep(5)

        print self.switches

        # Add bulbs to agocontrol
        self.log.info('Found {} bulbs'.format(len(self.switches)))
        if len(self.switches) > 0:
            # print self.switches
            self.log.info('Looking for devices, found:')
            for devId, dev in self.switches.iteritems():
                self.log.debug('devId={} dev={} Name = {}, Model={}'.format(devId, dev, dev["name"], dev["model"]))
                if dev["isRGB"]:  # TODO: Check dimming to set correct type
                    self.connection.add_device(dev["id"], "dimmerrgb", dev["name"])
                    self.log.info('Added {} as dimmer'.format(dev["id"]))
                else:
                    self.connection.add_device(dev["id"], "dimmer", dev["name"])
                    self.log.info('Added {} as dimmerrgb'.format(dev["id"]))

        self.connection.add_device("testrgb", "dimmerrgb", "test")
        self.log.info('Added testrgb as dimmerrgb')


        BACKGROUND = PullStatus(self, self.log, self.PollDelay)
        BACKGROUND.setDaemon(True)
        BACKGROUND.start()

    def message_handler(self, internalid, content):
        """The messagehandler."""
        if "command" in content:
            if content["command"] == "on":
                self.log.debug("switching on: %s", internalid)

                if self.lifx.turnOn(internalid):  # TODO: Add retry handling if state not as expected?
                    self.log.trace("TurnOn OK")
                    self.connection.emit_event(internalid, "event.device.statechanged", 255, "")
                else:
                    self.log.error("Failed to turn on device")

            elif content["command"] == "off":
                self.log.debug("switching off: %s", internalid)

                if self.lifx.turnOff(internalid):
                    self.log.trace("TurnOff OK")
                    self.connection.emit_event(internalid, "event.device.statechanged", 0, "")
                else:
                    self.log.error("Failed to turn on device")

            elif content["command"] == "setlevel":
                self.log.debug("dimming: {}, level={}".format(internalid, int(content["level"])))
                if self.lifx.dim(internalid, int(content["level"])):
                    self.log.trace("Dim OK")
                    self.connection.emit_event(internalid, "event.device.statechanged", int(content["level"]), "")
                else:
                    self.log.error("Failed dimming device")

            elif content["command"] == "setcolor":
                red = int(content["red"]);
                green = int(content["green"]);
                blue = int(content["blue"]);
                self.log.debug("setting colour for: {} - R={} G={} B={}".format(internalid, red, green, blue))
                self.lifx.set_colour(internalid, red, green, blue)
                #self.connection.emit_event(internalid, "event.device.statechanged", content["level"], "")

    def app_cleanup(self):
        pass


class PullStatus(threading.Thread):
    """The background thread is checking status of the bulbs
       This is needed if e.g. the LIFX smartphone app or scheduling is used to alter state"""
    def __init__(self, app, log, PollDelay):
        threading.Thread.__init__(self)
        self.app = app
        self.log = log
        self.switches = self.app.switches
        self.PollDelay = PollDelay

    def run(self):
        self.log.info('Background thread started')

        # TODO: Improve this; we do not handle proper shutdown..
        while not self.app.is_exit_signaled():
            for devid in self.switches:
                try:
                    state = self.app.lifx.getLightState(devid)
                    if state is not None:
                        self.app.connection.emit_event(devid, "event.device.statechanged", int(state["dimlevel"]) if state["power"] == u'on' else 0, "")
                        self.log.debug("PullStatus: {}, {}, level={}".format(devid, state["power"], int(state["dimlevel"])))
                    else:
                        self.log.error('PullStatus: Could not get status from light')
                except TypeError as e:
                    self.log.error("PullStatus: Exception occurred in background thread. {}".format(e.message))
            time.sleep(self.PollDelay)  # TODO: Calculate ((60-n)/NoDevices)/60

if __name__ == "__main__":
    AgoLIFX().main()
