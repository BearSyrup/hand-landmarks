import cv2
import time
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.framework.formats import landmark_pb2
from mediapipe import solutions


# Config
MARGIN = 10  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
HANDEDNESS_TEXT_COLOR = (88, 205, 54)  # vibrant green


def draw_landmarks_on_image(rgb_image, detection_result):
    hand_landmarks_list = detection_result.hand_landmarks
    handedness_list = detection_result.handedness
    annotated_image = np.copy(rgb_image)

    # Loop through the detected hands to visualize.
    for idx in range(len(hand_landmarks_list)):
        hand_landmarks = hand_landmarks_list[idx]
        handedness = handedness_list[idx]

        # Draw the hand landmarks.
        hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        hand_landmarks_proto.landmark.extend(
            [
                landmark_pb2.NormalizedLandmark(
                    x=landmark.x, y=landmark.y, z=landmark.z
                )
                for landmark in hand_landmarks
            ]
        )
        solutions.drawing_utils.draw_landmarks(
            annotated_image,
            hand_landmarks_proto,
            solutions.hands.HAND_CONNECTIONS,
            solutions.drawing_styles.get_default_hand_landmarks_style(),
            solutions.drawing_styles.get_default_hand_connections_style(),
        )

        # Get the top left corner of the detected hand's bounding box.
        height, width, _ = annotated_image.shape
        x_coordinates = [landmark.x for landmark in hand_landmarks]
        y_coordinates = [landmark.y for landmark in hand_landmarks]
        text_x = int(min(x_coordinates) * width)
        text_y = int(min(y_coordinates) * height) - MARGIN

        # Draw handedness (left or right hand) on the image.
        cv2.putText(
            annotated_image,
            f"{handedness[0].category_name}",
            (text_x, text_y),
            cv2.FONT_HERSHEY_DUPLEX,
            FONT_SIZE,
            HANDEDNESS_TEXT_COLOR,
            FONT_THICKNESS,
            cv2.LINE_AA,
        )

    return annotated_image


def main():
    capture_video()


RESULT = None
IMG = None


def detector_callback(
    result: vision.HandLandmarkerResult, output_image: mp.Image, time_stamp_ms: int
):
    global RESULT
    global IMG
    IMG = result
    RESULT = output_image


def capture_video():
    cam = cv2.VideoCapture(0)
    frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_heigth = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # output the video with a codec
    # fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    # out = cv2.VideoWriter("output.mp4", fourcc, 20, (frame_width, frame_heigth))
    base_options = python.BaseOptions(
        model_asset_path="hand_landmarker.task",
    )
    options = vision.HandLandmarkerOptions(
        base_options=base_options,
        num_hands=2,
        running_mode=mp.tasks.vision.RunningMode.LIVE_STREAM,
        result_callback=detector_callback,
    )
    detector = vision.HandLandmarker.create_from_options(options)
    time_stamp = 0
    while True:
        ret, frame = cam.read()
        if not ret:
            print("fail to get frame")
            break

        time_stamp += 1
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        detector.detect_async(mp_image, time_stamp)
        time.sleep(0.05)
        annotated_image = draw_landmarks_on_image(RESULT.numpy_view(), IMG)
        cv2.imshow("Camera", annotated_image)

        if cv2.waitKey(1) == ord("q"):
            break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
