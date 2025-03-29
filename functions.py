import arcpy
import cv2
import os


def extract_frames(start_secs, end_secs, vid_fp, frames_folder, base_fn):
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
    currentFrame = start_frame

    while currentFrame <= end_frame:
        # Read the frame
        ret, frame = video.read()

        if not ret:
            print(f"End of video or error: {vid_fp}")
            break

        if currentFrame % 2 == 0:
            # Create file name
            fn = f"{base_fn}{currentFrame}.jpg"

            # And a file path
            fp = os.path.join(frames_folder, fn)

            # Write the frame as an  image
            cv2.imwrite(fp, frame)

            # Increment
        currentFrame += 1

    video.release()
    cv2.destroyAllWindows()