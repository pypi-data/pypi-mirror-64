#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Christian Heider Nielsen'
__doc__ = r'''

           Created on 18/03/2020
           '''

from heimdallr.utilities import set_all_heimdallr_settings

GOOGLE_CALENDAR_ID = "nf1knhum9rdcugt700ah3or09b277gtp@import.calendar.google.com"  # Christian Alexandra

MQTT_ACCESS_TOKEN = "CV8qDsTJkSX3AeHamFP6"
MQTT_USERNAME = "iqgiyzir"
MQTT_PASSWORD = "9b0C2jJFoMxh"
MQTT_BROKER = "m24.cloudmqtt.com"
MQTT_PORT = 10915

if __name__ == '__main__':
  set_all_heimdallr_settings(
    google_calendar_id=GOOGLE_CALENDAR_ID,
    mqtt_access_token=MQTT_ACCESS_TOKEN,
    mqtt_username=MQTT_USERNAME,
    mqtt_password=MQTT_PASSWORD,
    mqtt_broker=MQTT_BROKER,
    mqtt_port=MQTT_PORT)
