## Overview
This folder contains sample applications written in Python Programming Language showing how to use IoT REST API.

These applications have been tested with python 2.7 and 3.0 versions on Mac OS X.

## iot-rest-api-sample.py
This sample app creates one event each of type - custom, network and error events.

Below variables need to be set before running the application.
```python
iot[appKey]  //AppKey generated in the controller when creating new application
iot[collectorUrl] //URL to validate or send the events to collector
```
Make sure all the packages imported in the file are installed.

```python
$ python iot-rest-api-sample.py
```
