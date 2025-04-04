import math
import pandas as pd


def time_to_sec(timestamp, ts_type):
    minute, sec = map(int, timestamp.split(":"))
    time_sec = minute * 60 + sec
    if ts_type == 'End':
        real_sec = math.ceil(time_sec * 0.6)
    else:
        real_sec = math.floor(time_sec * 0.6)

    return real_sec


def real_time(real_sec):
    real_ts = f"{real_sec // 60:02}:{real_sec % 60:02}"

    return real_ts


def clean_obs(obs_df):
    # Filter obs to only 3rd and 4th nights, rename and format columns
    obs_3_4_df = obs_df[obs_df['Flight_ID'] > 3000]
    obs_3_4_df = obs_3_4_df.rename(columns={'Video_Frame_Start': 'Start', 'Video_Frame_End': 'End'})
    obs_3_4_df['Start'] = pd.to_datetime(obs_3_4_df['Start'], format='%M:%S:%f').dt.strftime('%M:%S')
    obs_3_4_df['End'] = pd.to_datetime(obs_3_4_df['End'], format='%M:%S:%f').dt.strftime('%M:%S')

    # Convert timestamp to seconds and adjust for ClipChamp's weird timestamps
    obs_3_4_df['StartSec'] = obs_3_4_df.apply(lambda row: time_to_sec(row['Start'], 'Start'), axis=1)
    obs_3_4_df['EndSec'] = obs_3_4_df.apply(lambda row: time_to_sec(row['End'], 'End'), axis=1)
    obs_3_4_df['Start'] = obs_3_4_df['StartSec'].apply(real_time)
    obs_3_4_df['End'] = obs_3_4_df['EndSec'].apply(real_time)

    return obs_3_4_df
