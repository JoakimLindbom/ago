#!/usr/bin/python

import time
from qpid.messaging import Message
import agoclient

class AgoWeatherReporter(agoclient.AgoApp):
    def message_handler(self, internalid, content):
        self.log.info("content=%s", content)


    def setup_app(self):
        self.log.info("setup_app")

if __name__ == "__main__":
    AgoWeatherReporter().main()