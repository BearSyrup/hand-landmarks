# Hand Landmarks

A simple Python project for detecting hand landmarks using MediaPipe and OpenCV (cv2).

## Tools and Technologies

- **Python**
- **MediaPipe**
- **OpenCV (cv2)**

## Description

This project uses MediaPipe to detect hand landmarks in real-time video streams processed by OpenCV. Quick fix using global just to see it working and have some fun (it took too much time). I suppose mediapipe creates a new thread for inferences and for some reason it freezes cv2. This will be addressed in the future I guess.

## Future Improvements

- **Callback Implementation:**  
  Replace the global variable workaround with a proper callback function.
- **Blog Post:**  
  Write a detailed blog post explaining the project's design, challenges, and solutions.

## Installation

- **Use**
  Well, I create a makefile to use it but in the middle of the process learn about mamba and tried to use it. Everything is a mess. But worked!
  Hope someone trying mediapipe can see my Jerry-Rig go Horse solution and at least have fun using google's lib.

