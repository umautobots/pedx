# PedX

This package provides basic tools for working with the PedX dataset [[1]](#references) in Python.


## Directory Tree
```
pedx/
├── pedx/
├── data/
│   ├── calib/
│   │   ├── calib_cam_to_cam_blu79CF-grn43E3.txt
│   │   ├── calib_cam_to_cam_blu79CF-red707B.txt
│   │   ├── calib_cam_to_range_blu79CF.txt
│   │   ├── calib_cam_to_range_ylw79D0.txt
│   ├── images/
│   │   ├── 20171130T2000/
│   │   ├── 20171207T2024/
│   │   ├── 20171212T2030/
│   │   │   ├── ylw79D0/
│   │   │   ├── red707B/
│   │   │   ├── blu79CF/
│   │   │   ├── grn43E3/
│   │   │   │   ├── 20171212T2030_grn43E3_0001234.jpg
│   └── pointclouds/
│   │   ├── 20171130T2000/
│   │   ├── 20171207T2024/
│   │   ├── 20171212T2030/
│   │   │   ├── 20171212T2030_0001234.ply
│   └── labels/
│   │   ├── 2d/
│   │   │   ├── 20171130T2000/
│   │   │   ├── 20171207T2024/
│   │   │   ├── 20171212T2030/
│   │   ├── 3d/
│   │   │   │   ├── smpl/
│   │   │   │   │   ├── 20171130T2000/
│   │   │   │   │   ├── 20171207T2024/
│   │   │   │   │   ├── 20171212T2030/
│   │   │   │   ├── segment/
│   │   │   │   │   ├── 20171130T2000/
│   │   │   │   │   ├── 20171207T2024/
│   │   │   │   │   ├── 20171212T2030/
├── demo.py
└── README.md
```

## References
[1] Kim, Wonhui, et al. "Pedx: Benchmark dataset for metric 3d pose estimation of pedestrians in complex urban intersections."  _IEEE Robotics and Automation Letters_  (2019). [http://pedx.io/](http://pedx.io/)