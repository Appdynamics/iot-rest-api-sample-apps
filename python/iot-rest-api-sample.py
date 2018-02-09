"""
Copyright (c) AppDynamics, Inc., and its affiliates
2017

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import requests
import json
import time
import random
import gzip
import argparse

# For compatibility between python 2 and 3
try:
  import BytesIO as io
except ImportError:
  import io

'''
This sample code illustrates use of IoT REST API with sample data generated for a smart car application.
Data is first validated using /validate-beacons end point and then sent to /beacons end point to be stored
'''

# Read Command Line Options
parser = argparse.ArgumentParser()

# Mandatory argument - appkey
parser.add_argument("appkey", help="Set application key")

#optional arguments
parser.add_argument("-c", "--collectorurl", default = "http://shadow-eum-iot-col.appdynamics.com",
                    help="set IoT Collector URL to which the beacons should be sent to",)
parser.add_argument("-u", "--requesturl", help="set sample URL to trigger network request, capture and send network event",)
parser.add_argument("-x", "--requesttype", default = "GET", help="set request type for the URL. Default is set to GET",)
parser.add_argument("-d", "--requestdata", help="set data to be sent with HTTP Request for URL",)

args = parser.parse_args()

# Construct collector url to send beacons to
sendBeaconUrl = args.collectorurl + '/eumcollector/iot/v1/application/' + args.appkey + '/beacons'

# Device Information on which the application is running
device_info = {
    'deviceId': '1111',
    'deviceName': 'AudiS3',
    'deviceType': 'SmartCar'
  }

# Version Information of the application
version_info = {
    'hardwareVersion': '1.0',
    'firmwareVersion': '1.0',
    'softwareVersion': '1.0',
    'operatingSystemVersion': '1.0'
  }


# Construct and send a beacon with a sample custom event
def send_custom_event():
  custom_event = [{
      'eventType': 'Custom Event',
      'eventSummary': 'Diagnostic Data Captured in Smart Car',
      'timestamp': (int(time.time()) * 1000),
      'datetimeProperties': {
        'Last Engine Start Time': 1512483673000
      },
      'stringProperties': {
        'VinNumber': 'VN123456',
      },
      'doubleProperties': {
        'Temperature': 101.3
      },
      'longProperties': {
        'MPG Reading': 23,
        'Annual Mileage': 12000
      },
      'booleanProperties': {
        'Engine Lights ON': 'false'
      }
    }]
  beacon = [{}]
  beacon[0]['deviceInfo'] = device_info
  beacon[0]['versionInfo'] = version_info
  beacon[0]['customEvents'] = custom_event
  send_beacon(beacon)


# Construct and send a beacon with a sample network event
def send_network_event():
  network_event = [{
    'timestamp': (int(time.time()) * 1000),
    'duration': 20,
    'url': 'https://apdy.api.com/weather',
    'statusCode': 202,
    'networkError': 'NULL',
    'requestContentLength': 300,
    'responseContentLength': 100,
    'stringProperties': {
      'city': 'San Francisco',
      'country': 'USA'
    },
    'longProperties': {
      'zip': 94107
    },
    'doubleProperties': {
      'lat': 37.30,
      'long': -122.39
    }
  }]
  beacon = [{}]
  beacon[0]['deviceInfo'] = device_info
  beacon[0]['versionInfo'] = version_info
  beacon[0]['networkRequestEvents'] = network_event
  send_beacon(beacon)


# Trigger network request if url given as a command line option
# Capture network event containing url, response code, duration etc
# Construct and send beacon with the captured network event
def capture_and_send_network_event():
  startTime = time.time()

  data_bytes = None
  if args.requestdata:
    data_str = json.dumps(args.requestdata)
    data_bytes = data_str.encode('utf-8')

  r = requests.request(args.requesttype, args.requesturl,
                       headers={'ADRUM': 'isAjax:true',
                                'ADRUM_1': 'isMobile:true',
                                'Accept': 'application/json',
                                'Content-Type': 'application/json'},
                       data=data_bytes)

  endTime = time.time()

  response_headers = {}

  for key, value in r.headers.iteritems():
    response_headers[key] = [value]

  network_event = [{}]
  network_event[0]['url'] = args.requesturl
  network_event[0]['statusCode'] = r.status_code
  network_event[0]['responseHeaders'] = response_headers
  network_event[0]['timestamp'] = (int(time.time()) * 1000)
  network_event[0]['duration'] = int(endTime - startTime)

  if (r.content):
    network_event[0]['responseContentLength'] = len(r.content)

  beacon = [{}]
  beacon[0]['deviceInfo'] = device_info
  beacon[0]['versionInfo'] = version_info
  beacon[0]['networkRequestEvents'] = network_event

  send_beacon(beacon)


# Construct and send a beacon with a sample error event
# Two errors of type critical and fatal are included in the beacon
def send_error_event():
  error_events = [{
    'timestamp': (int(time.time()) * 1000),
    'duration': 10,
    'name': 'Bluetooth Connection Error',
    'message': 'connection dropped during voice call due to bluetooth exception',
    'severity': 'critical',
    'stringProperties': {
        'UUID': '00001101-0000-1000-8000-00805f9b34fb',
        'Bluetooth Version': '3.0'
    },
    'longProperties': {
        'Error Code': 43
    },
  },
  {
    'timestamp': (int(time.time()) * 1000),
    'duration': 10,
    'name': 'NullPointerException',
    'message': 'Tried to invoke method on null object reference',
    'stackTraces': [{
      'thread': '1',
      'runtime': 'native',
      'stackFrames': [{
        'symbolName': 'process_payment',
        'packageName': 'mediaplayer.so',
        'filePath': 'payment.cpp',
        'lineNumber': 123,
        'absoluteAddress': 0
      }]
    }],
    'errorStackTraceIndex': 0,
    'severity': 'fatal',
  }]
  beacon = [{}]
  beacon[0]['deviceInfo'] = device_info
  beacon[0]['versionInfo'] = version_info
  beacon[0]['errorEvents'] = error_events
  send_beacon(beacon)


# Send beacon to IoT Collector
def send_beacon(beacon):
  out = io.BytesIO()
  with gzip.GzipFile(fileobj=out, mode='w') as f:
    json_str = json.dumps(beacon)
    json_bytes = json_str.encode('utf-8')
    f.write(json_bytes)

  print('beacon: {}'.format(beacon))

  # send beacon if validation is successful
  r = requests.post(
        sendBeaconUrl,
        headers={
          'Content-Type': 'application/json',
          'Content-Length': str(len(json_str)),
          'Accept': 'application/json',
          'Content-Encoding': 'gzip',
        },
        data=out.getvalue()
      )

  print('send url: {}'.format(sendBeaconUrl))
  print('resp code: {}'.format(r.status_code))
  print('resp headers: {}'.format(r.headers))
  print('resp content: {}\n'.format(r.content))


# Send custom event
send_custom_event()

# If url is given as an option, trigger network request, capture network event and send it to collector.
if args.requesturl:
  capture_and_send_network_event()
else:
  send_network_event()

# Send error event
send_error_event()
