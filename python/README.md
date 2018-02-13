## Overview
This folder contains sample applications written in Python Programming Language showing how to use IoT REST API.

These applications have been tested with python 2.7 and 3.0 versions on Mac OS X.

## iot-rest-api-sample.py
This sample app creates and sends one event each of type - custom, network and error events.

Below is usage information for the sample app. Provide `appkey` as an input along with any options as needed.

```sh
USAGE: python iot-rest-api-sample.py appkey [options]
options:
-c, --collectorurl <url> IoT Collector URL to which the beacons should be sent to.
-u, --url <url>          URL to trigger network request and capture network event.
-x, --request <command>  Specify the request method to url. It is set to GET by default.
-d, --data <data>        Data in JSON format that is to be sent in a POST request.
-v, --verbose            Enable Debug Information. It is disabled by default.
-h, --help               Display available options
```

Below are the default values used by the sample app if above options are not given
```sh
DEFAULT PARAMS:
collectorurl = https://iot-col.eum-appdynamics.com
```

Here are some examples of using the sample app:

Display Usage Information
```sh
$ python iot-rest-api-sample.py -h
```

Send Sample Custom, Network, and Error Events to default APPD Collector
```sh
$ python iot-rest-api-sample.py <appkey>
```

Send Sample Custom, Network, and Error Events to Custom Collector (http://localhost:9001)
```sh
$  python iot-rest-api-sample.py <appkey> -c http://localhost:9001
```

Trigger POST Network Request to URL (http://yoururl.com) with data in JSON format. Capture and Send Network Event to Custom Collector (http://localhost:9001)
```sh
$  python iot-rest-api-sample.py <appkey> -c http://localhost:9001 -u http://yoururl.com -x POST -d '{"param1"="value1"}'
```
