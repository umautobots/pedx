import cv2
import numpy as np
import pedx.data_loader as dl
import pedx.vis_utils as vis

__author__ = "Wonhui Kim"
__email__ = "pedx-dataset@umich.edu"

# change this to the directory where you stored PedX data
basedir = './data'

# specify the data to load
capture_date = '20171207T2024'
frame_id = 200

# visualize
wn = 'demo'
savedir = 'demo'
vis.draw_2d_labels_at_an_image(basedir, capture_date, 'blu79CF', frame_id, track_ids=None, labels=None, window_name=wn, savedir=savedir)
vis.draw_2d_labels_at_a_frame(basedir, capture_date, frame_id, track_ids=None, labels=None, window_name=wn, savedir=savedir)
vis.draw_projected_pointclouds_at_a_frame(basedir, capture_date, frame_id, track_ids=None, window_name=wn, savedir=savedir)
