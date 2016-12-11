#!/usr/bin/python
AGO_LIFX_VERSION = '0.0.1'
############################################
#
# LIFX class supporting device handling via LIFX LAN APIs
#
# Date of origin: 2016-12-10
#
__author__ = "Joakim Lindbom"
__copyright__ = "Copyright 2016, Joakim Lindbom"
__credits__ = ["Joakim Lindbom", "The ago control team"]
__license__ = "GPL Public License Version 3"
__maintainer__ = "Joakim Lindbom"
__email__ = 'Joakim.Lindbom@gmail.com'
__status__ = "Experimental"
__version__ = AGO_LIFX_VERSION
############################################

from lifxbase import lifxbase
import time
from agoclient.agoapp import ConfigurationError
import json
from lifxlan import *


class LIFX_Offline(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)

class LifxLAN2(lifxbase):
    """Class used for Lifx devices via LIFX LAN API"""

    def __init__(self, app):
        super(LifxLAN2, self).__init__(app)

        self.devices = {}
        self.models = {}
        self.names = {}
        self.devicesRetrieved = False
        with open('prodinfo.json') as json_file:
            self.prodinfo =json.load(json_file)

        self.colour = {"hue": None,
                       "saturation": None,
                       "brightness": None,
                       "kelvin": None}
        self.dim_level = None  # 0-100%

    def __get__(self, obj, objtype=None):
        pass

    def __set__(self, obj, val):
        pass

    def __delete__(self, obj):
        pass

    def init(self, num_lights, sensor_poll_delay=None, temp_units='C', RetryLimit=3, RetryTime=2):
        self.SUPPORTED_METHODS = self.LIFX_TURNON | self.LIFX_TURNOFF | self.LIFX_DIM

        self.RetryLimit = RetryLimit
        self.RetryTime = RetryTime

        print("Discovering lights...")
        self.lifx = LifxLAN(num_lights)

        return True

    def close(self):
        pass

    def turnOn(self, devid):
        """ Turn on light"""
        self.log.trace('turnOn {}'.format(self.devices[devid]["name"]))
        self.devices[devid]["bulb"].set_power("on", True)
        return True

    def turnOff(self, devid):
        """ Turn off light"""
        self.log.trace('turnOff {}'.format(self.devices[devid]["name"]))
        self.devices[devid]["bulb"].set_power("off", True)
        return True

    def set_state(self, devid, payload, limit=0):
        """Set state of light to on, off, color, dim """
        pass

    def set_colour(self, devid, red, blue, green):
        """Set light to colour (RGB) """  # TODO: Recalculate into HSBK format, not supporting RGB
        print red
        print blue
        print green

        payload = {"color": "rgb:{},{},{}".format(red, green, blue)}
        self.log.info(payload)  # TODO: Change to trace
        return self.set_state(devid, payload)

    def list_lights(self):
        """Get a list of devices on local LAN"""
        self.devices = {}
        devices = self.lifx.get_lights()
        for i in devices:
            dev_id = i.source_id

            dev = {
                "id": dev_id,
                "name": i.get_label(),
                'bulb': i}

            for m in self.prodinfo[0]['products']:
                if i.product == m['pid']:
                    dev['model'] = m['name']
                    if m['features']['color'] == True:
                        dev["isRGB"] = True
                    else:
                        dev["isRGB"] = False
                    # TODO: Also check ['features']['infrared'] and ['features']['multizone']

            dev["isDimmer"] = True
            try:
                power = i.get_power()
                lvl = power/65535
                print lvl
                dev["dimlevel"] = int(lvl*100)  # From 16 bit integer to percent
                #dev["dimlevel"] = int((i.power_level/65535)*100)  # From 16 bit integer to percent
                dev["status"] = "on" if lvl > 0 else "off"
            except:
                print("Oops")
                print i
                print i.power_level

            self.switches[dev_id] = dev
            self.devices[dev_id] = dev

            self.log.info('Found {}'.format(dev['name']))

        self.devicesRetrieved = True

        return self.devices

    def getLightState(self, devid):
        """Get state of one light"""
        self.log.trace('getLighState {}'.format(self.devices[devid]["name"]))

        power = self.devices[devid]["bulb"].get_power()
        color = self.devices[devid]["bulb"].get_color()
        self.colour = {"hue": color[0],
                       "saturation": color[1],
                       "brightness": color[2],
                       "kelvin": color[3]}
        lvl = int(100*self.colour["brightness"]/65535)

        print lvl
        self.devices[devid]["dimlevel"] = lvl  # From 16 bit integer to percent

        state = {"power":    u'on' if power > 0 else u'off',  # 'on'/'off'
                 "dimlevel": int(lvl),                  # 0-100
                 }
        return state

        #    self.log.error('getLightState failed. Received status {}'.format(response.status_code))
        #    return None


    def listSwitches(self):
        """Create a dictionary with all lights"""

        if len(self.devices) == 0:
            devs = self.list_lights()

        return self.switches

    def getErrorString(self, res_code):
        return res_code  # TOT: Remove

    def dim(self, devId, level, limit=0):
        """ Dim light, level=0-100 """
        #self.log.trace('Dim {} level {}'.format(self.devices[devId]["name"]), str(float(level/100.0))))
        self.log.trace('Dim {} '.format(self.devices[devId]["name"]))
        self.log.trace('Level {}'.format(str(float(level/100.0))))
        if self.colour["hue"] == None:
            self.get_colour(devId)
        power = 65535*level/100
        color = (self.colour["hue"], self.colour["saturation"], power, self.colour["kelvin"])
        self.devices[devId]["bulb"].set_color(color, duration=1, rapid=False)
        self.colour["brightness"] = power
        self.dim_level = level
        #TODO: Add support for Duration

        return True

    def get_dim(self, devId):
        colour = self.get_colour(devId)
        lvl = int(100*colour[2]/65535)
        self.dim_level = lvl
        return lvl

    def get_colour(self, devId):
        color = self.devices[devId]["bulb"].get_color()
        #print color
        self.colour = {"hue": color[0],
                       "saturation": color[1],
                       "brightness": color[2],
                       "kelvin": color[3]}
        return self.colour


    def checkResponse(self, response):
        pass


    def getName(self, dev_id):
        try:
            return self.names[dev_id]
        except:
            response = self.doRequest('device/info', {'id': dev_id, 'supportedMethods': self.SUPPORTED_METHODS})

            if ('error' in response):
                name = ''
                retString = response['error']
                print ("retString=" + retString)
            else:
                name = response['name']
                self.names[dev_id] = response['name']

            return name

    def getNumberOfDevices(self):
        if len(self.switches) == 0:
            self.listSwitches()
        return len(self.switches)

    def getDeviceId(self, i):
        return (self.devices[i])

    def getModel(self, dev_id):
        if dev_id in self.switches:
            s = self.switches[dev_id]
            return s["model"]
        elif dev_id in self.remotes:
            s = self.remotes[dev_id]
            return s["model"]
        elif dev_id in self.sensors:
            s = self.sensors[dev_id]
            return s["model"]

        response = self.doRequest('device/info', {'id': dev_id, 'supportedMethods': self.SUPPORTED_METHODS})

        if ('error' in response):
            model = ''
            retString = response['error']
            print ("retString=" + retString)
        else:
            if response['type'] == 'device':
                self.models[dev_id] = response['model']
            elif response['type'] == "group":
                self.models[dev_id] = 'group'
                # Devices in the group stored in  response['devices']

        return self.models[dev_id]

    # dead code

    def listRemotes(self):
        if not self.devicesRetrieved:
            self.listSwitches()
        return self.remotes

    def listSensors(self):
        response = self.doRequest('sensors/list', {'includeIgnored': 1, 'includeValues': 1})
        self.log.info("Number of sensors: %i" % len(response['sensor']))
        for sensor in response['sensor']:
            if sensor["id"] not in self.sensors:
                s = {}
                devId = str(sensor["id"])
                s["id"] = devId
                s["name"] = sensor["name"]
                s["new"] = True
                if "temp" in sensor:
                    s["isTempSensor"] = True
                    s["temp"] = float(sensor["temp"])  # C/ F
                    s["lastTemp"] = -274.0
                else:
                    s["isTempSensor"] = False

                if "humidity" in sensor:
                    s["id"] = devId
                    s["isHumiditySensor"] = True
                    s["humidity"] = float(sensor["humidity"])
                    s["lastHumidity"] = -999.0
                else:
                    s["isHumiditySensor"] = False

                if "temp" in sensor and "humidity" in sensor:
                    s["isMultiLevel"] = True
                else:
                    s["isMultiLevel"] = False

                self.sensors[devId] = s
                self.names[sensor["id"]] = devId

        return self.sensors
