#!/usr/bin/env python3

import asyncio
import jetson.inference
from jetson_tello import h264_frame_to_cuda, FrameDecodeError
from tello_asyncio import Tello
from drone_braain import World, WorldObserver, get_coco_class_by_name

net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)

human = None
human_detected = asyncio.Condition()

class HumanObserver(WorldObserver):
    human_class = get_coco_class_by_name("person")

    async def on_thing_detected(self, thing, is_new_thing):
        global human
        if thing.coco_class is self.human_class:
            print(('NEW ' if is_new_thing else '') + f'HUMAN at {thing.local_azimuth:.1f}')
            try: 
                await human_detected.acquire()
                human = thing 
                human_detected.notify()
            finally:
                human_detected.release()


world = World(HumanObserver())

async def process_frame(frame):
    try:
        cuda, width, height = h264_frame_to_cuda(frame)

        detections = net.Detect(cuda)

        await world.update_things(detections)

    except FrameDecodeError:
        pass    

async def main():
    global next_frame

    drone = Tello()

    async def turn(angle):
        a = round(angle)
        if a >= 1:
            await drone.turn_clockwise(a)
        elif a <= -1:
            await drone.turn_counterclockwise(-a)

    await drone.connect()
    await drone.start_video()

    async def fly():
        await drone.takeoff()
        while True:
            try: 
                await human_detected.acquire()
                await human_detected.wait()
                turn_angle = human.local_azimuth
            finally:
                human_detected.release()
            print(f'[drone] TURN {turn_angle}')
            await turn(turn_angle)

    async def process_video():
        async for frame in drone.video_stream:
            await process_frame(frame)

    try:
        await asyncio.wait([fly(), process_video()])
    finally:
        await drone.stop_video()
        await drone.disconnect()

# Python 3.7+
#asyncio.run(main())
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
