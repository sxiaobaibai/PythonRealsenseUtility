import argparse
import pyrealsense2 as rs
import numpy as np
import cv2
import os


def main():
    if not os.path.exists(args.directory):
        os.mkdir(args.directory)
    try:

        pipeline = rs.pipeline()
        config = rs.config()
        rs.config.enable_device_from_file(config, args.input, repeat_playback=False)
        prof = pipeline.start(config)
        device = prof.get_device().as_playback()
        device.set_real_time(False)


        config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 1280, 720, rs.format.rgb8, 30)
        #device = pipeline.get_active_profile().get_device()
        playback = rs.playback(device)
        i = 0
        while True:
            print("Saving frame:", i)
            frames = pipeline.wait_for_frames()
            #depth_frame = frames.get_depth_frame()
            depth_frame = frames.get_color_frame()
            depth_image = np.asanyarray(depth_frame.get_data())
            cv2.imwrite(args.directory + "/" + str(i).zfill(6) + ".png", depth_image)
            i += 1
            #print(playback.current_status())
            #print(rs.playback_status.playing)
            if playback.current_status() != rs.playback_status.playing:
                break
            # grab and process frames
    finally:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", type=str, help="Path to save the images")
    parser.add_argument("-i", "--input", type=str, help="Bag file to read")
    args = parser.parse_args()

    main()
