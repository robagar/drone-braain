from tello_asyncio import VIDEO_WIDTH, VIDEO_HEIGHT


# Tello camera field of view measured (roughly) in degrees
CAMERA_HORIZONTAL_HALF_FOV = 26.9
CAMERA_VERTICAL_HALF_FOV = 20.2

HALF_VIDEO_WIDTH = VIDEO_WIDTH / 2
HALF_VIDEO_HEIGHT = VIDEO_HEIGHT / 2

def video_x_to_local_azimuth(x):
    return CAMERA_HORIZONTAL_HALF_FOV * (x - HALF_VIDEO_WIDTH) / HALF_VIDEO_WIDTH

def video_y_to_local_altitude(y):
    return -CAMERA_VERTICAL_HALF_FOV * (y - HALF_VIDEO_HEIGHT) / HALF_VIDEO_HEIGHT
