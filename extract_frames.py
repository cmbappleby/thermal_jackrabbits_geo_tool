import pandas as pd
import tkinter as tk
from tkinter import filedialog
import os
import cv2


# === FUNCTION TO EXTRACT FRAMES === #
def extract_frames(df_row, vids_folder, out_folder):
    # Pull out data
    vid_fn = df_row['Filename']
    vid_type = df_row['Type']
    start_secs = df_row['Start']
    end_secs = df_row['End']

    # Create video fp
    vid_fp = os.path.join(vids_folder, f"{vid_fn}.MOV")

    # Create folder path for subfolder (separate detection and overlap)
    out_subfolder = os.path.join(out_folder, vid_type)
    if not os.path.exists(out_subfolder):
        os.makedirs(out_subfolder)

    # Pull an additional 10 frames before and after start time
    start_frame = start_secs * 30 - 10
    end_frame = end_secs * 30 + 10

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
            print(f"End of video: {vid_fp}")
            break

        if current_frame % 2 == 0:
            # Create file name
            fn = f"{vid_fn}_{current_frame}.jpg"

            # And a file path
            fp = os.path.join(out_subfolder, fn)

            # Write the frame as an  image
            cv2.imwrite(fp, frame)

            # Increment
        current_frame += 1

    video.release()
    cv2.destroyAllWindows()

# === SELECT FILES AND PROCESS CSV === #
# Hide the root window
root = tk.Tk()
root.withdraw()

# Open file explorer and allow user to select a file
det_ovrlp_fp = filedialog.askopenfilename(
    title="Select detection-overlap CSV file",
    filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
)

vids_folder = filedialog.askdirectory(title="Select folder containing videos")

frames_folder = filedialog.askdirectory(title="Select a output folder for frames")

# Read the selected CSV
det_ovrlp_csv = pd.read_csv(det_ovrlp_fp)

# Loop through rows of the data frame
for index, row in det_ovrlp_csv.iterrows():
    # If it's a detection, create a folder for the detection with the file base name
    if row['Type'] == "detection":
        # Get file base name sans extension
        vid_name = row['Filename']

        # Get a list of folders in the frames folder
        folder_list = os.listdir(frames_folder)
        # See how many folders are from the same file
        count = sum(1 for folder in folder_list if folder.startswith(vid_name))

        # If there are more than one, modify the folder name
        if count > 0:
            det_folder_name = f"{vid_name}_{count}"
        else:
            det_folder_name = vid_name

        # Create the folder
        det_folder_path = os.path.join(frames_folder, det_folder_name)
        os.makedirs(det_folder_path)

        # Create a folder to hold confirmation frames (used later)
        os.mkdir(os.path.join(det_folder_path, "confirmation"))

        extract_frames(row, vids_folder, det_folder_path)

    if det_folder_path:
        extract_frames(row, vids_folder, det_folder_path)
