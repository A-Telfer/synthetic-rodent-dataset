from pathlib import Path

SEED = 42

FRAMES_PER_VIDEO = 5
TRAIN_TEST_SPLIT = 0.8

PROJECT_DIR = Path(__file__).parents[1].absolute()

REAL_VIDEOS_FOLDER = PROJECT_DIR / "data/videos"
assert REAL_VIDEOS_FOLDER.exists()

REAL_DATA_FOLDER = PROJECT_DIR / "data/real_data"
REAL_DATA_FOLDER.mkdir(exist_ok=True, parents=True)

REAL_IMAGES_FOLDER = REAL_DATA_FOLDER / "images"
REAL_IMAGES_FOLDER.mkdir(exist_ok=True, parents=True)

BODYPARTS = [
    "nose",
    "shoulders",
    "tailbase",
    "left_front_foot",
    "right_front_foot",
    "left_back_foot",
    "right_back_foot"
]