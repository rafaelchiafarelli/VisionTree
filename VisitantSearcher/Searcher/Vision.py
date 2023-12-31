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
import os
import mediapipe as mp
import numpy as np
import numpy as np
import uuid
import json
from Searcher.Constants import landmark_names as names
class Vision:
    def __init__(self,debug, static_image_mode, model_complexity, enable_segmentation,min_detection_confidence, destination) -> None:
        print("start vision")
        self.debug = debug
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=static_image_mode,
            model_complexity=model_complexity,
            enable_segmentation=enable_segmentation,
            min_detection_confidence=min_detection_confidence)
        self.destination = destination
        self.base_options = python.BaseOptions(model_asset_path='./assets/face_landmarker_v2_with_blendshapes.task')
        self.options = vision.FaceLandmarkerOptions(base_options=self.base_options,
                                            output_face_blendshapes=True,
                                            output_facial_transformation_matrixes=True,
                                            num_faces=1)
        self.detector = vision.FaceLandmarker.create_from_options(self.options)
    
    def search_body(self, file_path):
        # For static images:
        BG_COLOR = (192, 192, 192) # gray

        image = cv2.imread(file_path)
        image_height, image_width, _ = image.shape

        # Convert the BGR image to RGB before processing.
        results = self.pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        UUID=uuid.uuid4()
        
        if not results.pose_landmarks:
            #print("no landmarks -- disregard")
            return (False,UUID,{})

        landmarks = {}
        landmarks["width"]  = image.shape[0]
        landmarks["height"]  = image.shape[1]
    
        head_visible = False
        for idx,landmark in enumerate(results.pose_landmarks.landmark):
            if idx < 7:
                if landmark.visibility < 0.7: 
                    #print("landmark {} not visible, disregard.".format(names[idx]))
                    return (False,UUID,{})
            
            if idx <= names.__len__():
                landmarks[names[idx]] =[
                                        landmark.x,
                                        landmark.y,
                                        landmark.z,
                                        landmark.visibility]
            else:
                #print("error in landmark index -- out of bounds idx:{}".format(idx))
                return (False,UUID,{})
        #calculate the size of the head considering the distance of the ears            
        if landmarks["left_ear"][0] - landmarks["right_ear"][0] < 0.07 or landmarks["left_ear"][0] - landmarks["right_ear"][0] > 0.30:
            #print("not a good sized head {}".format(UUID))
            return (False,UUID,{})
        #calculate if the head is above the shoulder considering the sholder avereage high and the nose
        if (landmarks["left_shoulder"][3]>0.5 and 
            landmarks["right_shoulder"][3]>0.5 and
            (landmarks["left_shoulder"][1] + landmarks["right_shoulder"][1])/2 <= landmarks["nose"][1]):
            #print("error - shoulder above the nose {}".format(UUID))
            return (False,UUID,{})
        #print("head {} is a GOOD HEAD".format(UUID))
        
        with open("{}/{}.metadata".format(self.destination,UUID), "w") as metadata:
            metadata.write(json.dumps(landmarks,indent=4))

        annotated_image = image.copy()
        segmented_image = image.copy()
        # Draw segmentation on the image.
        # To improve segmentation around boundaries, consider applying a joint
        # bilateral filter to "results.segmentation_mask" with "image".
        condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
        bg_image = np.zeros(image.shape, dtype=np.uint8)
        bg_image[:] = BG_COLOR
        segmented_image = np.where(condition, segmented_image, bg_image)
        
        # Draw pose landmarks on the image.
        self.mp_drawing.draw_landmarks(
            annotated_image,
            results.pose_landmarks,
            self.mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style())
        if self.debug:
            cv2.imshow("pose landmarks", annotated_image) 
            cv2.waitKey(10) 
        
        # calculate if the face is turned to the camera
        if landmarks["left_ear"][0] < landmarks["nose"][0]:
            
            print("face turned left -- do not use")
            return (False,UUID,{})
        if landmarks["right_ear"][0] > landmarks["nose"][0]:
            print("face turned right -- do not use")
            return (False,UUID,{})
        if landmarks["mounth_left"][1] < landmarks["nose"][1]:
            print("face upside down -- do not use")
            return (False,UUID,{})
        if landmarks["mounth_right"][1] < landmarks["nose"][1]:
            print("face upside down -- do not use")
            return (False,UUID,{})        
        # calculate the distance of the ears. if it is lower than a threshold, eliminates it
        
        #print('{}/{}.png'.format(destination,UUID))


        cv2.imwrite('{}/annotated{}.png'.format(self.destination,UUID), annotated_image)
        cv2.imwrite('{}/segmented{}.png'.format(self.destination,UUID), segmented_image)
        cv2.imwrite('{}/original{}.png'.format(self.destination,UUID), image)

        # Plot pose world landmarks.
        #self.mp_drawing.plot_landmarks(
        #    results.pose_world_landmarks, self.mp_pose.POSE_CONNECTIONS)
        return True,UUID, landmarks  
    
    def clean(self,UUID):
        os.remove('{}/annotated{}.png'.format(self.destination,UUID))
        os.remove('{}/segmented{}.png'.format(self.destination,UUID))
        os.remove('{}/original{}.png'.format(self.destination,UUID))
        os.remove("{}/{}.metadata".format(self.destination,UUID))


    def search_face(self, file_path):
        face_image = mp.Image.create_from_file(file_path)

        # STEP 4: Detect face landmarks from the input image.
        detection_result = self.detector.detect(face_image)
        
        # STEP 5: Process the detection result. In this case, visualize it.
        facemash_image = self.draw_landmarks_on_image(face_image.numpy_view(), detection_result)
        facemash_image = cv2.cvtColor(facemash_image,cv2.COLOR_BGR2RGB)
        if self.debug:
            cv2.imshow("facemesh",facemash_image)
            cv2.waitKey(10) 

        return facemash_image,detection_result
                

    def draw_landmarks_on_image(self,rgb_image, detection_result):
        face_landmarks_list = detection_result.face_landmarks
        annotated_image = np.copy(rgb_image)

        # Loop through the detected faces to visualize.
        for idx in range(len(face_landmarks_list)):
            face_landmarks = face_landmarks_list[idx]

            # Draw the face landmarks.
            face_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            face_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in face_landmarks
            ])

            solutions.drawing_utils.draw_landmarks(
                image=annotated_image,
                landmark_list=face_landmarks_proto,
                connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp.solutions.drawing_styles
                .get_default_face_mesh_tesselation_style())
            solutions.drawing_utils.draw_landmarks(
                image=annotated_image,
                landmark_list=face_landmarks_proto,
                connections=mp.solutions.face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp.solutions.drawing_styles
                .get_default_face_mesh_contours_style())
            solutions.drawing_utils.draw_landmarks(
                image=annotated_image,
                landmark_list=face_landmarks_proto,
                connections=mp.solutions.face_mesh.FACEMESH_IRISES,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp.solutions.drawing_styles
                .get_default_face_mesh_iris_connections_style())

        return annotated_image
