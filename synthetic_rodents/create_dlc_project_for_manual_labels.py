import deeplabcut 
import logging 
import shutil 

from PIL import Image
from pathlib import Path
from synthetic_rodents import constants

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

DEEPLABCUT_MANUAL_LABELS_FOLDER = Path('data/deeplabcut/manual_labels')
DEEPLABCUT_MANUAL_LABELS_FOLDER.mkdir(exist_ok=True, parents=True)
if DEEPLABCUT_MANUAL_LABELS_FOLDER.exists():
    logger.info(f"Folder {DEEPLABCUT_MANUAL_LABELS_FOLDER} already exists")

for scorer in constants.SCORERS:
    logger.info(f"Creating a new project for {scorer}")
    config_path = deeplabcut.create_new_project(
        project='labels', 
        experimenter=scorer,
        working_directory=DEEPLABCUT_MANUAL_LABELS_FOLDER,
        copy_videos=False,
        multianimal=False,
        videos=list(sorted(constants.REAL_VIDEOS_FOLDER.glob('*.mp4'))),
    )

    # Copy the labeled data to the deeplabcut projects
    logger.info(f"Copying the labeled data to the project {config_path}")
    labeled_data_folder = Path(config_path).parent / "labeled-data"

    logger.info("Copying the labeled data to %s", labeled_data_folder / 'training_frames')
    shutil.copytree(constants.REAL_FRAMES_TRAINING_FOLDER, labeled_data_folder / 'training_frames')

    logger.info("Copying the labeled data to %s", labeled_data_folder / 'evaluation_frames')
    shutil.copytree(constants.REAL_FRAMES_EVALUATION_FOLDER, labeled_data_folder / 'evaluation_frames')
    
    # Get the size of each frame 
    logger.info("Getting the size of each frame")
    image = Image.open(next(constants.REAL_FRAMES_TRAINING_FOLDER.glob('*.png')))
    img_size = image.size
    deeplabcut.auxiliaryfunctions.edit_config(config_path, {'imgsize': img_size})

    deeplabcut.auxiliaryfunctions.edit_config(config_path, {'bodyparts': constants.BODYPARTS})

