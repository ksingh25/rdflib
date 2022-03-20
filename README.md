# mrdflib
mRDFLib is a port of RDFLib for micropython for working with RDF. 
It is a work in progress and the idea is to make the code as small as possible. 
Currently XML, isodate, Decimal (and thus _XSD_DECIMAL, _XSD_DATETIME, _XSD_DATE, etc.) are not supported. 

# Quickstart

mRDFLib has been tested by compiling micropython on Linux and ESP32 (with 4MB PSRAM).

## Prerequisites
To test is quickly you need either linux with python3 or ESP32 with 4MB of SPIRAM. 
For testing over ESP32, one needs to install IDF (tested with v4.0.2, adafruit-ampy, picocom).

## Linux 
To test it on Linux, please compile the micropython with advanced REGEX options enabled. This can be done by modifying
micropython/ports/unix/mpconfigport.h

and adding the following (after `#ifndef MICROPY_UNIX_MINIMAL` for example)

```
#define MICROPY_PY_URE_SUB 40
#define MICROPY_PY_URE_MATCH_GROUPS         (1)
#define MICROPY_PY_URE_MATCH_SPAN_START_END (1)
```

## ESP32
To test it on ESP32, please install idf framework (tested with IDF v4.0.2), download micropython code, 
cd to `micropython/ports/esp32` directory and then compile and flash the firware

```
idf.py -D MICROPY_BOARD=GENERIC_SPIRAM -B build-GENERIC_SPIRAM  fullclean
make submodules
make BOARD=GENERIC_SPIRAM
idf.py -D MICROPY_BOARD=GENERIC_SPIRAM -B build-GENERIC_SPIRAM  -p /dev/ttyUSB0 -b 460800 erase_flash
idf.py -D MICROPY_BOARD=GENERIC_SPIRAM -B build-GENERIC_SPIRAM  -p /dev/ttyUSB0 -b 460800 flash`
```

## Upload files on ESP32
You may skip this step if you just need to test it on Linux with micropython.
The step is to upload the files on ESP32. 
```
git clone 
cd mRDFLib
````
Upload all the files manually or use the copy.py script or WebREPL over WiFi. Uploading files over UART takes around 7 to 10 minutes. 
mRDFLib is around 800KB and thus the next step will be to reduce its size.

## Test some examples
You may enter the terminal using picocom.

`picocom -b 115200 /dev/ttyUSB0`

1. Add some facts to the graph and serialize them in different formats.
```
>>> execfile('example_serialize.py')
--- printing raw triples ---
N2cd597acdbf84ff7bc6c6df8380d3888 http://xmlns.com/foaf/0.1/name Jack Jack
N636a33fe2c9946e7a53228e5a3ae15e4 http://xmlns.com/foaf/0.1/nick donna
N636a33fe2c9946e7a53228e5a3ae15e4 http://www.w3.org/1999/02/22-rdf-syntax-ns#type http://xmlns.com/foaf/0.1/Person
N2cd597acdbf84ff7bc6c6df8380d3888 http://xmlns.com/foaf/0.1/nick jack
N636a33fe2c9946e7a53228e5a3ae15e4 http://xmlns.com/foaf/0.1/name Donna Fales
N2cd597acdbf84ff7bc6c6df8380d3888 http://www.w3.org/1999/02/22-rdf-syntax-ns#type http://xmlns.com/foaf/0.1/Person

--- printing mboxes ---

RDF Serializations:
--- start: turtle ---
@prefix foaf: <http://xmlns.com/foaf/0.1/> .

[] a foaf:Person ;
    foaf:name "Jack Jack" ;
    foaf:nick "jack"@en .

[] a foaf:Person ;
    foaf:name "Donna Fales" ;
    foaf:nick "donna"@foo .


--- end: turtle ---
...
```

2. Input a string containing RDF triples, add triples to the RDF store, serialize the graph to JSON-LD format 

```
>>> execfile('example_sosa.py')
Warning: parser.py BytesIOWrapper not supported
absolutize namespacemanager <NamespaceManager object at 3f8f5ab0>
Warning namespace.py absolutize: getcwd is different on linux vs other platforms
Graph length 12
--- start: JSON-LD ---
[{"@id": "file:///.%2f/sensor/philips/HJC42XB/bulb","@type": ["http://www.w3.org/ns/sosa#Sensor"],"http://www.w3.org/ns/sosa#observes": [{"@id": "file:///.%2f/philips/46N7743619/light"}],"http://www.w3.org/2000/01/rdf-schema#label": [{"@value": "Philips E27 Bulb - HJC42XB - Read Lumen","@language": "en"}]},{"@id": "file:///.%2f/actuator/philips/HJC42XB/bulb","http://www.w3.org/ns/sosa#actsOnProperty": [{"@id": "file:///.%2f/philips/46N7743619/light"}],"http://www.w3.org/2000/01/rdf-schema#label": [{"@value": "Philips E27 Bulb - HJC42XB - Turn On/Off","@language": "en"}],"@type": ["http://www.w3.org/ns/sosa#Actuator"],"http://www.w3.org/ns/sosa#usedProcedure": [{"@id": "file:///.%2f/philips/46N7743619/switchAPI"}]},{"@id": "file:///.%2f/philips/46N7743619","http://www.w3.org/2000/01/rdf-schema#label": [{"@value": "Philips Hue Bridge 46N7743619","@language": "en"}],"http://www.w3.org/ns/sosa#hosts": [{"@id": "file:///.%2f/actuator/philips/HJC42XB/bulb"},{"@id": "file:///.%2f/sensor/philips/HJC42XB/bulb"}],"@type": ["http://www.w3.org/ns/sosa#Platform"],"http://www.w3.org/2000/01/rdf-schema#comment": [{"@value": "Philips Hue Bridge - installed in living room","@language": "en"}]}]
--- end: JSON-LD ---
```


3. Download a file over http (currently hrrps is not working), parse and serialize it.
put the foaf_modified.n3 (original foaf file has some special characters which are causing problems for parsing) file on a folder on your PC and run a simple HTTP Server to make it accessible on web.
On your PC:
`sudo python -m SimpleHTTPServer 80`

Now to the ESP32 (using picocom)
connect to WiFi
```
>>> execfile('wlan.py')
network config: ('192.168.0.20', '255.255.255.0', '192.168.0.254', '212.27.40.241')
```
This download the whole foaf.n3, parses it and prints the triples on the terminal.

