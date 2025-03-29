import pandas as pd
import tkinter as tk
from tkinter import filedialog
import os
import functions

from main import loop_num

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
    loop_num = row["LoopNum"]
    output_folder = os.path.join(frames_folder, loop_num)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    functions.extract_frames(row, output_folder)
