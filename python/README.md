## Overview
This folder contains sample applications written in Python Programming Language showing how to use IoT REST API.

These applications have been tested with python 2.7 and 3.0 versions on Mac OS X.

## iot-rest-api-sample.py
This sample app creates and sends one event each of type - custom, network and error events.

```python
usage: iot-rest-api-sample.py appkey [-h] [-c COLLECTORURL] [-u REQUESTURL]
       [-x REQUESTTYPE] [-d REQUESTDATA]

positional arguments:
  appkey                Set application key

optional arguments:
  -h, --help            Show this help message and exit
  -c, --collectorurl    Set IoT Collector URL to which the beacons should be sent to
  -u, --requesturl      set sample URL to trigger network request, capture and send network event
  -x, --requesttype     Set request type for the URL. Default is set to GET
  -d, --requestdata     Set data to be sent with HTTP Request for URL
```
