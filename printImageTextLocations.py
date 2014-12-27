#!/usr/bin/env python
#
# Little code snippet that reverse geocodes locations of image files.
# Quick and dirty helper for manual image tagging.

__author__ = "B. Henne"

import sys
import time
import os.path
import exiftool
from geopy.geocoders import GoogleV3, Nominatim
from geopy.location import Location

if len(sys.argv) < 2:
    sys.stderr.write('specify path to images as parameter, please\n')
    sys.exit(-1)
if len(sys.argv) > 2:
    sys.stderr.write('too many parameters.\n')
    sys.exit(-1)

files = []
param = sys.argv[1]
if os.path.isfile(param):
    files = [ param ]
elif os.path.isdir(param):
    files = os.listdir(param)
    files = [ os.path.join(param, f) for f in files ]
else:
    sys.stderr.write('not a valid path or file.\n')
    sys.exit(-2)

with exiftool.ExifTool(executable_='/usr/bin/exiftool') as et:
    for f in files:
        lon = lat = address = a= ''
        metadata = et.get_metadata(f)
        if u'Composite:GPSLongitude' in metadata and u'Composite:GPSLatitude' in metadata:
            lon = metadata[u'Composite:GPSLongitude']
            lat = metadata[u'Composite:GPSLatitude']
            if u'EXIF:GPSLongitudeRef' in metadata and metadata[u'EXIF:GPSLongitudeRef'] == u'W':
                lon = -1*lon
            if u'EXIF:GPSLatitudeRef' in metadata and metadata[u'EXIF:GPSLatitudeRef'] == u'S':
                lat = -1*lat

            for geolocator in (GoogleV3(), Nominatim()):
                address = geolocator.reverse('%s, %s' % (lat, lon), exactly_one=True, language='de')
                if type(address) == Location:
                    address = address.address
                a += '\t' + address + '\n'

        print f
        print '\t%s %s\n%s' % (lon, lat, a)
