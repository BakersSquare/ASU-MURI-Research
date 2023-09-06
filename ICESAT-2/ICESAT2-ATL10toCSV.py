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

            # We'll need to restructure our script to call functions that pull this information out.
            # We could make a function and pass in these variables as keys? That way we can avoid drawing them out.
            beam_enum = ['gt1r', 'gt1l', 'gt2r', 'gt2l', 'gt3r', 'gt3l']
            data_cols = []

            df_dict = {}
            # gt1rLat, gt1rLon, gt1lLat, gt1lLon,
            # gt2rLat, gt2rLon, gt2lLat, gt2lLon,
            # gt3rLat, gt3rLon, gt3lLat, gt3lLon

            if "gt1r/freeboard_beam_segment/beam_freeboard" in file:
                filePathToBeamData = "freeboard_beam_segment/beam_freeboard"
            else:
                filePathToBeamData = "freeboard_segment"

            if "gt1r/freeboard_beam_segment/height_segments" in file:
                filePathToHeightData = "freeboard_beam_segment/height_segments"
            else:
                filePathToHeightData = "freeboard_segment/heights"

            print(filePathToBeamData)
            print(filePathToHeightData)

            for beam in beam_enum:
                print(beam)
                # Read in the lat/lon
                latvar = file[f'/{beam}/{filePathToBeamData}/latitude']
                latitude = list(latvar[:])
                lonvar = file[f'/{beam}/{filePathToBeamData}/longitude']
                longitude = list(lonvar[:])

                # Read in the freeboard height
                dset_name = f'/{beam}/{filePathToBeamData}/beam_fb_height'
                datavar = file[dset_name]
                data = datavar[:]

                # Assign the Fill Value once
                _FillValue = datavar.attrs['_FillValue']

                # Handle FillValue
                data[data == _FillValue] = np.nan
                data = np.ma.masked_where(np.isnan(data), data)

                # Read in the time and convert to readable
                timevar = file[f'/{beam}/{filePathToBeamData}/delta_time']
                time = list(timevar[:])
                dateTime = []
                GPS_EPOCH = datetime.datetime(2018,1,1).timestamp()    # Passing in the ATLAS EPOCH

                for timeInSec in time:
                    calendarTime = datetime.datetime.fromtimestamp(timeInSec+GPS_EPOCH).strftime('\"%H:%M:%S.%f %Y-%m-%d\"')
                    dateTime.append(calendarTime)

                # Read in the beam confidence
                dataConf = file[f'/{beam}/{filePathToBeamData}/beam_fb_confidence']
                dataConf = list(dataConf[:])

                # Read in the height confidence
                heightSegConf = file[f'/{beam}/{filePathToHeightData}/height_segment_confidence']
                heightSegConf = list(heightSegConf[:])

                # Read in the height segment type
                heightSegType = file[f'/{beam}/{filePathToHeightData}/height_segment_type']
                heightSegType = list(heightSegType[:])

                # Read in the reflectance
                heightSegRefl = file[f'/{beam}/{filePathToHeightData}/asr_25']
                heightSegRefl = list(heightSegRefl[:])

                # Read in the quality flag
                qualityFlag = file[f"/{beam}/{filePathToBeamData}/beam_fb_quality_flag"]
                qualityFlag = list(qualityFlag[:])
                
                # Calculate ground distance
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

                print("Beam: ", beam)
                print("Freeboards & location lengths")
                print(len(latitude))
                print(len(longitude))
                print(len(data))
                print("Heights / confidence lengths:")
                print(len(dataConf))
                print(len(heightSegConf))
                print(len(heightSegType))
                print(len(heightSegRefl))
                print("Time")
                print(len(time))
                print(len(dateTime))
                
                # We want to append the lat/lon, fbheights, and ground distance for each beam, and then dateTime only on the last
                latCol = beam + "Lat"
                lonCol = beam + "Lon"
                fbCol = beam + "FBH"
                distCol = beam + "Dist(m)"
                df_dict[latCol] = latitude
                df_dict[lonCol] = longitude
                df_dict[fbCol] = data
                df_dict[distCol] = distance

                # Keep track of the data columns so we can remove nan values
                data_cols.append(fbCol)
                

            df_dict["Calendar Time"] = dateTime

            df = pd.DataFrame(dict([(k,pd.Series(v)) for k,v in df_dict.items()]))
            df = df.replace(r'^\s*$', np.nan, regex=True)

            # Drop all rows where ICESAT has no FB height data across any of it's beams
            df = df.dropna(subset=data_cols, thresh = 1)

            df.to_csv(OUT_FILE, date_format=None)

            print("\nSuccesfully wrote to output csv. Dataframe shape:")
            print(df.shape)
            print("\n")
            quit()