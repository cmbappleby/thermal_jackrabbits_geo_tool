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


    # Select points in detection fc using Start and End time (select by start attribute)


    # Using detection fc name, determine loop number


    # Create folder with name of loop number


    # Extract frames from destination video using Start and End times (add "detection{i}" to fn)


    # Subset SRT fc list that have the same loop number, sans detection fc (overlap fc list)


    # Loop through overlap fc list


        # Select overlap fc points by location (within 15 m of detection points)


        # Pull min and max start values from selected overlap fc points


        # Pull FC_name from overlap fc points


        # Using FC_name and min and max start values, extract frames from overlap video (add "overlap{i}" to fn)