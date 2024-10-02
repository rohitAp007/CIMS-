import hashlib
import ffmpeg

# Calculate the MD5 hash of the file
def calculate_file_hash(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# Extract video metadata using ffmpeg
def get_video_metadata(video_path):
    try:
        probe = ffmpeg.probe(video_path)
        video_streams = [stream for stream in probe['streams'] if stream['codec_type'] == 'video']
        if len(video_streams) > 0:
            video_metadata = video_streams[0]
            return {
                'resolution': f"{video_metadata['width']}x{video_metadata['height']}",
                'fps': eval(video_metadata['r_frame_rate']),  # fps might be in fractional form
                'codec': video_metadata['codec_name'],
                'duration': float(video_metadata['duration'])  # duration in seconds
            }
        return None
    except ffmpeg.Error as e:
        print(f"Error extracting metadata: {e}")
        return None

# Load the original file hash stored at the time of upload
def load_original_hash(video_path):
    try:
        with open(f"{video_path}.hash", 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

# Compare the video metadata with expected values
def check_metadata(video_path):
    metadata = get_video_metadata(video_path)
    if not metadata:
        return False  # Unable to extract metadata, assume tampering

    # Example of expected metadata (this can be stored at the upload time)
    expected_metadata = {'resolution': '1920x1080', 'fps': 30, 'codec': 'h264', 'duration': 300}

    # Check for differences in metadata
    return (
        metadata['resolution'] == expected_metadata['resolution'] and
        abs(metadata['fps'] - expected_metadata['fps']) < 0.5 and  # Allow slight differences in fps
        metadata['codec'] == expected_metadata['codec'] and
        abs(metadata['duration'] - expected_metadata['duration']) < 5  # Allow a small difference in duration
    )

# Detect tampering by comparing the file hash and metadata
def detect_tampering(video_path, original_hash):
    new_hash = calculate_file_hash(video_path)
    if new_hash != original_hash:
        print("Hash mismatch detected!")
        return True

    if not check_metadata(video_path):
        print("Metadata mismatch detected!")
        return True

    return False
