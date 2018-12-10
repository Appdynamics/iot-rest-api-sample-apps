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
'''

# Read Command Line Options
parser = argparse.ArgumentParser()

# Mandatory argument - appkey
parser.add_argument("appkey", help="set application key")

#optional arguments
parser.add_argument("-c", "--collectorurl", default = "https://iot-col.eum-appdynamics.com",
                    help="set IoT Collector URL to which the beacons should be sent to")
parser.add_argument("-u", "--url", help="set sample URL to trigger network request and capture network event")
parser.add_argument("-X", "--request", default = "GET", help="set request method for the URL. Default is set to GET")
parser.add_argument("-d", "--data", help="set HTTP POST data in JSON format")
parser.add_argument("-v", "--verbose", action="store_true", help="enable debug info")

args = parser.parse_args()

# Construct collector url to send beacons to
sendBeaconUrl = args.collectorurl + '/eumcollector/iot/v1/application/' + args.appkey + '/beacons'

if args.verbose:
  print("Beacon URL: {}".format(sendBeaconUrl))

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

  print("send custom event")
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

  print("send network event for url: {}".format(network_event[0]['url']))
  send_beacon(beacon)


# Trigger network request if url is given as a command line option
# Capture network event including url, response code, duration etc
# Construct and send beacon with the captured network event
def capture_and_send_network_event():
  startTime = time.time()

  data_bytes = ""
  if args.data:
    data_str = json.dumps(args.data)
    data_bytes = data_str.encode('utf-8')

  data_size = len(data_bytes)

  # Attach ADRUM Headers to HTTP Request to get BT Correlation Data in Response Headers
  r = requests.request(args.request, args.url,
                       headers={'ADRUM': 'isAjax:true',
                                'ADRUM_1': 'isMobile:true',
                                'Accept': 'application/json',
                                'Content-Type': 'application/json',
                                'Content-Length': str(data_size)},
                       data=data_bytes)

  endTime = time.time()

  response_headers = {}

  if args.verbose:
    print("sent {} request to url: {}".format(args.request, args.url))
    print("status code: {}".format(r.status_code))
    print("response headers: {}".format(r.headers))
    print("content length: {}".format(data_size))

  # As part of network event, capture and send all response headers which include BT Correlation Data
  for key, value in r.headers.iteritems():
    response_headers[key] = [value]
    if args.verbose:
      print(key + ":" + value)

  network_event = [{}]
  network_event[0]['url'] = args.url
  network_event[0]['statusCode'] = r.status_code
  network_event[0]['responseHeaders'] = response_headers
  network_event[0]['timestamp'] = (int(time.time()) * 1000)
  network_event[0]['duration'] = int(endTime - startTime)
  network_event[0]['requestContentLength'] = data_size

  if (r.content):
    network_event[0]['responseContentLength'] = len(r.content)

  beacon = [{}]
  beacon[0]['deviceInfo'] = device_info
  beacon[0]['versionInfo'] = version_info
  beacon[0]['networkRequestEvents'] = network_event

  print("send network event for url:" + network_event[0]['url'])
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
  print("send error event")
  send_beacon(beacon)


# Send beacon to IoT Collector
def send_beacon(beacon):
  # Compress Payload
  out = io.BytesIO()
  with gzip.GzipFile(fileobj=out, mode='w') as f:
    json_str = json.dumps(beacon)
    json_bytes = json_str.encode('utf-8')
    f.write(json_bytes)

  if args.verbose:
    print('beacon: {}'.format(beacon))

  r = requests.post(
        sendBeaconUrl,
        headers={
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Content-Encoding': 'gzip'
        },
        data=out.getvalue()
      )

  print('resp code: {}'.format(r.status_code))

  if args.verbose:
    print('send url: {}'.format(sendBeaconUrl))
    print('resp headers: {}'.format(r.headers))


# Send custom event
send_custom_event()

# If url is given as an option then trigger network request to capture network event and send it to collector.
if args.url:
  capture_and_send_network_event()
else:
  send_network_event()

# Send error event
send_error_event()
