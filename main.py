"""
The purpose of this tool is to extract frames from thermal drone footage that can be used to confirm user detections
of black-tailed jackrabbits.

This is the code executed by ArcGIS Pro when the geoprocessing tool is ran.
"""


import arcpy
import cv2
import os
import glob
import re
import pandas as pd
from moviepy import *
import functions


# === USER INPUTS === #
srt_gdb = arcpy.GetParameterAsText(0)
vids_folder = arcpy.GetParameterAsText(1)
overlap_frames_out_folder = arcpy.GetParameterAsText(2)
obs_csv_fp = arcpy.GetParameterAsText(3)

# === READ CSV AND GET LIST OF SRT GDB FEATURE CLASSES === #
obs_csv = pd.read_csv(obs_csv_fp)

arcpy.env.workspace = srt_gdb
# Only need FCs with a loop designation (ex: F3100_L3)
srt_fc_list = arcpy.ListFeatureClasses("F*_L*")

# === EXTRACT FRAMES FROM DETECTION AND OVERLAPPING VIDEOS === #
# Loop through the obs CSV (i)
for i in range(len(obs_csv)):
    # Prevent outputs from being added to the map
    arcpy.env.addOutputsToMap = False

    # Get filename from CSV
    filename = obs_csv['Filename'][i]

    # Create fp for detection video
    det_vid_name = filename + ".MOV"
    det_vid_fp = os.path.join(vids_folder, det_vid_name)

    # Use first four characters of Flight from obs CSV to create fp for detection fc
    flight = filename[:4]
    det_srt_fc_name = next((fc for fc in srt_fc_list if flight in fc), None)
    det_srt_fc = os.path.join(srt_gdb, det_srt_fc_name)

    # Convert Start and End times to seconds
    det_start_time = obs_csv['Start'][i]
    minute, sec = map(int, det_start_time.split(":"))
    det_start_sec = minute * 60 + sec

    det_end_time = obs_csv['End'][i]
    minute, sec = map(int, det_end_time.split(":"))
    det_end_sec = minute * 60 + sec

    # Using detection fc name, determine loop number, and create folder with loop number
    loop_num = det_srt_fc_name.split("_")[-1]
    frames_folder = os.path.join(overlap_frames_out_folder, loop_num)
    os.mkdir(frames_folder)

    # Extract frames from destination video using Start and End times (add "_detection{i}" to fn)
    det_base_fn = f"{filename}_{loop_num}_detection{i}_"
    functions.extract_frames(det_start_sec, det_end_sec, det_vid_fp, frames_folder, det_base_fn)

    # Select points in detection fc using Start and End time (select by start attribute)
    det_lyr = "det_lyr"
    arcpy.management.MakeFeature(det_srt_fc, det_lyr)

    arcpy.management.SelectLayerByAttribute(
        in_layer_or_view=det_lyr,
        selection_type="NEW_SELECTION",
        where_clause=f"start >= {det_start_sec} And start <= {det_end_sec}",
        invert_where_clause=None
    )

    # Subset SRT fc list that have the same loop number, sans detection fc (overlap fc list)
    ovlp_srt_fc_list = arcpy.ListFeatureClasses(f"*{loop_num}*")

    # Loop through overlap fc list


        # Select overlap fc points by location (within 15 m of detection points)


        # Pull min and max start values from selected overlap fc points


        # Pull FC_name from overlap fc points


        # Using FC_name and min and max start values, extract frames from overlap video (add "overlap{i}" to fn)