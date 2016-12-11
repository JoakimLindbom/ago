import unittest
import time
from lifxlan2 import LifxLAN2

class lifxTests(unittest.TestCase):
    def setUp(self):
        self.lifx = LifxLAN2(self)
        self.lifx.init(num_lights=1)
        self.switches = self.lifx.listSwitches()
        self.assertGreater(len(self.switches), 0, "No lamps found. Error in config?")
        print ("No lamps found %d" % len(self.switches))

    def test1_printinfo(self):
         if len(self.switches) > 0:
            print self.switches

    def test2_listdeviceinfo(self):
        if len(self.switches) > 0:
            #print switches
            for devId, dev in self.switches.iteritems():
                print ('devId={} dev={}'.format(devId, dev))

    def test3a_getColour(self):
        if len(self.switches) > 0:
            for devid in self.switches:
                self.assertTrue(self.lifx.get_colour(devid))

    def test3b_dim(self):
        if len(self.switches) > 0:
            for devid in self.switches:
                self.assertTrue(self.lifx.dim(devid, 100))
                time.sleep(1)
                self.assertTrue(self.lifx.dim(devid, 10))
                time.sleep(1)
                self.assertTrue(self.lifx.dim(devid, 100))


    def test3c_getLightState(self):
        if len(self.switches) > 0:
            for devid in self.switches:
                self.assertTrue(self.lifx.turnOn(devid))
                time.sleep(1)
                state = self.lifx.getLightState(devid)
                self.assertTrue(state["power"] == u'on')

                self.assertTrue(self.lifx.turnOff(devid))
                time.sleep(1)
                state = self.lifx.getLightState(devid)
                self.assertTrue(state["power"] == u'off')

    def test4_turnon(self):
        for devid in self.switches:
            self.assertTrue(self.lifx.turnOff(devid))
            time.sleep(1)
            self.assertTrue(self.lifx.turnOn(devid))

    def test5_dim(self):
        for devid, dev in self.switches.iteritems():
            if dev["isDimmer"]:
                self.assertTrue(self.lifx.dim(devid, 100))
                time.sleep(1)
                self.assertTrue(self.lifx.dim(devid, 10))
                time.sleep(1)
                self.assertTrue(self.lifx.dim(devid, 100))

    def tearDown(self):
        pass
#        for devid in self.switches:
#            self.assertTrue(self.lifx.turnOff(devid))  # Turn off all lights

if __name__ == "__main__":
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(lifxTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
