# Deep Learning Takes Flight: Detecting Jackrabbits with Thermal Drone Imagery
![010148_jackrabbit_likely_frame22026](https://github.com/user-attachments/assets/6a4e70af-4286-4471-8c49-4657f0d53388)

## Confirming Jackrabbit Detections

### Background
The Morley Nelson Snake River Birds of Prey National Conservation Area is nearly half a million acres and is home to many different species. Black-tailed jackrabbits are an important prey species, especially to coyotes and golden eagles. They are the preferred prey for golden eagles, but recently, the golden eagle diet has shifted from primarily jackrabbits to other prey. Prey that carry diseases and parasites. As a result, less golden eagle chicks are surviving. Is their diet shifting because there are fewer jackrabbits at the NCA? We don’t know because jackrabbit abundance hasn’t been surveyed since 1997. Spotlight surveys are as not effective in sagebrush steppes because the sagebrush limits visibility and can lead to inaccurate abundance estimations. We wanted to see if drones could be used to detect jackrabbits instead of spotlight surveys.

### Project
In 2024, we flew 3-6 flights on four different nights to obtain thermal drone footage. The flights were flown at 40 meters above ground level with the camera pointed straight down. We flew at night to maximize the contrast between the jackrabbit's body temperature and the background environment. An observer manually identified jackrabbits in the videos. These manual observations were used to label video frames to create a dataset using CVAT. The dataset was used to train and test a YOLOv5 model to automatically detect jackrabbits in the thermal footage. A Jupyter Notebook with the code used to extract the video frames and train and the test the model will be uploaded to the repository soon. 

Since we flew at night, not all jackrabbit detections, whether manual identified or detected by the model, could be confirmed with visible/RGB video. In an effort to confirm the detections, we plan to compare video frames from two different flights at the same location. If the potential jackrabbit detection appears in both videos, it is a false detection. If the potential jackrabbit only appears in the one video, it is a true and confirmed detection. The Python scripts in this repository are in development to create an ArcGIS Pro geoprocessing tool automate the workflow of matching the video frames of a detection in Video 1 to the video frames in Video 2, with the Video 2 flight path being the same as Video 1 but at a different time or day. Then we will compare the frames from each video determine if the detection is true or false.

Below are images to illustrate the jackrabbit detection confirmation method describe above. The images in the first example are from the same video and are for demonstration purposes only; same with the second example.

<img src="https://github.com/user-attachments/assets/7ce5d137-ef50-49cd-b8d6-dca509332f3f" width="400">          <img src="https://github.com/user-attachments/assets/a810de47-f94c-46a0-b95c-6caaf8c57e15" width="400">

*Example 1 - The potential jackrabbit detection is on the left from Video 1. If the jackrabbit does not appear at the same location in Video 2, the detection is confirmed.*

<img src="https://github.com/user-attachments/assets/5e336a60-69ea-4bac-a563-aa8f8cd5bad1" width="400">          <img src="https://github.com/user-attachments/assets/24e22103-c74a-4491-8851-a7e85cf2e978" width="400">

*Example 2 - The potential jackrabbit detection is on the left from Video 1. The same "blob" appears in at the same location in Video 2; the detection was a false positive.*
