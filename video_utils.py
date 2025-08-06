# video_utils.py

import cv2
import os

def extract_keyframes(video_path, output_dir="frames", timestamp_sec=5):
    """
    Extracts a single keyframe from the video.
    If the given timestamp exceeds the video duration, it picks the middle frame.
    """
    os.makedirs(output_dir, exist_ok=True)
    vidcap = cv2.VideoCapture(video_path)
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    target_frame = int(fps * timestamp_sec)

    # Fallback: if timestamp is beyond video length, use middle frame
    if target_frame >= total_frames:
        target_frame = total_frames // 2

    # Go to the target frame
    vidcap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
    success, image = vidcap.read()
    if success:
        filename = os.path.join(output_dir, "frame0.jpg")
        cv2.imwrite(filename, image)
        vidcap.release()
        return [filename]
    else:
        vidcap.release()
        return []

def describe_frame(frame_path):
    """
    Generates a description for a given frame.
    This is interpreted by Gemini or any vision model as a visual input.
    """
    return f"This image shows part of a pet product shelf from a retail store. Analyze it for planogram compliance. Image path: {frame_path}"
