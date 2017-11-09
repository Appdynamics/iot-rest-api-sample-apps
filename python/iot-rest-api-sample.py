import requests
import json
import time
import random
import StringIO
import gzip

'''
This sample code illustrates use of IoT REST API with sample data generated for a smart car application.
Data is first validated using /validate-beacons end point and then later sent to /beacons end point to be stored
'''

#set iot appKey and collectorUrl
iot = {}
iot['appKey'] = 'AD-AAB-AAF-ZGK'
iot['collectorUrl'] = 'https://iot-col.eum-appdynamics.com'

#custom event object
custom_event = {
  'deviceInfo':{
    'deviceId':'1111',
    'deviceName':'AudiS3',
    'deviceType':'SmartCar'
  },
  'versionInfo':{
    'hardwareVersion':'1.0',
    'firmwareVersion':'1.0',
    'softwareVersion':'1.0',
    'operatingSystemVersion':'1.0'
  },
  'customEvents':[
    {
      'eventType':'Custom Event',
      'eventSummary':'Diagnostic Data Captured in Smart Car',
      'timestamp': ((int(time.time())*1000)),
      'dateProperties':{
        'Last Engine Start Time':1492266358
      },
      'stringProperties': {
          'VinNumber':'VN123456',
      },
      'doubleProperties':{
          'Temperature': 101.3
      },
      'integerProperties':{
          'MPG Reading': 23,
          'Annual Mileage': 12000
      },
      'booleanProperties':{
          'Engine Lights ON': 'false'
      }
    }
  ]
}

#network event object
network_event = {
  'deviceInfo':{
    'deviceId':'1111',
    'deviceName':'AudiS3',
    'deviceType':'SmartCar'
  },
  'versionInfo':{
    'hardwareVersion':'1.0',
    'firmwareVersion':'1.0',
    'softwareVersion':'1.0',
    'operatingSystemVersion':'1.0'
  },
  'networkRequestEvents': [
    {
            'timestamp': ((int(time.time()) * 1000)),
            'duration': 20,
            'url': 'https://apdy.api.com/weather',
            'statusCode': 202,
            'networkError': 'NULL',
            'requestContentLength': 300,
            'responseContentLength': 100,
            'stringProperties': {
                'city': 'San Francisco',
                'country':'USA'
            },
            'integerProperties': {
                'zip': 94107
            },
            'doubleProperties': {
                'lat': 37.30, 'long':-122.39
            }
    }
 ]
}

#error event object
error_event = {
    'deviceInfo': {
        'deviceId': '1111',
        'deviceName': 'AudiS3',
        'deviceType': 'SmartCar'
    },
  'versionInfo':{
    'hardwareVersion':'1.0',
    'firmwareVersion':'1.0',
    'softwareVersion':'1.0',
    'operatingSystemVersion':'1.0'
  },
  'errorEvents': [
      {
            'timestamp': ((int(time.time()) * 1000)),
            'duration': 10,
            'name': 'Bluetooth Connection Error',
            'message': 'connection dropped during voice call due to bluetooth exception',
            'severity': 'critical',
            'stringProperties': {
                'UUID': '00001101-0000-1000-8000-00805f9b34fb',
                'Bluetooth Version': '3.0'
            },
            'integerProperties': {
                'Error Code': 43
            },
      },
      {
          'timestamp': ((int(time.time()) * 1000)),
          'duration': 10,
          'name': 'NullPointerException',
          'message': 'Tried to invoke method on null object reference',
          'stackTraces': [
              {
                  'thread': '1',
                  'runtime': 'native',
                  'stackFrames': [
                      {
                          'symbolName': 'process_payment',
                          'packageName': 'mediaplayer.so',
                          'filePath': 'payment.cpp',
                          'lineNumber': 123,
                          'absoluteAddress': 0
                      }
                  ]
              }
          ],
          'errorStackTraceIndex': 0,
          'severity': 'fatal',
      }
    ]
}

def validate_event(event):
    print(event)
    payload = [event]
    out = StringIO.StringIO()
    with gzip.GzipFile(fileobj=out, mode='w') as f:
        json_str = json.dumps(payload)
        json_bytes = json_str.encode('utf-8')
        f.write(json_bytes)
        out.getvalue()

    url = iot['collectorUrl'] + '/eumcollector/iot/v1/application/' + iot['appKey'] + '/validate-beacons'

    r = requests.post(url,
                      headers={
                               'Content-Type': 'application/json',
                               'Content-Length': str(len(json.dumps(payload))),
                               'Accept': 'application/json',
                               'gzip': 'true',
                               }, data=json_bytes)

    print url
    print "status:", r.status_code
    print r.headers
    print r.content

def send_event(event):
    print(event)
    payload = [event]
    out = StringIO.StringIO()
    with gzip.GzipFile(fileobj=out, mode='w') as f:
        json_str = json.dumps(payload)  # 2. string
        json_bytes = json_str.encode('utf-8')  # 3. bytes (i.e. UTF-8)
        f.write(json_bytes)
        out.getvalue()

    url = iot['collectorUrl'] + '/eumcollector/iot/v1/application/' + iot['appKey'] + '/beacons'
    
    r = requests.post(url,
                      headers={
                               'Content-Type': 'application/json',
                               'Content-Length': str(len(json.dumps(payload))),
                               'Accept': 'application/json',
                               'gzip': 'true',
                               }, data=json_bytes)

    print url
    print "status:",r.status_code
    print r.headers
    print r.content


validate_event(custom_event)
send_event(custom_event)
send_event(network_event)
send_event(error_event)



