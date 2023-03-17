#!/usr/bin/env python3

"""
Quick visualization of data along a ICESAT2 Track
To understand more about the data being input to this script, consider visiting https://nsidc.org/sites/default/files/atl10-v005-userguide_1_0.pdf
Code written originally by: Chris Polashenski
Refactored, added command line support, and removed sartopy package: John Baker
"""

import h5py
import pandas as pd
import datetime
import numpy as np
import sys
import haversine as hs

if(len(sys.argv) == 1):
    print("SYNTAX ERROR")
    print("Expected: python3 Open_ICESAT2.h5v.py file1.h5 file2.h5 file3.h5 ...")
    quit()

if(len(sys.argv) >= 1):
    for x in range(1, len(sys.argv)):
        FILE_NAME = sys.argv[x]
        if(FILE_NAME[-3:] != ".h5"):
            print("Encountered unexpected file type: " + FILE_NAME)
            print("Only .h5 files are supported. Now exiting...")
            quit()
        OUT_FILE = FILE_NAME[:-3] + ".csv"

        with h5py.File(FILE_NAME, mode='r') as f:

            latvar = f['/gt1r/freeboard_beam_segment/beam_freeboard/latitude']
            latitude = latvar[:]
            latitude = list(latitude)
            
            lonvar = f['/gt1r/freeboard_beam_segment/beam_freeboard/longitude']
            longitude = lonvar[:]
            longitude = list(longitude)
            
            dset_name = '/gt1r/freeboard_beam_segment/beam_freeboard/beam_fb_height'
            datavar = f[dset_name]
            data = datavar[:]

            units = datavar.attrs['units']
            long_name = datavar.attrs['long_name']
            _FillValue = datavar.attrs['_FillValue']
            # Handle FillValue
            data[data == _FillValue] = np.nan
            data = np.ma.masked_where(np.isnan(data), data)

            timevar = f['/gt1r/freeboard_beam_segment/beam_freeboard/delta_time']
            time = timevar[:]
            time = list(time)

            dateTime = []
            GPS_EPOCH = datetime.datetime(2018,1,1).timestamp()    # Passing in the ATLAS EPOCH

            for timeInSec in time:
                calendarTime = datetime.datetime.fromtimestamp(timeInSec+GPS_EPOCH).strftime('\"%H:%M:%S.%f %Y-%m-%d\"')
                dateTime.append(calendarTime)

            df = pd.DataFrame({
                "Latitude": latitude,
                "Longitude": longitude,
                "Freeboard Height": data,
                "Time (seconds since 1/1/2018)": time,
                "Calendar Time": dateTime
            })
            df = df.replace(r'^\s*$', np.nan, regex=True)
            df = df.dropna()

            validLatitudes = list(df['Latitude'])
            validLongitudes = list(df['Longitude'])

            distance = []
            x1 = validLongitudes[0]
            y1 = validLatitudes[0]

            for i in range(len(validLatitudes)):
                x2 = validLongitudes[i]
                y2 = validLatitudes[i]
                deltaDistance = hs.haversine((y1,x1), (y2, x2), normalize=True, unit="m")
                distance.append(deltaDistance)
                x1= x2
                y1 = y2

            df.insert(3, "Along-Ground Distance Change (m)",distance)

            df.to_csv(OUT_FILE, date_format=None)

            print("\nSuccesfully wrote to output csv. Dataframe shape:")
            print(df.shape)
            print("\n")
            quit()