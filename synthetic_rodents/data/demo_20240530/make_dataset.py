import bpy 
import pickle 
import numpy as np
import bmesh 
import bpy_extras

from pathlib import Path 
from bpy.app.handlers import persistent

# import world coords to camera
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector, Matrix

# SETUP 
#----------------------------------------------------------
output_path = Path("data/tests/demo_20240530")
output_path.mkdir(exist_ok=True, parents=True)

MAX_RENDER_TIME = 30

# DEFAULT RENDER SETTINGS
#----------------------------------------------------------
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.device = 'GPU'
scene.cycles.feature_set = 'SUPPORTED'
scene.cycles.samples = 1000
scene.cycles.max_bounces = 12
scene.cycles.transparent_max_bounces = 12
scene.cycles.transparent_min_bounces = 8
scene.cycles.use_square_samples = True
scene.cycles.preview_samples = 100
scene.cycles.aa_samples = 12
scene.cycles.diffuse_samples = 12
scene.cycles.glossy_samples = 12
scene.cycles.transmission_samples = 12
scene.cycles.volume_samples = 12
scene.cycles.use_progressive_refine = True
scene.cycles.use_square_samples = True
scene.cycles.preview_aa_samples = 12
scene.cycles.preview_diffuse_samples = 12
scene.cycles.preview_glossy_samples = 12
scene.cycles.preview_transmission_samples = 12
scene.cycles.preview_volume_samples = 12

scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100

scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGB'
scene.render.image_settings.color_depth = '16'
scene.render.image_settings.compression = 100
scene.render.image_settings.use_zbuffer = False
scene.render.image_settings.use_preview = False

# ANIMATION 
#----------------------------------------------------------
scene = bpy.context.scene
context = bpy.context
scene.frame_start = 0
scene.frame_end = 200
scene.render.fps = 200


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

for i in range(0, 30):
# for i in [0, 5, 10]:
    print(f"Rendering frame {i}")

    output_image_file = output_path / f"render_{i:04}.png"
    output_pose_file = output_path / f"render_{i:04}.pkl"

    scene.frame_set(i)
    context.view_layer.update()

    # Save the rendered image only if the file doesnt exist already
    if output_image_file.exists():
        print(f"Skipping frame {i}")
        continue

    scene.render.filepath = str(output_image_file)
    bpy.ops.render.render(write_still=True)

    # Save the pose only if the file doesnt exist already
    if output_pose_file.exists():
        print(f"Skipping pose {i}")
        continue

    results = {}
    for bodypart in bodyparts:
        obj = scene.objects[bodypart]
        camera = scene.objects['Camera']

        # position of object in camera view
        position_2d = bpy_extras.object_utils.world_to_camera_view(scene, camera, obj.matrix_world.translation)
        print("Position 2D", position_2d)

        # adjust for image size
        width = scene.render.resolution_x
        height = scene.render.resolution_y
        print("Resolution", width, height)
        
        x = position_2d.x * width
        y = (1 - position_2d.y) * height
        print("Position", x, y)

        results[bodypart] = np.array([x, y])

    with open(output_pose_file, "wb") as f:
        pickle.dump(results, f)