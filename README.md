# Deep Learning Takes Flight: Detecting Jackrabbits with Thermal Drone Imagery
![010148_jackrabbit_likely_frame22026](https://github.com/user-attachments/assets/6a4e70af-4286-4471-8c49-4657f0d53388)

## Confirming Jackrabbit Detections

### Background
The Morley Nelson Snake River Birds of Prey National Conservation Area is nearly half a million acres and is home to many different species. Black-tailed jackrabbits are an important prey species, especially to coyotes and golden eagles. They are the preferred prey for golden eagles, but recently, the golden eagle diet has shifted from primarily jackrabbits to other prey. Prey that carry diseases and parasites. As a result, less golden eagle chicks are surviving. Is their diet shifting because there are fewer jackrabbits at the NCA? We don’t know because jackrabbit abundance hasn’t been surveyed since 1997. Spotlight surveys are as not effective in sagebrush steppes because the sagebrush limits visibility and can lead to inaccurate abundance estimations. We wanted to see if drones could be used to detect jackrabbits instead of spotlight surveys.

### Project
In 2024, we flew 3-6 flights on four different nights to obtain thermal drone footage. The flights were flown at 40 meters above ground level with the camera pointed straight down. We flew at night to maximize the contrast between the jackrabbit's body temperature and the background environment. An observer manually identified jackrabbits in the videos. These manual observations were used to label video frames to create a dataset using CVAT. The dataset was used to train and test a YOLOv5 model to automatically detect jackrabbits in the thermal footage. A Jupyter Notebook with the code used to extract the video frames and train and the test the model will be uploaded to the repository soon. 

Since we flew at night, not all jackrabbit detections, whether manual identified or detected by the model, could be confirmed with visible/RGB video. In an effort to confirm the detections, we plan to compare video frames from two different flights at the same location. If the potential jackrabbit detection appears in both videos, it is a false detection. If the potential jackrabbit only appears in the one video, it is a true and confirmed detection. The geotool.py Python is a script to create an ArcGIS Pro geoprocessing tool to automate the workflow of matching the video times of a detection in Video 1 to the video times in Video 2, with the Video 2 flight path being the same as Video 1 but at a different time or day. The output of the geoprocessing tool is a CSV with the video file paths and start and end times of the detections for the detection and overlapping videos, along with some data. The frames are extracted by executing extract_frames.py.

Below are images to illustrate the jackrabbit detection confirmation method describe above. The images in the examples are an actual comparison of two different videos.

<img src="https://github.com/user-attachments/assets/d995b4c4-31a0-4ce4-864d-106cfe455350" width="400">          <img src="https://github.com/user-attachments/assets/b74d52c9-57c3-4a47-83d4-77e2f7848b90" width="400">

*Example 1 - The potential jackrabbit detection is on the left from Video 1. The same "blob" appears at the same location in Video 2; the detection was a false positive.*

<img src="https://github.com/user-attachments/assets/6cb63d90-12cd-452d-99f7-53a411441790" width="400">          <img src="https://github.com/user-attachments/assets/7dd88af9-fd29-4b8c-a0ac-366869ae711e" width="400">

*Example 2 - The potential jackrabbit detection is on the left from Video 1. The same "blob" does not appear at the same location in Video 2; the detection was a true positive.*
