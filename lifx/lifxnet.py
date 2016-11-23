#!/usr/bin/python
AGO_LIFX_VERSION = '0.0.1'
############################################
#
# LIFX class supporting device handling via LIFX Cloud APIs
#
# Date of origin: 2016-11-19
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
import sys, getopt, httplib, urllib, json, os, thread, time
#import oauth.oauth as oauth
import datetime
from agoclient.agoapp import ConfigurationError
import json
import requests


class lifxnet(lifxbase):
    """Class used for Lifx devices via LIFX Cloud API"""

    def __init__(self, app):
        super(lifxnet, self).__init__(app)

        self.devices = {}
        self.models = {}
        self.names = {}
        self.devicesRetrieved = False

    def __get__(self, obj, objtype=None):
        pass

    def __set__(self, obj, val):
        pass

    def __delete__(self, obj):
        pass

    def init(self, API_KEY):
        self.SUPPORTED_METHODS = self.LIFX_TURNON | self.LIFX_TURNOFF | self.LIFX_DIM

        self.API_KEY = API_KEY
        if not self.API_KEY:
            raise ConfigurationError("API_KEY missing in LIFX.conf. Cannot continue")
            return False

        self.headers = {"Authorization": "Bearer %s" % self.API_KEY, }
        return True

    def close(self):
        pass

    def set_state(self, devId, state):
        """Set light to "on" or "off" """
        payload = {"power": state,}
        print payload
        response = requests.put('https://api.lifx.com/v1/lights/' + devId + '/state', data = payload, headers=self.headers)
        #print response.content
        if response.status_code == 207: # Multiple status received
            if devId in response.content:
                if '"status":"ok"' in response.content:
                    return True
                elif '"status":"offline"' in response.content:
                    return False
            else:
                return False

        if response.status_code ==200:
            print "resonse 200 - check code!"
            return True

        return False

    def list_lights(self):
        """Get a list of devices for current account"""
        response = requests.get('https://api.lifx.com/v1/lights/all', headers=self.headers)
        #print response.content
        return response

    def listSwitches(self):
        """Create a dictionary with all lights"""
        ra = self.list_lights()
        rsp = ra.content
        #print len(rsp)
        #print rsp
        #print rsp.content
        if "id" in rsp: #.content:
            rj=json.loads(rsp)
            lights = {}
            for i in rj:
                print i
                light = {}
                if u'id' in i:
                    devId = i["id"]

                    model = i["product"]["name"] # u'White 800'

                    dev = {
                        "id": devId,
                        "name": i["label"],
                        "model": model}
                    if 'White' in model:
                        dev["isDimmer"] = True
                    else:
                        dev["isDimmer"] = False
                    #light["status"] = "on" if i["connected"] else "Off"
                    self.switches[devId] = dev
        return self.switches

    def turnOn(self, devId):
        """ Turn on light"""
        print "on"
        self.set_state(devId, "on")
        return True

    def turnOff(self, devId):
        """ Turn off light"""
        print "off"
        self.set_state(devId, "off")
        #return self.doMethod(devId, self.LIFX_TURNOFF)
        return True

    def getErrorString(self, resCode):
        return resCode  # Telldus API returns strings, not resCodes. Just for making this compatible with Lifx Duo API

    def dim(self, devId, level):
        """ Dim light, level=0-100 """
        print "dim - " + str(float(level/100.0))
        #TODO: Add support for Duration
        payload = {"power": "on",
                   "brightness": float(level/100.0),
                   "duration": float(1.0),}
        #print payload
        response = requests.put('https://api.lifx.com/v1/lights/' + devId + '/state', data = payload, headers=self.headers)
        # return self.doMethod(devId, self.LIFX_DIM, level)
        return True

    def getName(self, devId):
        try:
            return self.names[devId]
        except:
            response = self.doRequest('device/info', {'id': devId, 'supportedMethods': self.SUPPORTED_METHODS})

            if ('error' in response):
                name = ''
                retString = response['error']
                print ("retString=" + retString)
            else:
                name = response['name']
                self.names[devId] = response['name']

            return name

    def getNumberOfDevices(self):
        if len(self.switches) > 0:
            return len(self.switches)
        else:
            self.listSwitches()
            return len(self.switches)

    def getDeviceId(self, i):
        return (self.devices[i])

    def getModel(self, devId):
        if devId in self.switches:
            s = self.switches[devId]
            return s["model"]
        elif devId in self.remotes:
            s = self.remotes[devId]
            return s["model"]
        elif devId in self.sensors:
            s = self.sensors[devId]
            return s["model"]

        response = self.doRequest('device/info', {'id': devId, 'supportedMethods': self.SUPPORTED_METHODS})

        if ('error' in response):
            model = ''
            retString = response['error']
            print ("retString=" + retString)
        else:
            if response['type'] == 'device':
                self.models[devId] = response['model']
            elif response['type'] == "group":
                self.models[devId] = 'group'
                # Devices in the group stored in  response['devices']

        return self.models[devId]

    # dead code

    def registerDeviceEvent(self, deviceEvent):
        pass

    def registerDeviceChangedEvent(self, deviceEvent):
        pass

    def registerSensorEvent(self, deviceEvent):
        pass

    def doRequest(self, method, params):
        pass

    def listRemotes(self):
        if not self.devicesRetrieved:
            self.listSwitches()
        return self.remotes

    def listSensors(self):
        response = self.doRequest('sensors/list', {'includeIgnored': 1, 'includeValues': 1})
        print("Number of sensors: %i" % len(response['sensor']))
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

    def sensorThread(self, sensorCallback, dummy):
        pass
