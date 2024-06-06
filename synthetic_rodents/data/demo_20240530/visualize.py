from pathlib import Path
from skimage.draw import line, ellipse
from PIL import Image

import numpy as np
import pickle 
import matplotlib.pyplot as plt

bodyparts = [
    'left_eye',
    'right_eye',
    'nose',
    'neck',
    'midback',
    'hip',
    'tailbase',
    'left_front_paw',
    'left_front_knee',
    'left_front_shoulder',
    'right_front_paw',
    'right_front_knee',
    'right_front_shoulder',
    'left_rear_paw',
    'left_rear_knee',
    'left_rear_hip',
    'right_rear_paw',
    'right_rear_knee',
    'right_rear_hip',
]

skeleton = [
    ['nose', 'left_eye'],
    ['nose', 'right_eye'],
    ['nose', 'neck'],
    ['left_eye', 'neck'],
    ['right_eye', 'neck'],
    ['neck', 'midback'],
    ['midback', 'hip'],
    ['hip', 'tailbase'],
    ['neck', 'left_front_shoulder'],
    ['left_front_shoulder', 'left_front_knee'],
    ['left_front_knee', 'left_front_paw'],
    ['neck', 'right_front_shoulder'],
    ['right_front_shoulder', 'right_front_knee'],
    ['right_front_knee', 'right_front_paw'],
    ['midback', 'left_rear_hip'],
    ['left_rear_hip', 'left_rear_knee'],
    ['left_rear_knee', 'left_rear_paw'],
    ['midback', 'right_rear_hip'],
    ['right_rear_hip', 'right_rear_knee'],
    ['right_rear_knee', 'right_rear_paw'],
]


data_folder = Path("data/tests/demo_20240530").absolute()
print("rendering to", data_folder)

for i, frame in enumerate(sorted(data_folder.glob("*.png"))):
    if 'labeled' in frame.stem:
        continue

    with open(data_folder / f"{frame.stem}.pkl", "rb") as f:
        data = pickle.load(f)

    image = Image.open(frame)
    image = np.array(image)
    radius = 10
    for label, loc in data.items():
        rr, cc = ellipse(loc[1], loc[0], radius, radius, image.shape)
        image[rr, cc] = 255

    height, width = image.shape[:2]
    for a, b in skeleton:
        loc_a = data[a]
        loc_b = data[b]
        c0, r0 = map(int, loc_a)
        c1, r1 = map(int, loc_b)
        
        rr, cc = line(r0, c0, r1, c1)
        mask = (rr >= 0) & (rr < height) & (cc >= 0) & (cc < width)
        rr = rr[mask]
        cc = cc[mask]
        image[rr, cc] = 255
        
    image = Image.fromarray(image)
    image.save(data_folder / f"{frame.stem}_labeled.png")
    print("saved", data_folder / f"{frame.stem}_labeled.png")