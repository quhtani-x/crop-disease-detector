# Crop Disease Detector

A farmer photographs a leaf and this estimates how diseased it is. It finds the
leaf, separates healthy green from brown/yellow diseased spots, reports the
percentage of the leaf that looks unhealthy, and outlines the bad patches in
red. A "scout your field with your phone" tool.

If you don't pass an image it generates a fake spotted leaf so it runs right
away.

## how it works

- convert to HSV color space
- mask healthy green vs diseased brown/yellow ranges
- diseased % = diseased pixels / total leaf pixels
- outline the diseased patches and give a verdict

## run

```bash
pip install opencv-python numpy

python detect.py            # runs on a generated leaf
python detect.py leaf.jpg   # runs on your own photo
```

tags: ai, computer-vision, opencv, agriculture, farming

color segmentation in HSV is perfect for "how much of this is green vs not".
