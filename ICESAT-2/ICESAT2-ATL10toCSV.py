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


        # Consider adding a for loop to do this same process but for all 6 beams gt1r/l, gt2r/l, gt3r/l
        # Ex: Declare the starting beam names, and iterate through that array and push the variables into another array
        #       where you then supply them into df
        with h5py.File(FILE_NAME, mode='r') as file:

            filePathToBeamData = "freeboard_beam_segment/beam_freeboard"
            filePathToHeightData = "freeboard_beam_segment/height_segments"

            try:
                latvar = file[f'/gt1r/{filePathToBeamData}/latitude']
            except:
                filePathToBeamData = "freeboard_segment"
                filePathToHeightData = "freeboard_segment/heights"
                latvar = file[f'/gt1r/{filePathToBeamData}/latitude']
            latitude = latvar[:]
            latitude = list(latitude)
            
            lonvar = file[f'/gt1r/{filePathToBeamData}/longitude']
            longitude = lonvar[:]
            longitude = list(longitude)
            
            # Start reading in the first set of GT1R beams
            dset_name = f'/gt1r/{filePathToBeamData}/beam_fb_height'
            datavar = file[dset_name]
            data = datavar[:]

            # # Assign the Fill Value once
            _FillValue = datavar.attrs['_FillValue']

            # # Handle FillValue
            data[data == _FillValue] = np.nan
            data = np.ma.masked_where(np.isnan(data), data)

            # Read in the second (central) strong beam
            dset_name = f'/gt2r/{filePathToBeamData}/beam_fb_height'
            datavar = file[dset_name]
            data2 = datavar[:]

            # Handle FillValue
            data2[data2 == _FillValue] = np.nan
            data2 = np.ma.masked_where(np.isnan(data2), data2)

            # Read in the last (central) strong beam
            dset_name = f'/gt3r/{filePathToBeamData}/beam_fb_height'
            datavar = file[dset_name]
            data3 = datavar[:]

            # Handle FillValue
            data3[data3 == _FillValue] = np.nan
            data3 = np.ma.masked_where(np.isnan(data3), data3)

            timevar = file[f'/gt1r/{filePathToBeamData}/delta_time']
            time = timevar[:]
            time = list(time)

            data2conf = file[f'/gt2r/{filePathToBeamData}/beam_fb_confidence']
            data2conf = list(data2conf[:])

            heightSegConf = file[f'/gt2r/{filePathToHeightData}/height_segment_confidence']
            heightSegConf = list(heightSegConf[:])

            heightSegType = file[f'/gt2r/{filePathToHeightData}/height_segment_type']
            heightSegType = list(heightSegType[:])

            heightSegRefl = file[f'/gt2r/{filePathToHeightData}/asr_25']
            heightSegRefl = list(heightSegRefl[:])

            qualityFlag = file[f"/gt2r/{filePathToBeamData}/beam_fb_quality_flag"]
            qualityFlag = list(qualityFlag[:])

            dateTime = []
            GPS_EPOCH = datetime.datetime(2018,1,1).timestamp()    # Passing in the ATLAS EPOCH

            for timeInSec in time:
                calendarTime = datetime.datetime.fromtimestamp(timeInSec+GPS_EPOCH).strftime('\"%H:%M:%S.%f %Y-%m-%d\"')
                dateTime.append(calendarTime)
            
            distance = []
            x1 = longitude[0]
            y1 = latitude[0]

            for i in range(len(latitude)):
                x2 = longitude[i]
                y2 = latitude[i]
                deltaDistance = hs.haversine((y1,x1), (y2, x2), normalize=True, unit="m")
                distance.append(deltaDistance)
                x1= x2
                y1 = y2

            print("Freeboards & location")
            print(len(latitude))
            print(len(longitude))
            print(len(data))
            print(len(data2))
            print(len(data3))
            print("Heights / confidence:")
            print(len(data2conf))
            print(len(heightSegConf))
            print(len(heightSegType))
            print(len(heightSegRefl))
            print("Time")
            print(len(time))
            print(len(dateTime))

            df_dict = {
                "Latitude": latitude,
                "Longitude": longitude,
                "1FBH": data,
                "2FBH": data2,
                "3FBH": data3,
                "2FBCONF": data2conf,
                "2HSCONF": heightSegConf,
                "2HSTYPE": heightSegType,
                "2HSREFL": heightSegRefl,
                "Quality": qualityFlag,
                "GroundDist": distance,
                "Time (seconds since 1/1/2018)": time,
                "Calendar Time": dateTime
            }

            df = pd.DataFrame(dict([(k,pd.Series(v)) for k,v in df_dict.items()]))
            df = df.replace(r'^\s*$', np.nan, regex=True)
            # df = df.dropna()

            df.to_csv(OUT_FILE, date_format=None)

            print("\nSuccesfully wrote to output csv. Dataframe shape:")
            print(df.shape)
            print("\n")
            quit()