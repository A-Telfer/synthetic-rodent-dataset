# synthetic_rodents

## Setup
First you have to export the path to your blender executable, for me that's `export BLENDER=/home/andretelfer/blender-3.4.1-linux-x64/blender`
```
conda create -n synth-rodent python=3.10
conda activate synth-rodent
make requirements 
make render-demo
```

### Extracting Evaluation Frames from Real Videos

Download and link to the video folder, or place them inside data/videos
```
ln -s /path/to/downloaded/videos data/videos
```
