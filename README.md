

# PedX

This package provides basic tools for working with the PedX dataset [[1]](#references) in Python.

## Data
The dataset is available from the webpage (http://pedx.io/downloads/). You can download the entire dataset by running the script `download_data.py`.  The data will be organized as in the following directory tree.

### Directory Tree
```
pedx/
├── pedx/
├── data/
│   ├── images/
│   │   ├── 20171130T2000/
│   │   ├── 20171207T2024/
│   │   └── 20171212T2030/
│   │       ├── ylw79D0/
│   │       ├── red707B/
│   │       ├── blu79CF/
│   │       └── grn43E3/
│   │           └── 20171212T2030_grn43E3_0001234.jpg
│   ├── pointclouds/
│   │   ├── 20171130T2000/
│   │   ├── 20171207T2024/
│   │   └── 20171212T2030/
│   │       └── 20171212T2030_0001234.ply
│   ├── labels/
│   |   ├── 2d/
│   |   │   ├── 20171130T2000/
│   |   │   ├── 20171207T2024/
│   |   │   └── 20171212T2030/
│   |   └── 3d/
│   |       ├── smpl/
│   |       │   ├── 20171130T2000/
│   |       │   ├── 20171207T2024/
│   |       |   └── 20171212T2030/
│   |       └── segment/
│   |           ├── 20171130T2000/
│   |           ├── 20171207T2024/
│   |           └── 20171212T2030/
│   ├── calib/
│   │   ├── calib_cam_to_cam_blu79CF-grn43E3.txt
│   │   ├── calib_cam_to_cam_blu79CF-red707B.txt
│   │   ├── calib_cam_to_range_blu79CF.txt
│   │   └── calib_cam_to_range_ylw79D0.txt
│   └── timestamps/
│       ├── timestamps-images-20171130T2000.txt
│       ├── timestamps-images-20171207T2024.txt
│       ├── timestamps-images-20171212T2030.txt
│       ├── timestamps-pointclouds-20171130T2000.txt
│       ├── timestamps-pointclouds-20171207T2024.txt
│       └── timestamps-pointclouds-20171212T2030.txt
├── demo.py
└── README.md
```

* `data` contains the rectified images, point clouds, calibrated parameters and frame metadata.
* All the manual/automatic annotations are in `data/labels`. 2D/3D annotations are provided in an instance-level.
* We provide 3 video sequences captured at different 4-way stop intersections on different dates.
	* Capture dates: `20171130T2000`, `20171207T2024`, `20171212T2030`
* The cameras are color-coded for our convenience.
	* Cameras: `ylw79D0`, `red707B`, `blu79CF`, `grn43E3`
	* Stereo pairs: `ylw79D0-red707B`, `blu79CF-grn43E3` (left-right camera)
* We provide a simple Python demo script: `demo.py`. `pedx` provides Python helper functions to load and visualize the data. We have tested the script with the Python packages listed in `requirements.txt`.


## Contact
Email: pedx-dataset@umich.edu

## References
[1] Kim, Wonhui, et al. "Pedx: Benchmark dataset for metric 3d pose estimation of pedestrians in complex urban intersections."  _IEEE Robotics and Automation Letters_  (2019). [http://pedx.io/](http://pedx.io/)