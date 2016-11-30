import unittest
import time
from lifxnet import LifxNet

from lifxtestsuite1 import API_KEY

class lifxTests2(unittest.TestCase):
    def setUp(self):
        #print ("Configuration parameter 'APIKEY'=%s", API_KEY)
        self.lifx = LifxNet(self)
        self.lifx.init(API_KEY=API_KEY)
        self.switches = self.lifx.listSwitches()
        self.assertGreater(len(self.switches), 0, "No lamps found. Error in config?")
        print ("No lamps found %d" % len(self.switches))

    def test_printinfo(self):
        if len(self.switches) > 0:
            print self.switches

    def test_getLightState(self):
        if len(self.switches) > 0:
            for devid in self.switches:
                state = self.lifx.getLightState(devid)
                print state

    def test_listdeviceinfo(self):
        if len(self.switches) > 0:
            #print switches
            for devId, dev in self.switches.iteritems():
                print ('devId={}'.format(devId))
                print ('dev={}'.format(dev))
                print ('MODEL={}'.format(dev["model"]))

    def tearDown(self):
        pass

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(lifxTests2)
    unittest.TextTestRunner(verbosity=2).run(suite)
