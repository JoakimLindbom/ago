import unittest
import time
from lifxnet import lifxnet

from lifxtestsuite1 import API_KEY

class lifxtests(unittest.TestCase):
    def setUp(self):
        print ("Configuration parameter 'APIKEY'=%s", API_KEY)

        self.lifx = lifxnet(self)
        self.lifx.init(API_KEY)

    def test_listdevices(self):
        switches = self.lifx.listSwitches()
        self.assertGreater(len(switches), 0, "Check that at least one device was found")

        if len(switches) >0:
            print switches
            for devId, dev in switches.iteritems():
                print ("devId=%s", devId)
                print ("dev=", dev)
                print ("MODEL=%s", dev["model"])

    def test_turnon(self):
        switches = self.lifx.listSwitches()
        self.assertGreater(len(switches), 0, "Check that at least one device was found")
        for id in switches:
            self.assertTrue(self.lifx.turnOff(id))
            time.sleep(1)
            self.assertTrue(self.lifx.turnOn(id))

    def test_dim(self):
        switches = self.lifx.listSwitches()
        self.assertGreater(len(switches), 0, "Check that at least one device was found")
        for id in switches:
            self.lifx.dim(id,100)
            time.sleep(1)
            self.lifx.dim(id, 50)
            time.sleep(1)
            self.lifx.dim(id, 10)
            time.sleep(1)
            self.lifx.dim(id,100)
            time.sleep(1)

if __name__ == "__main__":
    unittest.main()
