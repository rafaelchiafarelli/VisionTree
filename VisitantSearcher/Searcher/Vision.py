"""Vision module
Loads all libraries related to vision, such as mediapipe,
has a function to detect all features
will receive the image as a file name, a folder to store the result
this function will return a uuid of the detection or None.

if there is a human, detect the head
if there is a head and it is looking this way, then return the uuid and save the metadata
return None otherwise
"""
import cv2
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2

# STEP 1: Import the necessary modules.
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import mediapipe as mp
import numpy as np
import numpy as np
import uuid
import json
from Searcher.Constants import landmark_names as names
class Vision:
    def __init__(self, static_image_mode, model_complexity, enable_segmentation,min_detection_confidence) -> None:
        print("start vision")
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=static_image_mode,
            model_complexity=model_complexity,
            enable_segmentation=enable_segmentation,
            min_detection_confidence=min_detection_confidence)
        

    
    def run(self, file_path, destination ):
        # For static images:
        BG_COLOR = (192, 192, 192) # gray

        image = cv2.imread(file_path)
        image_height, image_width, _ = image.shape
        # Convert the BGR image to RGB before processing.
        results = self.pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        if not results.pose_landmarks:
            return None

        UUID=uuid.uuid4()
        with open("{}/{}.metadata".format(destination,UUID), "w") as metadata:
            landmarks = []
            for idx,landmark in enumerate(results.pose_landmarks.landmark):
                print(landmark)
                if idx <= names.__len__():
                    landmarks.append({
                        
                        names[idx]:[
                            {"x":landmark.x},
                            {"y":landmark.y},
                            {"z":landmark.z},
                            {"visibility":landmark.visibility}]})
                else:
                    print("error in landmark index -- out of bounds idx:{}".format(idx))
            metadata.write(json.dumps(landmarks,indent=4))
        annotated_image = image.copy()
        # Draw segmentation on the image.
        # To improve segmentation around boundaries, consider applying a joint
        # bilateral filter to "results.segmentation_mask" with "image".
        condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
        bg_image = np.zeros(image.shape, dtype=np.uint8)
        bg_image[:] = BG_COLOR
        annotated_image = np.where(condition, annotated_image, bg_image)
        # Draw pose landmarks on the image.
        self.mp_drawing.draw_landmarks(
            annotated_image,
            results.pose_landmarks,
            self.mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style())
        cv2.imwrite('{}/{}.png'.format(destination,UUID), annotated_image)
        # Plot pose world landmarks.
        self.mp_drawing.plot_landmarks(
            results.pose_world_landmarks, self.mp_pose.POSE_CONNECTIONS)
        return UUID