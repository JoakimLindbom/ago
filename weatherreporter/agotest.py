#!/usr/bin/python

import time
from qpid.messaging import Message
import agoclient

#TODO: Add cron job to update Sunset/sunrise +- 1h, +-½h

class AgoTest(agoclient.AgoApp):


    def setup_app(self):

        try:
            self.general_delay = float(
                self.get_config_option('Delay', 111, section='EventDevices', app='test'))
        except ValueError:
            self.general_delay = 0.222

        print ("delay=" + str(self.general_delay))

        try:
            self.general_delay = float(
                self.get_config_option('Delay', 333, section='EventDevices', app='tellstick')) / 1000
        except ValueError:
            self.general_delay = 0.444

        print ("delay=" + str(self.general_delay))



if __name__ == "__main__":
    AgoTest().main()
