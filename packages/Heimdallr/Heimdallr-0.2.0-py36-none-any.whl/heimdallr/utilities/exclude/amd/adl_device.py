#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Christian Heider Nielsen'
__doc__ = r'''

           Created on 19/03/2020
           '''

from heimdallr.utilities.exclude.amd import ADLManager


class ADLDevice(object):

    def __init__(self, adapterIndex, adapterID, busNumber, uuid, name):
        self.adapterIndex = adapterIndex
        self.adapterID = adapterID.value
        self.adapterName = name
        self.busNumber = busNumber
        self.uuid = uuid
        self.coreVoltageRange = None
        self.engineClockRange = None
        self.memoryClockRange = None
        self.fanSpeedPercentageRange = None
        self.fanspeedRPMRange = None

    # Return the current core voltage in mV
    def getCurrentCoreVoltage(self):
        return ADLManager.getInstance().getCurrentCoreVoltage(self)

    # Return the current engine frequency in MHz
    def getCurrentEngineClock(self):
        return ADLManager.getInstance().getCurrentEngineClock(self)

    # Return the current fan speed in a specified unit (ADL_DEVICE_FAN_SPEED_TYPE_PERCENTAGE or ADL_DEVICE_FAN_SPEED_TYPE_RPMS)
    def getCurrentFanSpeed(self, speedType):
        return ADLManager.getInstance().getCurrentFanSpeed(self, speedType)

    # Return the current memory frequency in MHz
    def getCurrentMemoryClock(self):
        return ADLManager.getInstance().getCurrentMemoryClock(self)

    # Return the current temperature in Celsius
    def getCurrentTemperature(self):
        return ADLManager.getInstance().getCurrentTemperature(self)

    # Return the current load (%)
    def getCurrentUsage(self):
        return ADLManager.getInstance().getCurrentUsage(self)

    # Return the core voltage range (Min, Max)
    def getCoreVoltageRange(self, reload = False):
        return ADLManager.getInstance().getCoreVoltageRange(self, reload)

    # Return the engine clock frequency range (Min, Max)
    def getEngineClockRange(self, reload = False):
        return ADLManager.getInstance().getEngineClockRange(self, reload)

    # Get the fan speed range in the specified unit (ADL_DEVICE_FAN_SPEED_TYPE_PERCENTAGE or ADL_DEVICE_FAN_SPEED_TYPE_RPMS)
    def getFanSpeedRange(self, speedType, reload = False):
        return ADLManager.getInstance().getFanSpeedRange(self, speedType, reload)

    # Return the memory clock frequency range (Min, Max)
    def getMemoryClockRange(self, reload = False):
        return ADLManager.getInstance().getMemoryClockRange(self, reload)
