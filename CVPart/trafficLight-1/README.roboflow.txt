
trafficLight - v1 ver0.1
==============================

This dataset was exported via roboflow.com on June 2, 2026 at 3:26 PM GMT

Roboflow is an end-to-end computer vision platform that helps you
* collaborate with your team on computer vision projects
* collect & organize images
* understand and search unstructured image data
* annotate, and create datasets
* export, train, and deploy computer vision models
* use active learning to improve your dataset over time

For state of the art Computer Vision training notebooks you can use with this dataset,
visit https://github.com/roboflow/notebooks

To find over 100k other datasets and pre-trained models, visit https://universe.roboflow.com

The dataset includes 56 images.
TrafficLight are annotated in YOLOv8 format.

The following pre-processing was applied to each image:
* Auto-orientation of pixel data (with EXIF-orientation stripping)
* Resize to 432x432 (Stretch)

The following augmentation was applied to create 3 versions of each source image:
* Random rotation of between -13 and +13 degrees
* Random shear of between -10° to +10° horizontally and -14° to +14° vertically
* Random brigthness adjustment of between -35 and +35 percent
* Salt and pepper noise was applied to 1.09 percent of pixels


