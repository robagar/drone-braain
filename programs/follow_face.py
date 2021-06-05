#!/usr/bin/env python3

import asyncio
import jetson.inference
from jetson_tello import run_jetson_tello_app
from drone_braain import video_x_to_local_azimuth


face_detector = jetson.inference.detectNet("facenet", threshold=0.5)

face = None
face_detected = asyncio.Condition()


async def detect_faces(drone, frame, cuda):
    global face
    face_detections = face_detector.Detect(cuda)

    for f in face_detections:
        try: 
            await face_detected.acquire()
            face = f 
            face_detected.notify()
        finally:
            face_detected.release()


async def fly(drone):
    await drone.takeoff()
    while True:
        try: 
            await face_detected.acquire()
            await face_detected.wait()
            print(face)
            x,y = face.Center
            turn_angle = video_x_to_local_azimuth(x)
        finally:
            face_detected.release()
        print(f'[drone] TURN {turn_angle}')
        await drone.turn_clockwise(turn_angle)


run_jetson_tello_app(fly, process_frame=detect_faces)