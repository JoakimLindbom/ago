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
from lifxnet import lifxnet

class AgoLIFX(agoclient.AgoApp):
    """AgoControl device with support for the LIFX protocol"""
    def app_cmd_line_options(self, parser):
        """App-specific command line options"""
        parser.add_argument('-T', '--test', action="store_true",
                help="This can be set or not set")

        parser.add_argument('--set-parameter', 
                help="Set this to do set_config_option with the value upon startup")


    # the message_handler method will be called by the CLIENT
    # library when a message comes in that is destined for
    # one of the child devices you're handling
    # the first parameter is your internal id (all the mapping
    # from ago control uuids to the internal ids is handled
    # transparently for you)
    # the second parameter is a dict with the message content
    def message_handler(self, internalid, content):
        """The messagehandler."""
        if "command" in content:
            if content["command"] == "on":
                self.log.debug("switching on: %s", internalid)

                if self.lifx.turnOn(internalid):
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
                self.log.debug("dimming: %s", internalid)
                if self.lifx.dim(internalid, int(content["level"])):
                    self.log.trace("Dim OK")
                    self.connection.emit_event(internalid, "event.device.statechanged", content["level"], "") #TODO: Check if this is correct
                else:
                    self.log.error("Failed dimming device")

    def setup_app(self):
        # specify our message handler method
        self.connection.add_handler(self.message_handler)

        # If we want to use the custom command line argument, we look at
        # self.args:
        if self.args.test:
            self.log.info("Test argument was set")
        else:
            self.log.warning("Test argument was NOT set")

        API = self.get_config_option('API', 'Cloud')
        self.log.info("Configuration parameter 'API'=%s", API)
        if "Cloud" in API:
            API_KEY = self.get_config_option('APIKEY', 'c7d12d4b5176bea52eba449211ca5e7551d9ce737d0dc36623968e3550bcb460', section='LIFX', app='LIFX')
            self.log.info("Configuration parameter 'APIKEY'=%s", API_KEY)
            self.lifx = lifxnet(self)
            self.lifx.init(API_KEY)

        if self.args.set_parameter:
            self.log.info("Setting configuration parameter 'some_key' to %s", self.args.set_parameter)
            self.set_config_option("some_key", self.args.set_parameter)

            param = self.get_config_option("some_key", "0")
            self.log.info("Configuration parameter 'some_key' is now set to %s", param)

        # we add a switch and a dimmer
        self.lifx.list_lights()
        switches = self.lifx.listSwitches()
        if len(switches) >0:
            print switches
            for devId, dev in switches.iteritems():
                #if dev["model"]==""
                print dev
                print dev["model"]
                self.log.info("MODEL=%s", dev["model"])
                self.connection.add_device(dev["id"], "dimmer", 'lifx-dimmer')

        # for our threading lifx in the next section we also add a binary sensor:
        #self.connection.add_device("125", "binarysensor")

        #BACKGROUND = TestEvent(self)
        #BACKGROUND.setDaemon(True)
        #BACKGROUND.start()


    def app_cleanup(self):
        # When our app is about to shutdown, we should clean up any resources we've
        # allocated in app_setup. This is done here.
        # In this lifx, we do not have any resources..
        pass



class TestEvent(threading.Thread):
    """Test Event."""
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.app = app

    def run(self):
        level = 0
        # This is a dummy backend thread. It loops forever.
        # It is important that we exit when told to, by checking is_exit_signaled.
        #
        # TODO: Improve this lifx; we do not handle proper shutdown..
        while not self.app.is_exit_signaled():
            self.app.connection.emit_event("125",
                "event.security.sensortriggered", level, "")
            if (level == 0):
                level = 255
            else:
                level = 0
            time.sleep(5)

# Finally, but very important.
# We must call the main function of the application object
if __name__ == "__main__":
    AgoLIFX().main()

