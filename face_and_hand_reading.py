import mediapipe as mp, cv2

from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from collections import Counter, deque



class HandDetection:


    def __init__ (self) -> None:

        base_options = python.BaseOptions(
            model_asset_path = "hand_landmarker.task"
        )
        
        options = vision.HandLandmarkerOptions(
            base_options = base_options,
            running_mode = vision.RunningMode.VIDEO,
            num_hands = 1,
        )

        self.landmarker = vision.HandLandmarker.create_from_options(options)
        self.direction = "NONE"
        self.direction_history = deque(maxlen = 10)


    def get_tracked_direction(self, hand) -> str:

        avg_x = (hand[5].x + hand[9].x + hand[13].x + hand[17].x) / 4
        avg_y = (hand[5].y + hand[9].y + hand[13].y + hand[17].y) / 4
        
        dir_x = avg_x - hand[0].x
        dir_y = avg_y - hand[0].y

        # #for debugging
        # print(f"dir_x={dir_x:.4f}, dir_y={dir_y:.4f},")

        if abs(dir_x) > (abs(dir_y) * 1.5):
            if dir_x > 0:
                return "LEFT"
            elif dir_x < 0:
                return "RIGHT"
            
        if abs(dir_y) > (abs(dir_x) * 1.5):
            if dir_y > 0:
                return "DOWN"
            elif dir_y < 0:
                return "UP"
        
        return "NONE"
    

    def update(self, frame, timestamp_ms, man_dir_check):

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(
            image_format = mp.ImageFormat.SRGB,
            data = rgb_frame
        )
        
        result = self.landmarker.detect_for_video(mp_image, timestamp_ms)

        if result.hand_landmarks and man_dir_check:
            detected_direction = self.get_tracked_direction(result.hand_landmarks[0])
            self.direction_history.append(detected_direction)

            # for debugging:
            # print(f"count in dir history: {len(self.direction_history)}")

            direction_counts = Counter(self.direction_history)
            self.direction = direction_counts.most_common(1)[0][0]
        elif man_dir_check:
            self.direction = "NONE"
        
        if not man_dir_check:
            self.direction_history.clear()

        return result
    
    
    def get_direction(self) -> str:

        return self.direction


    def draw(self, frame, result) -> None:

        if not result.hand_landmarks:
            return
        
        h, w, _ = frame.shape

        for hand in result.hand_landmarks:

            for landmark in hand:

                x = int(landmark.x * w)
                y = int(landmark.y * h)

                cv2.circle(
                    frame,
                    (x, y),
                    5,
                    (0, 255, 0),
                    -1
                )



class FaceDetection:


    def __init__ (self) -> None:

        base_options = python.BaseOptions(
            model_asset_path = "face_landmarker.task"
        )
        
        options = vision.FaceLandmarkerOptions(
            base_options = base_options,
            running_mode = vision.RunningMode.VIDEO,
            num_faces = 1,
        )

        self.landmarker = (vision.FaceLandmarker.create_from_options(options))
        self.direction = "NONE"
        self.direction_history = deque(maxlen = 10)

    
    def get_tracked_direction(self, face) -> str:

        nose_tip_point = face[1]
        left_cheek_point = face[234]
        right_cheek_point = face[454]
        forehead_point = face[10]
        chin_point = face[152]

        center_x = (left_cheek_point.x + right_cheek_point.x) / 2
        center_y = (forehead_point.y + chin_point.y) / 2

        dir_x = nose_tip_point.x - center_x
        dir_y = nose_tip_point.y - center_y

        
        ##for debugging
        #print(f"dir_x={dir_x:.4f}, dir_y={dir_y:.4f}")

        if abs(dir_x) > (abs(dir_y) * 1.5):
            if dir_x > 0:
                return "LEFT"
            else:
                return "RIGHT"
        elif abs(dir_y) > abs(dir_x):
            if dir_y > 0:
                return "DOWN"
            else:
                return "UP"

        return "NONE"


    def update(self, frame, timestamp_ms, man_dir_check):

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(
            image_format = mp.ImageFormat.SRGB,
            data = rgb_frame
        )
        
        result = self.landmarker.detect_for_video(mp_image, timestamp_ms)

        if result.face_landmarks and man_dir_check:
            detected_direction = self.get_tracked_direction(result.face_landmarks[0])
            self.direction_history.append(detected_direction)

            ##for debugging:
            #print(f"count in dir history: {len(self.direction_history)}")

            direction_counts = Counter(self.direction_history)
            self.direction = direction_counts.most_common(1)[0][0]
        elif man_dir_check:
            self.direction = "NONE"

        if not man_dir_check:
            self.direction_history.clear()

        return result


    def get_direction(self) -> str:

        return self.direction
    

    def draw(self, frame, result) -> None:
        
        if not result.face_landmarks:
            return
        
        h, w, _ = frame.shape

        for face in result.face_landmarks:
            
            for point in face:
                x = int(point.x * w)
                y = int(point.y * h)

                cv2.circle(
                    frame,
                    (x, y),
                    5,
                    (0, 255, 0),
                    -1
                )