import requests
import json
import time
import random
import StringIO
import gzip

'''
This sample code illustrates use of IoT REST API with sample data generated for a smart car application.
Data is first validated using /validate-beacons end point and then sent to /beacons end point to be stored
'''

# set iot appKey and collectorUrl
iot = dict()
iot['appKey'] = 'AB-AAB-AAC-AAD'
iot['collectorUrl'] = 'https://iot-col.eum-appdynamics.com'

iot['validateBeaconUrl'] = iot['collectorUrl'] + '/eumcollector/iot/v1/application/' + iot['appKey'] + '/validate-beacons'
iot['sendBeaconUrl'] = iot['collectorUrl'] + '/eumcollector/iot/v1/application/' + iot['appKey'] + '/beacons'

# beacon with custom event
beacon_custom_event = [{
  'deviceInfo': {
    'deviceId': '1111',
    'deviceName': 'AudiS3',
    'deviceType': 'SmartCar'
  },
  'versionInfo': {
    'hardwareVersion': '1.0',
    'firmwareVersion': '1.0',
    'softwareVersion': '1.0',
    'operatingSystemVersion': '1.0'
  },
  'customEvents': [{
    'eventType': 'Custom Event',
    'eventSummary': 'Diagnostic Data Captured in Smart Car',
    'timestamp': (int(time.time())*1000),
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
}]

# beacon with network event
beacon_network_event = [{
  'deviceInfo': {
    'deviceId': '1111',
    'deviceName': 'AudiS3',
    'deviceType': 'SmartCar'
  },
  'versionInfo': {
    'hardwareVersion': '1.0',
    'firmwareVersion': '1.0',
    'softwareVersion': '1.0',
    'operatingSystemVersion': '1.0'
  },
  'networkRequestEvents': [{
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
}]

# beacon with error event
beacon_error_event = [{
  'deviceInfo': {
    'deviceId': '1111',
    'deviceName': 'AudiS3',
    'deviceType': 'SmartCar'
  },
  'versionInfo':{
    'hardwareVersion': '1.0',
    'firmwareVersion': '1.0',
    'softwareVersion': '1.0',
    'operatingSystemVersion': '1.0'
  },
  'errorEvents': [{
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
}]


def send_beacon(beacon):
  out = StringIO.StringIO()
  with gzip.GzipFile(fileobj=out, mode='w') as f:
    json_str = json.dumps(beacon)
    json_bytes = json_str.encode('utf-8')
    f.write(json_bytes)

  print('beacon: {}'.format(beacon))

  # validate beacon before sending (optional)
  r = requests.post(
        iot['validateBeaconUrl'],
        headers={
          'Content-Type': 'application/json',
          'Content-Length': str(len(json_str)),
          'Accept': 'application/json',
          'Content-Encoding': 'gzip',
        },
        data=out.getvalue()
      )

  print('validate url: {}'.format(iot['validateBeaconUrl']))

  if r.status_code != 200:
    print('validate beacons failed. Check for beacon data format')
    print('resp code: {}'.format(r.status_code))
    print('resp headers: {}'.format(r.headers))
    print('resp content: {}\n'.format(r.content))
    return
  else:
    print('validate beacons passed')

  # send beacon if validation is successful
  r = requests.post(
        iot['sendBeaconUrl'],
        headers={
          'Content-Type': 'application/json',
          'Content-Length': str(len(json_str)),
          'Accept': 'application/json',
          'Content-Encoding': 'gzip',
        },
        data=out.getvalue()
      )

  print('send url: {}'.format(iot['sendBeaconUrl']))
  print('resp code: {}'.format(r.status_code))
  print('resp headers: {}'.format(r.headers))
  print('resp content: {}\n'.format(r.content))


send_beacon(beacon_custom_event)
send_beacon(beacon_network_event)
send_beacon(beacon_error_event)