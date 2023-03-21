DATASET NAME:
N/A

SOURCE:
N/A

RELEVANT LINKS:
https://nsidc.org/sites/default/files/atl10-v005-userguide_1_0.pdf
https://nsidc.org/sites/nsidc.org/files/technical-references/ICESat2_ATL10_data_dict_v004.pdf
https://nsidc.org/sites/nsidc.org/files/technical-references/ICESat2_ATL07_ATL10_ATL20_ATL21_ATBD_r005.pdf
https://openaltimetry.org/data/icesat2/

TIME PERIOD(S):
October 13 2018 - Present

GEOGRAPHIC REGION(S):
Global

MODALITY:
Laser Altimetry

SPACIAL RESOLUTION:
N/A

TEMPORAL RESOLUTION:
N/A

DATA FORMATS:
ICESAT-2 ATL10 Data Product's .h5 files.

NOTES:
The ICESAT2-ATL10toCSV.py script can be executed via the command line by 
"python3 <pathToATL10toCSV.py> <[path to n number of .h5 files]>"

Per the first spec above, the returned data product has many different fields and many are nuanced. 

At the moment, downloading a software like HDFView to visualize the folder structure of the .h5 file can
be used to modify the script and extract different features into the csv.

As it stands, the CSV is written with Latitude, Longitude, beam_fb_height (height relative to the sea surface, correcting for tide), time,
and a computed ground-track distance between each ICE-SAT2 footprint (in meters).

The python code is written to extract data from the "gt1r" beam, which upon visualization from (https://openaltimetry.org/data/icesat2/)
is not the center beam. This should not matter so long as all spatial data corresponds to the same beam, but more research should be done to validate this nuance and possibly switch to the "gt2r" beam.