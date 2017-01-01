import unittest
import time
from lifxnet import LifxNet

from lifxtestsuite1 import API_KEY

class lifxTests2(unittest.TestCase):
    def setUp(self):
        #print ("Configuration parameter 'APIKEY'=%s", API_KEY)
        self.lifx = LifxNet(self)
        self.lifx.init(API_KEY=API_KEY, RetryLimit=4, RetryTime=3)
        self.switches = self.lifx.listSwitches()
        self.assertGreater(len(self.switches), 0, "No lamps found. Error in config?")
        print ("No lamps found %d" % len(self.switches))

    def test1_printinfo(self):
        if len(self.switches) > 0:
            print self.switches

    def test2_getLightState(self):
        if len(self.switches) > 0:
            for devid in self.switches:
                state = self.lifx.getLightState(devid)
                print state

    def test3_listdeviceinfo(self):
        if len(self.switches) > 0:
            #print switches
            for devId, dev in self.switches.iteritems():
                print ('devId={} dev={}'.format(devId, dev))

    def test4_colour(self):
        if len(self.switches) > 0:
            for devId, dev in self.switches.iteritems():
                if dev["isRGB"]:
                    self.lifx.set_colour(devId, 255, 0, 0)
                    time.sleep(1)
                    self.lifx.set_colour(devId, 0, 255,  0)
                    time.sleep(1)
                    self.lifx.set_colour(devId, 0, 0, 255)

    def tearDown(self):
        pass

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(lifxTests2)
    unittest.TextTestRunner(verbosity=2).run(suite)
