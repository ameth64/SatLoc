# SatLoc Dataset

This repository contains datasets created from the work of the following papers.: 

[Towards UAV Localization in GNSS-Denied Environments: The SatLoc Dataset and a Hierarchical Adaptive Fusion Framework](https://www.mdpi.com/2072-4292/17/17/3048)


## Dataset

### Download

The dataset can be downloaded from: 
 [Quark](https://pan.quark.cn/s/1cdf996537cc) with access code `yYuP`, including the UAV captured frames and satellite images for training and evaluation.

### Description

We have prepared UAV aerial images with different trajectories, as well as satellite imagery covering the flight paths (stored in .tif format). The directory structure is as follows:

```
+--- SatLoc
|	+--- Satellite Data
|		---- CS_Area1.tif
|		---- ref_sample.csv
|		+--- sat_image_ref
|	+--- UAV Data
|		+--- traj01
|		+--- ...
|		+--- ...
|   ---- eval_samplel.py

```

For files in the `Satellite Data` directory:

- Satellite imagery contains a complete DOM (DOM) of the data acquisition area (.tif), with embedded geographic coordinate data;
- The `sat_image_ref` directory stores satellite tile images used for DOM composition, numbered sequentially with 5 digits;
- `ref_sample.csv` stores the correspondence between the sequence number of a satellite tile image and its local pixel coordinates in the DOM image.

To obtain the latitude and longitude range corresponding to the "top left - bottom right" corner of a satellite tile image with a given sequence number, please refer to the example code in `eval_samplel.py`.

The `UAV Data` directory stores the image sequences captured by the UAV's onboard imaging equipment, organized by flight sortie number. Each image is named according to the following rule:

```
Sequence_Number@Frame_Number@Longitude@Latitude
```
Due to the large volume of flight sortie data, we will upload it in batches as soon as possible.


## Citation

If you find this dataset useful for your research, please consider citing our paper: 

```
@Article{rs17173048,
AUTHOR = {Zhou, Xiang and Zhang, Xiangkai and Yang, Xu and Zhao, Jiannan and Liu, Zhiyong and Shuang, Feng},
TITLE = {Towards UAV Localization in GNSS-Denied Environments: The SatLoc Dataset and a Hierarchical Adaptive Fusion Framework},
JOURNAL = {Remote Sensing},
VOLUME = {17},
YEAR = {2025},
NUMBER = {17},
ARTICLE-NUMBER = {3048},
URL = {https://www.mdpi.com/2072-4292/17/17/3048},
ISSN = {2072-4292},
DOI = {10.3390/rs17173048}
}
```
