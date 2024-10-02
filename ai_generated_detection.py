import cv2
import numpy as np

def detect_ai_generated_content(video_path):
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    ai_flag = False
    
    for i in range(frame_count):
        ret, frame = cap.read()
        if not ret:
            break
        
        # Calculate average color and its standard deviation
        avg_color_per_row = np.average(frame, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)
        color_std = np.std(avg_color)
        
        print(f"Frame {i}: Avg Color = {avg_color}, Std Dev = {color_std}")  # Debugging output
        
        # Check for uniformity
        if color_std < 10:  # Threshold for "uniformity"
            ai_flag = True
            break
    
    cap.release()
    return ai_flag

# Example usage:
video_path = "path_to_video.mp4"
if detect_ai_generated_content(video_path):
    print("AI-generated content detected!")
else:
    print("Video seems authentic.")
