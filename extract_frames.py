import pandas as pd
import tkinter as tk
from tkinter import filedialog
import os
import cv2


# === FUNCTION TO EXTRACT FRAMES === #
def extract_frames(df_row, out_folder):
    # Pull out data
    vid_fp = df_row['Filepath']
    vid_type = df_row['Type']
    start_secs = df_row['Start']
    end_secs = df_row['End']

    # Create folder path for subfolder (separate detection and overlap)
    out_subfolder = os.path.join(out_folder, vid_type)
    if not os.path.exists(out_subfolder):
        os.makedirs(out_subfolder)


    # Create frame file base name
    vid_fn = os.path.basename(vid_fp)[:-4]
    base_fn = f"{vid_fn}_{vid_type}{df_row['DetectionNum']}_"

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
            fn = f"{base_fn}{current_frame}.jpg"

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

frames_folder = filedialog.askdirectory(title="Select a output folder for frames")

# Read the selected CSV
det_ovrlp_csv = pd.read_csv(det_ovrlp_fp)

# Loop through rows of the data frame
for index, row in det_ovrlp_csv.iterrows():
    # Get loop number, create output folder path for frames
    loop_num = row['LoopNum']
    output_folder = os.path.join(frames_folder, loop_num)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    extract_frames(row, output_folder)
