import argparse
import pyrealsense2 as rs
import numpy as np
import cv2
import os

def convert_bag_to_mp4(file_name, fps=30, width=1280, height=720,output_file_name='output.mp4'):
    '''
    generate mp4 file from a bag file
    '''
    try:
        pipeline = rs.pipeline()
        config = rs.config()
        rs.config.enable_device_from_file(config, file_name, repeat_playback=False)
        prof = pipeline.start(config)
        device = prof.get_device().as_playback()
        device.set_real_time(False)

        #set config for recorded realsense data
        config.enable_stream(rs.stream.depth, width, height, rs.format.z16, fps)
        config.enable_stream(rs.stream.color, width, height, rs.format.rgb8, fps)
        playback = rs.playback(device)
        i = 0

        # Make instance for VideoWriter
        fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
        writer = cv2.VideoWriter(output_file_name, fourcc, fps, (width, height))
        print("Opening bag file: {}".format(file_name))
        while True:
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            color_image = np.asanyarray(color_frame.get_data())
            color_image = cv2.cvtColor(color_image, cv2.COLOR_RGB2BGR)
            writer.write(color_image)
            if playback.current_status() != rs.playback_status.playing:
                print('Reach to file end')
                break
    finally:
        print("mp4 file is generated")
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, help="Bag file to read")
    args = parser.parse_args()

    convert_bag_to_mp4(args.input)

