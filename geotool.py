"""
The purpose of this tool is to create a CSV with video names and start and end times of overlapping videos. The CSV can
then be used to extract frames from the videos. It is not the most efficient code (some of it is very repetitive and
could be turned into functions), but it gets the job done.

This is the code executed by ArcGIS Pro when the geoprocessing tool is ran.
"""


import arcpy
import os
import pandas as pd


# === USER INPUTS === #
# GDB with the SRT point feature classes
srt_gdb = arcpy.GetParameterAsText(0)
# Folder containing the thermal videos
vids_folder = arcpy.GetParameterAsText(1)
# File path to the CSV containing the observations/detections with start and end times
obs_csv_fp = arcpy.GetParameterAsText(2)
# Output folder for CSVs
ovrlp_csv_folder = arcpy.GetParameterAsText(3)

# === READ CSV AND SET WORKSPACE === #
obs_csv = pd.read_csv(obs_csv_fp)
arcpy.env.workspace = srt_gdb

# === CREATE DATA FRAME TO HOLD DATA NEEDED TO EXTRACT FRAMES === #
ovrlp_cols = ["Filepath", "Type", "Start", "End", "StartTS", "EndTS"]
ovrlp_df = pd.DataFrame(columns=ovrlp_cols)

# === GET DATA FOR DETECTION AND OVERLAPPING VIDEOS === #
# Loop through the obs CSV (i)
for i, row in obs_csv.iterrows():
    # DETECTION VIDEO
    # Prevent outputs from being added to the map
    arcpy.env.addOutputsToMap = False

    # Get filename from CSV
    filename = row['Filename']

    # Use first four characters of Flight from obs CSV to find SRT fc create fp for detection fc
    flight = filename[:4]
    det_srt_fc_list = arcpy.ListFeatureClasses(f"*{flight}_L*")
    det_srt_fc_name = det_srt_fc_list[0]
    det_srt_fc = os.path.join(srt_gdb, det_srt_fc_name)

    # Convert Start and End times to seconds
    det_start_time = row['Start']
    minute, sec = map(int, det_start_time.split(":"))
    det_start_sec = minute * 60 + sec

    det_end_time = row['End']
    minute, sec = map(int, det_end_time.split(":"))
    det_end_sec = minute * 60 + sec

    # Using detection fc name, determine loop number
    loop_num = det_srt_fc_name.split("_")[-1]

    # Add detection data to data frame
    fp = os.path.join(vids_folder, f"{filename}.MOV")
    ovrlp_df.loc[len(ovrlp_df)] = [fp, "detection", det_start_sec, det_end_sec, det_start_time, det_end_time]

    # Select points in detection fc using Start and End time (select by start attribute)
    det_lyr = "det_lyr"
    arcpy.management.MakeFeatureLayer(det_srt_fc, det_lyr)

    arcpy.management.SelectLayerByAttribute(
        in_layer_or_view=det_lyr,
        selection_type="NEW_SELECTION",
        where_clause=f"start >= {det_start_sec} And start <= {det_end_sec} And FC_Name='F{filename}'",
        invert_where_clause=None
    )

    # OVERLAPPING VIDEO(S)
    # Subset SRT fc list that have the same loop number, sans detection fc (overlap fc list)
    ovlp_srt_fc_loop = arcpy.ListFeatureClasses(f"*{loop_num}*")
    ovlp_srt_fc_list = [fc for fc in ovlp_srt_fc_loop if str(flight) not in fc]

    # Loop through overlap fc list
    for ovlp_srt_fc_name in ovlp_srt_fc_list:
        # Create file path for overlap SRT fc
        ovlp_srt_fc = os.path.join(srt_gdb, ovlp_srt_fc_name)

        # Select overlap fc points by location (within 15 m of detection points)
        ovlp_lyr = "ovlp_lyr"
        arcpy.management.MakeFeatureLayer(ovlp_srt_fc, ovlp_lyr)

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
        fc_names_unique_list = list(fc_names_unique)

        # EXTRACT FRAMES IF MORE THAN ONE FEATURE CLASS
        if len(fc_names_unique_list) > 1:
            # Get the index of the second FC_Name
            second_fc_name = fc_names_unique_list[1]
            second_fc_index = fc_names.index(second_fc_name)

            # Subset the start values list
            first_start_values = start_values[:second_fc_index]
            second_start_values = start_values[second_fc_index:]
            start_values_lists = [first_start_values, second_start_values]

            for j in range(len(start_values_lists)):
                # Get min and max start values
                min_start = min(start_values_lists[j])
                max_start = max(start_values_lists[j])

                # Convert to values to timestamps
                minutes, secs = divmod(min_start, 60)
                min_ts = f"{minutes:02}:{secs:02}"
                minutes, secs = divmod(max_start, 60)
                max_ts = f"{minutes:02}:{secs:02}"

                # Get SRT fc name and remove the first character and create base file name
                fc_name = fc_names_unique_list[j][1:]

                # Add overlap data to data frame
                fp = os.path.join(vids_folder, f"{fc_name}.MOV")
                ovrlp_df.loc[len(ovrlp_df)] = [fp, "overlap", min_start, max_start, min_ts, max_ts]
        else:
            # Get min and max start times
            min_start = min(start_values)
            max_start = max(start_values)

            # Convert to values to timestamps
            minutes, secs = divmod(min_start, 60)
            min_ts = f"{minutes:02}:{secs:02}"
            minutes, secs = divmod(max_start, 60)
            max_ts = f"{minutes:02}:{secs:02}"

            # Add overlap data to data frame
            fc_name = fc_names_unique_list[0][1:]
            fp = os.path.join(vids_folder, f"{fc_name}.MOV")
            ovrlp_df.loc[len(ovrlp_df)] = [fp, "overlap", min_start, max_start, min_ts, max_ts]


        arcpy.management.Delete(ovlp_lyr)

    arcpy.management.Delete(det_lyr)

# Save detection-overlap CSV
ovrlp_df.to_csv(os.path.join(ovrlp_csv_folder, "det_ovrlp.csv"), index=False)
