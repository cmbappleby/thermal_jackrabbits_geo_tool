import pandas as pd
import os


def time_to_sec(timestamp):
    minute, sec = map(int, timestamp.split(":"))
    time_sec = minute * 60 + sec

    return time_sec


# === EDIT THE FOLLOWING FILEPATHS (AND SHEET NUMBERS) === #
# Spreadsheet with the observations
obs_xlsx_fp = r"C:\Users\cowsp\OneDrive\ISU\Fall_24\jackrabbit_project\FlightOverlapDetectionBTJR\data\in_files\Observations_Pearson.xlsx"
# Sheet number for the observations (the first sheet is 0, second is 1, etc.)
obs_xlsx_sheet = 1

# Spreadsheet with the flight info
flight_csv_fp = r"C:\Users\cowsp\OneDrive\ISU\Fall_24\jackrabbit_project\FlightOverlapDetectionBTJR\data\in_files\flight_date_time.csv"

# CSV with temperature data
temp_csv_fp = r"C:\Users\cowsp\OneDrive\ISU\Fall_24\jackrabbit_project\FlightOverlapDetectionBTJR\data\in_files\temps_2024.csv"

# === READ THE FILES INTO PANDAS DATA FRAMES === #
# noinspection PyTypeChecker
obs_df = pd.read_excel(obs_xlsx_fp,
                       sheet_name=obs_xlsx_sheet,
                       usecols=['Flight_ID', 'Filename', 'Video_Frame_Start', 'Video_Frame_End', 'Certainty'])

flight_df = pd.read_csv(flight_csv_fp)
temp_df = pd.read_csv(temp_csv_fp)

# === CREATE AN OBS CSV WITH DESIRED DATA === #
# Join temps to flight info
flight_temp_df = flight_df.join(temp_df)

# Remove unnecessary rows and columns
flight_temp_df = flight_temp_df[flight_temp_df['Flight_ID'] > 3000]
flight_temp_df = flight_temp_df.drop(['Flight_Date', 'Flight_Start', 'wind_mph', 'wind_kmph'], axis=1)

# Filter obs to only 3rd and 4th nights, rename and format columns
obs_3_4_df = obs_df[obs_df['Flight_ID'] > 3000]
obs_3_4_df = obs_3_4_df.rename(columns={'Video_Frame_Start': 'Start', 'Video_Frame_End': 'End'})
obs_3_4_df['Start'] = pd.to_datetime(obs_3_4_df['Start'], format='%M:%S:%f').dt.strftime('%M:%S')
obs_3_4_df['End'] = pd.to_datetime(obs_3_4_df['End'], format='%M:%S:%f').dt.strftime('%M:%S')
obs_3_4_df['StartSec'] = obs_3_4_df['Start'].apply(time_to_sec)
obs_3_4_df['EndSec'] = obs_3_4_df['End'].apply(time_to_sec)

# Join obs to flight and temp info
flight_temp_obs_df = flight_temp_df.merge(obs_3_4_df, on='Flight_ID', how='right')

# Mutate filename
flight_temp_obs_df['Filename'] = flight_temp_obs_df['Filename'].apply(os.path.basename)
flight_temp_obs_df['Filename'] = flight_temp_obs_df['Filename'].str.split('_').str[:2].str.join('_')
flight_temp_obs_df['Filename'] = flight_temp_obs_df.apply(lambda row: f"{row['Flight_ID']}_{row['Filename']}", axis=1)

# Get folder path
out_folder = os.path.dirname(obs_xlsx_fp)
flight_temp_obs_df.to_csv(os.path.join(out_folder, "obs_for_geotool.csv"), index=False)
