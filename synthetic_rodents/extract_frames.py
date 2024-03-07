"""Extract frames from the real videos"""

import cv2
import numpy as np
import logging 
import yaml
import pandas as pd
import random 

from synthetic_rodents import constants
from pathlib import Path
from tqdm import tqdm
from PIL import Image

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

videos = list(sorted(Path('data/videos').glob('*.mp4')))
logger.info(f"Found {len(videos)} videos")

np.random.seed(constants.SEED)
random.seed(constants.SEED)
logger.info(f"Using seed {constants.SEED}")

logger.info(f"Creating config file for videos and frames")
with open(constants.REAL_DATA_FOLDER / "config.yaml", "w") as f:
    yaml.dump({
        'bodyparts': constants.BODYPARTS,
    }, f)

data = []
for video in videos:
    cap = cv2.VideoCapture(str(video))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    logger.info(f"Video {video.name} has {total_frames} frames")

    for _ in range(constants.FRAMES_PER_VIDEO):
        # Select a frame
        while True:
            frame_index = np.random.randint(0, total_frames)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
            ret, frame = cap.read()
            if not ret:
                logger.error(f"Could not read frame {frame_index} from {video}")
                continue

            break

        frame = np.flip(frame, axis=2)
        image = Image.fromarray(frame)
        filename = f"image{random.randint(0, 1e10):010}.png"
        output_path = constants.REAL_IMAGES_FOLDER / filename
        logger.info(f"Saved frame {frame_index} from {video.name} to {output_path}")
        image.save(output_path)
        data.append({
            'video': video.name,
            'frame_index': frame_index,
            'filename': filename,
        })

    cap.release()
    
pd.DataFrame(data).to_csv(constants.REAL_DATA_FOLDER / "frames.csv", index=False)