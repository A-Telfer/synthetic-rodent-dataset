from pathlib import Path

SEED = 42

REAL_TRAINING_FRAMES = 200
REAL_EVALUATION_FRAMES = 100

PROJECT_DIR = Path(__file__).parents[1].absolute()

REAL_VIDEOS_FOLDER = PROJECT_DIR / "data/videos"
assert REAL_VIDEOS_FOLDER.exists()

REAL_FRAMES_TRAINING_FOLDER = PROJECT_DIR / "data/real_frames/training"
REAL_FRAMES_TRAINING_FOLDER.mkdir(exist_ok=True, parents=True)

REAL_FRAMES_EVALUATION_FOLDER = PROJECT_DIR / "data/real_frames/evaluation"
REAL_FRAMES_EVALUATION_FOLDER.mkdir(exist_ok=True, parents=True)

DEEPLABCUT_MANUAL_LABELS_FOLDER = PROJECT_DIR / "data/deeplabcut/manual_labels"
DEEPLABCUT_MANUAL_LABELS_FOLDER.mkdir(exist_ok=True, parents=True)

SCORERS = [
    "user1",
    "user2",
    "user3"
]

BODYPARTS = [
    "nose",
    "shoulders",
    "tailbase",
    "left_front_foot",
    "right_front_foot",
    "left_back_foot",
    "right_back_foot"
]