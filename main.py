"""
The purpose of this tool is to extract frames from thermal drone footage that can be used to confirm user detections
of black-tailed jackrabbits.

This is the code executed by ArcGIS Pro when the geoprocessing tool is ran.
"""


import arcpy
import os
import pandas as pd
import functions


# === USER INPUTS === #
srt_gdb = arcpy.GetParameterAsText(0)
vids_folder = arcpy.GetParameterAsText(1)
overlap_frames_out_folder = arcpy.GetParameterAsText(2)
obs_csv_fp = arcpy.GetParameterAsText(3)

# === READ CSV AND SET WORKSPACE === #
obs_csv = pd.read_csv(obs_csv_fp)
arcpy.env.workspace = srt_gdb

# === EXTRACT FRAMES FROM DETECTION AND OVERLAPPING VIDEOS === #
# Loop through the obs CSV (i)
for i in range(len(obs_csv)):
    # Prevent outputs from being added to the map
    arcpy.env.addOutputsToMap = False

    # Get filename from CSV
    filename = obs_csv['Filename'][i]

    # Use first four characters of Flight from obs CSV to find SRT fc create fp for detection fc
    flight = filename[:4]
    det_srt_fc_name = arcpy.ListFeatureClasses(f"*{flight}_L*")
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

    if not os.path.isfile(frames_folder):
        os.mkdir(frames_folder)

    # Extract frames from destination video using Start and End times (add "_detection{i}" to fn)
    detection_folder = os.path.join(frames_folder, "detection")

    if not os.path.isdir(detection_folder):
        os.mkdir(detection_folder)

    det_base_fn = f"{filename}_{loop_num}_detection{i}_"
    functions.extract_frames(det_start_sec, det_end_sec, vids_folder, filename, detection_folder, det_base_fn)

    # Select points in detection fc using Start and End time (select by start attribute)
    det_lyr = "det_lyr"
    arcpy.management.MakeFeature(det_srt_fc, det_lyr)

    arcpy.management.SelectLayerByAttribute(
        in_layer_or_view=det_lyr,
        selection_type="NEW_SELECTION",
        where_clause=f"start >= {det_start_sec} And start <= {det_end_sec} And FC_Name='F{filename}",
        invert_where_clause=None
    )

    # Subset SRT fc list that have the same loop number, sans detection fc (overlap fc list)
    ovlp_srt_fc_list = arcpy.ListFeatureClasses(f"*{loop_num}*")

    # Create folder for overlapping frames
    overlap_folder = os.path.join(frames_folder, "overlap")

    if not os.path.isdir(overlap_folder):
        os.mkdir(overlap_folder)

    # Loop through overlap fc list
    for ovlp_srt_fc_name in ovlp_srt_fc_list:
        # Create file path for overlap SRT fc
        ovlp_srt_fc = os.path.join(srt_gdb, ovlp_srt_fc_name)

        # Select overlap fc points by location (within 15 m of detection points)
        ovlp_lyr = "ovlp_lyr"
        arcpy.management.MakeFeature(ovlp_srt_fc, ovlp_lyr)

        arcpy.management.SelectLayerByLocation(
            in_layer=ovlp_lyr,
            overlap_type="INTERSECT",
            select_features=det_lyr,
            search_distance="15 Meters",
            selection_type="NEW_SELECTION",
            invert_spatial_relationship="NOT_INVERT"
        )

        # PULL VALUES FROM SELECTED OVERLAP FC POINTS
        # Ensure the layer has a selection
        selected_count = int(arcpy.management.GetCount(ovlp_lyr)[0])

        if selected_count == 0:
            arcpy.AddWarning(f"No overlapping points in {ovlp_lyr} for {det_srt_fc}.")

            continue
        else:
            # Use a search cursor to get the values from "start" and "FC_Name" field
            with arcpy.da.SearchCursor(ovlp_lyr, ["start", "FC_Name"]) as cursor:
                values = [row for row in cursor]

            # Get a list of the values from the fields
            start_values = [row[0] for row in values]
            fc_names = [row[1] for row in values]

        # Check for more than one FC_Name
        fc_names_unique = set(fc_names)

        # EXTRACT FRAMES IF MORE THAN ONE FEATURE CLASS
        if len(fc_names_unique) > 1:
            functions.extract_frames_two_fcs(start_values, fc_names, fc_names_unique, loop_num, i, vids_folder,
                                             overlap_folder)
        else:
            # Get min and max start times
            min_start = min(start_values)
            max_start = max(start_values)

            # Pull FC_name, create base name, and extract frames
            ovlp_base_fn = f"{fc_names_unique[0]}_{loop_num}_overlap{i}_"
            functions.extract_frames(min_start, max_start, vids_folder, fc_names_unique[0], overlap_folder,
                                     ovlp_base_fn)
