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

def estimate_face_distance(face):
    try:
        return round(100 * 50000 / face.Area)
    except Exception as e:
        print(f'{e}')


async def fly(drone):
    await drone.takeoff()
    while True:
        try: 
            await face_detected.acquire()
            await face_detected.wait()
            print(face)
            face_distance = estimate_face_distance(face) 
            print(f'estimated distance: {face_distance}cm')
            x,y = face.Center
            turn_angle = video_x_to_local_azimuth(x)
        finally:
            face_detected.release()
        print(f'[drone] TURN {turn_angle}')
        await drone.turn_clockwise(turn_angle)

        if face_distance < 40:
            await drone.move_back(40)
        if face_distance > 60:
            await drone.move_forward(min(face_distance - 40, 100))


run_jetson_tello_app(fly, process_frame=detect_faces)