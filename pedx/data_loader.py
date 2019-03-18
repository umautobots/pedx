import os
import glob
import numpy as np
import json
import cv2
from pedx.utils import read_calib_file, read_ply

def list_all_capture_dates():
    return ['20171130T2000', '20171207T2024', '20171212T2030']

def list_all_camera_names():
    return ['ylw79D0','red707B','blu79CF','grn43E3']

def list_all_camera_pairs():
    return ['ylw79D0-red707B', 'blu79CF-grn43E3']

def get_image_shape(camera_name):
    if camera_name == 'blu79CF' or camera_name == 'grn43E3':
        return (3645,2687)
    elif camera_name == 'ylw79D0' or camera_name == 'red707B':
        return (3678,2668)
    else:
        print('Invalid camera name: {}'.format(camera_name))
        return None

def load_calib(basedir, pairname):
    camera_name_ref = pairname.split('-')[0]
    fn_cam2range = os.path.join(basedir, 'calib/calib_cam_to_range_{}.txt'.format(camera_name_ref))
    fn_cam2cam = os.path.join(basedir, 'calib/calib_cam_to_cam_{}.txt'.format(pairname))
    calib_rigid = read_calib_file(fn_cam2range)
    calib = read_calib_file(fn_cam2cam)
    return calib_rigid, calib

def load_an_image(basedir, capture_date, camera_name, frame_id):
    frame_key = '{}_{}_{:07d}'.format(capture_date, camera_name, frame_id)
    ext = 'jpg'
    fn = os.path.join(basedir, 'images', capture_date, camera_name, '{}.{}'.format(frame_key, ext))
    if os.path.exists(fn):
        image = cv2.imread(fn, cv2.IMREAD_UNCHANGED)
    else:
        print('Failed to load an image: {}'.format(fn))
        image = None
    return image

def load_a_pointcloud(basedir, capture_date, frame_id):
    frame_key = '{}_{:07d}'.format(capture_date, frame_id)
    ext = 'ply'
    fn = os.path.join(basedir, 'pointclouds', capture_date, '{}.{}'.format(frame_key, ext))
    if os.path.exists(fn):
        pcd = read_ply(fn)
    else:
        print('Failed to load a pointcloud: {}'.format(fn))
        pcd = None
    return pcd

def load_label_2d_at_an_image(basedir, capture_date, camera_name, frame_id, track_ids=None):
    if track_ids is None:
        fns = glob.glob(os.path.join(basedir, 'labels/2d', capture_date, camera_name, 
            '{}_{}_{:07d}_*.json'.format(capture_date, camera_name, frame_id)))
        track_ids = [fn.split('_')[-1].split('.')[0] for fn in fns]
    elif type(track_ids) is not list:
        track_ids = list(track_ids)
    labels = {}
    for tid in track_ids:
        ext = 'json'
        frame_key = '{}_{}_{:07d}_{}'.format(capture_date, camera_name, frame_id, tid)
        fn = os.path.join(basedir, 'labels/2d', capture_date, camera_name, '{}.{}'.format(frame_key, ext))
        if os.path.exists(fn):
            labels[tid] = json.load(open(fn,'r'))
    return labels

def load_label_2d_at_a_frame(basedir, capture_date, frame_id, track_ids=None):
    labels = {}
    camera_names = list_all_camera_names()
    for camera_name in camera_names:
        labels[camera_name] = load_label_2d_at_an_image(basedir, capture_date, camera_name, frame_id, track_ids)
    return labels

def load_pointclouds_at_a_frame(basedir, capture_date, frame_id, track_ids=None):
    if track_ids is None:
        fns = glob.glob(os.path.join(basedir, 'labels/3d/segment', capture_date, 
            '{}_{:07d}_*.ply'.format(capture_date, frame_id)))
        track_ids = [fn.split('_')[-1].split('.')[0] for fn in fns]
    elif type(track_ids) is not list:
        track_ids = list(track_ids)
    pcds = {}
    for tid in track_ids:
        ext = 'ply'
        frame_key = '{}_{:07d}_{}'.format(capture_date, frame_id, tid)
        fn = os.path.join(basedir, 'labels/3d/segment', capture_date, '{}.{}'.format(frame_key, ext))
        if os.path.exists(fn):
            pcds[tid] = read_ply(fn)
    return pcds
