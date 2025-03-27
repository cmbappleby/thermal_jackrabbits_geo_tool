import arcpy
import cv2
import os
import glob
import re
import pandas as pd
from moviepy import *

srt_gdb = arcpy.GetParameterAsText(0)
vids_folder = arcpy.GetParameterAsText(1)
overlap_frames_out_folder = arcpy.GetParameterAsText(2)
obs_csv_fp = arcpy.GetParameterAsText(3)

# Read observation CSV into pandas data frame


# Read SRT GDB feature classes into a list?


# Loop through the obs CSV (i)


    # Use first four characters of Flight to create fp for detection fc


    # Convert Start and End times to seconds



    # Select points in detection fc using Start and End time


    #