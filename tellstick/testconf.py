#!/usr/bin/python

import time
from qpid.messaging import Message
import agoclient

class AgoTestConfig(agoclient.AgoApp):
    def setup_app(self):
        self.timers = {} # List of timers
        self.event_received = {}
        self.lasttime = {}
        self.dev_delay = {}
        self.sensors = {}
        self.ignoreModels = {}

        print ("Entering setup_app")

        try:
            self.general_delay = float(self.get_config_option('Delay', 500, section='EventDevices', app='tellstick'))/1000
            print ("Got from config file: " + str(self.general_delay))
        except ValueError:
            self.general_delay = 0.5
            print ("ValueError, set to: " + str(self.general_delay))


        try:
            ignoreModels = self.get_config_option('IgnoreModels', "", section='EventDevices', app='tellstick')
            print ("Got from config file: " + ignoreModels)
        except ValueError:
            ignoreModels = ""
            print ("ValueError, self.ignoreModels empty " )

        self.ignoreModels = ignoreModels.replace(' ', '').split(',')


        try:
            desc = self.get_config_option('Desc', "", section='201', app='tellstick')
            print ("201 Got from config file: " + desc)
        except ValueError:
            desc= ""
            print ("201 ValueError, desc empty" )

        try:
            desc = self.get_config_option('Desc', "", section='202', app='tellstick')
            print ("202 Got from config file: " + desc)
        except ValueError:
            desc= ""
            print ("202 ValueError, desc empty" )

        try:
            ignore = self.get_config_option('Ignore', "no", section='201', app='tellstick')
            print ("201 Got from config file: " + ignore)
        except ValueError:
            desc= ""
            print ("201 ValueError, ignore empty" )


        try:
            ignore = self.get_config_option('Ignore', "", section='161', app='tellstick')
            print ("161 Got from config file: " + ignore)
        except ValueError:
            desc= ""
            print ("161 ValueError, ignore empty" )


        print ("Leaving setup_app")

if __name__ == "__main__":
    AgoTestConfig().main()