import arcpy
import cv2
import os


def extract_frames(start_secs, end_secs, vids_folder, filename, out_folder, base_fn):
    # Create fp for detection video
    if filename.startswith('F'):
        filename = filename[1:]

    vid_name = filename + ".MOV"
    vid_fp = os.path.join(vids_folder, vid_name)

    # Pull an additional 10 frames before and after start time
    start_frame = start_secs - 10
    end_frame = end_secs + 10

    # If the observation is only one second of the video...
    if start_secs == end_secs:
        # Add the fps (30) to the end frame and an additional 10 frames
        end_frame = end_secs + 30

    # Read the video
    video = cv2.VideoCapture(vid_fp)

    # Set the start of the video to the start frame
    video.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    # Initialize frame number
    current_frame = start_frame

    while current_frame <= end_frame:
        # Read the frame
        ret, frame = video.read()

        if not ret:
            arcpy.AddMessage(f"End of video: {vid_fp}")
            break

        if current_frame % 2 == 0:
            # Create file name
            fn = f"{base_fn}{current_frame}.jpg"

            # And a file path
            fp = os.path.join(out_folder, fn)

            # Write the frame as an  image
            cv2.imwrite(fp, frame)

            # Increment
        current_frame += 1

    video.release()
    cv2.destroyAllWindows()


def extract_frames_two_fcs(start_values, fc_names, fc_names_unique, loop_num, det_num, vids_folder, out_folder):
    # Get the index of the second FC_Name
    second_fc_name = fc_names_unique[1]
    second_fc_index = fc_names.index(second_fc_name)

    # Subset the start values list
    first_start_values = start_values[:second_fc_index]
    second_start_values = start_values[second_fc_index:]
    start_values_lists = [first_start_values, second_start_values]

    # Loop through lists
    for i in range(len(start_values_lists)):
        # Get min and max start values
        min_value = min(start_values_lists[i])
        max_value = max(start_values_lists[i])

        # Get SRT fc name and remove the first character and create base file name
        fc_name = fc_names_unique[i][1:]
        ovlp_base_fn = f"{fc_name}_{loop_num}_overlap{det_num}_"

        # Extract frames from overlap video
        extract_frames(min_value, max_value, vids_folder, fc_name, out_folder, ovlp_base_fn)
