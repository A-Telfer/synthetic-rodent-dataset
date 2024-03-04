"""Extract frames from the real videos"""

import cv2
import numpy as np
import logging 

from pathlib import Path
from typing import List, Tuple
from tqdm import tqdm
from PIL import Image

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

SEED = 42
TRAINING_FRAMES = 200
EVALUATION_FRAMES = 100

REAL_FRAMES_TRAINING_FOLDER = Path('data/real_frames/training')
REAL_FRAMES_TRAINING_FOLDER.mkdir(exist_ok=True, parents=True)

REAL_FRAMES_EVALUATION_FOLDER = Path('data/real_frames/evaluation')
REAL_FRAMES_EVALUATION_FOLDER.mkdir(exist_ok=True, parents=True)

videos = list(sorted(Path('data/videos').glob('*.mp4')))
logger.info(f"Found {len(videos)} videos")

np.random.seed(SEED)
logger.info(f"Using seed {SEED}")

def extract_frame_randomly(videos, output_folder):
    video = np.random.choice(videos)
    cap = cv2.VideoCapture(str(video))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_index = np.random.randint(0, total_frames)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)

    ret, frame = cap.read()
    if not ret:
        logger.error(f"Could not read frame {frame} from {video}")
        return None
    
    frame = np.flip(frame, axis=2)
    image = Image.fromarray(frame)
    output_path = output_folder / f"{video.stem}_{frame_index:05}.png"
    image.save(output_path)

logger.info(f"Extracting {TRAINING_FRAMES} training frames")
for _ in tqdm(range(TRAINING_FRAMES)):
    extract_frame_randomly(videos, REAL_FRAMES_TRAINING_FOLDER)

logger.info(f"Extracting {EVALUATION_FRAMES} evaluation frames")
for _ in tqdm(range(EVALUATION_FRAMES)):
    extract_frame_randomly(videos, REAL_FRAMES_EVALUATION_FOLDER)

assert len(list(REAL_FRAMES_TRAINING_FOLDER.glob('*.png'))) == TRAINING_FRAMES
assert len(list(REAL_FRAMES_EVALUATION_FOLDER.glob('*.png'))) == EVALUATION_FRAMES