import cv2
import os


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
