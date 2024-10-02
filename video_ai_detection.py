import cv2
import numpy as np

def detect_ai_generated_content(video_path):
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    ai_flag = False
    
    # Variables for motion analysis
    prev_frame = None
    
    for i in range(frame_count):
        ret, frame = cap.read()
        if not ret:
            break
        
        # Color Uniformity Check
        avg_color_per_row = np.average(frame, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)
        color_std = np.std(avg_color)

        # Motion Analysis Check
        if prev_frame is not None:
            # Convert to grayscale for easier processing
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray_prev_frame = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
            
            # Calculate the absolute difference between frames
            motion = cv2.absdiff(gray_frame, gray_prev_frame)
            motion_avg = np.mean(motion)
            
            print(f"Frame {i}: Avg Color = {avg_color}, Std Dev = {color_std:.2f}, Motion Avg = {motion_avg:.2f}")  # Debugging output
            
            # Heuristic conditions for AI detection
            if color_std < 10 and motion_avg < 15:  # Thresholds can be adjusted
                ai_flag = True
                break
        
        # Update previous frame
        prev_frame = frame
    
    cap.release()
    return ai_flag

# Example usage:
if __name__ == "__main__":
    # List of test videos with their expected outcomes (True = AI-generated, False = Authentic)
    test_videos = [
        {"path": "path_to_authentic_video1.mp4", "expected": False},
        {"path": "path_to_ai_generated_video1.mp4", "expected": True},
        # Add more videos as needed
    ]

    for video in test_videos:
        print(f"Testing {video['path']}...")
        result = detect_ai_generated_content(video["path"])
        
        # Compare the result with the expected outcome
        if result == video["expected"]:
            print("Test Passed!")
        else:
            print("Test Failed!")
