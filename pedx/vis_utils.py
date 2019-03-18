import os
import random
import cv2
import numpy as np
import pedx.data_loader as dl

def generate_a_random_color(dtype):
    if dtype == np.uint8:
        return (random.randint(10,255), random.randint(10,255), random.randint(10,255))
    else:
        print('Not implemented yet')
        return None

def draw_a_skeleton(image, points, color=None):
    if color is None: color = generate_a_random_color(np.uint8)
    print('draw_a_skeleton not implemented yet')
    return image

def draw_a_polygon(image, polygon, color=None):
    if color is None: color = generate_a_random_color(np.uint8)
    cv2.polylines(image, [polygon], True, color=color, thickness=3)
    return image

def draw_a_text_box(image, text_str, text_loc, color=None, fontscale=2.5, thickness=5, noise=True):
    if color is None: color = generate_a_random_color(np.uint8)
    text_size, text_baseline = cv2.getTextSize(text_str, cv2.FONT_HERSHEY_SIMPLEX, fontscale, thickness)
    if noise:
        tx = np.maximum(np.minimum(int(text_loc[0]-text_size[0]/2-100+random.randint(0,100)), image.shape[1]-text_size[0]-1),0)
        ty = int(text_loc[1]-random.randint(30,250))
    else:
        tx, ty = tuple(text_loc)
    text_w, text_h = text_size
    colors_rect = np.array([[250,250,250],[200,200,200],[150,150,150],[100,100,100],[50,50,50],[0,0,0]]).reshape(-1,3).astype('float')
    clr = (np.array(list(color))).astype('int')
    color_rect = colors_rect[np.argmax(np.linalg.norm(colors_rect - clr.reshape(1,3), axis=1))]
    cv2.rectangle(image, (tx-2,int(ty-text_h-text_baseline/2)),(tx+text_w+2,int(ty+text_baseline/2+12)), color_rect, thickness=-1)
    cv2.putText(image, text_str, (tx,ty), cv2.FONT_HERSHEY_SIMPLEX, fontscale, color, thickness, lineType=cv2.LINE_AA)
    return image

def draw_2d_labels_at_an_image(
        basedir, capture_date, camera_name, frame_id, track_ids=None, labels=None, 
        track_id_to_color_map=None, window_name=None, savedir=None):

    if labels is None:
        labels = dl.load_label_2d_at_an_image(basedir, capture_date, camera_name, frame_id, track_ids)
    
    image = dl.load_an_image(basedir, capture_date, camera_name, frame_id)
    
    if track_id_to_color_map is None: track_id_to_color_map = {}

    for k, d in labels.items():
        tid = d['tracking_id']
        assert k == tid, '>> Draw_2d_labels_at_an_image :: Invalid label: {}_{}_{:07d}'.format(capture_date, camera_name, frame_id)
        
        # assign a color to the instance
        if tid not in track_id_to_color_map.keys():
            track_id_to_color_map[tid] = generate_a_random_color(np.uint8)
        color = track_id_to_color_map[tid]
        
        # draw labels
        text_loc = None
        if 'polygon' in d.keys():
            if d['polygon'] is not None:
                polygon = np.array(d['polygon'])
                image = draw_a_polygon(image, polygon, color)
                text_loc = tuple(np.min(polygon, axis=0))
        if d['category'] == 'pedestrian':
            text_str = tid[-4:]
            if d['keypoint'] is not None:
                # image = draw_a_skeleton(image, keypoints)
                if text_loc is None:
                    pts = [[v['x'],v['y']] for v in d['keypoint'].values()]
                    text_loc = tuple(np.min(kpts, axis=0))
        elif d['category'] == 'vehicle':
            subtype = d['subtype'] if 'subtype' in d.keys() else None
            text_str = '{}|{}'.format(tid[-4:], subtype)
            print('drawing vehicle not implemented yet')
        image = draw_a_text_box(image, text_str, text_loc, color)

    if window_name is not None:
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, 800, 800)
        cv2.moveWindow(window_name, 0, 0)
        cv2.imshow(window_name, image)
        cv2.waitKey(0)

    if savedir is not None:
        frame_key = '{}_{}_{:07d}'.format(capture_date, camera_name, frame_id)
        fn_save = os.path.join(savedir, capture_date, camera_name, '{}.png'.format(frame_key))
        if not os.path.exists(os.path.dirname(fn_save)):
            os.makedirs(os.path.dirname(fn_save), exist_ok=True)
        cv2.imwrite(fn_save, image)
        print('{} saved.'.format(fn_save))

    return image, track_id_to_color_map

def draw_2d_labels_at_a_frame(
        basedir, capture_date, frame_id, track_ids=None, labels=None,
        track_id_to_color_map=None, window_name=None, savedir=None):

    if labels is None:
        labels = dl.load_label_2d_at_a_frame(basedir, capture_date, frame_id, track_ids)
    
    images = {}
    for camera_name in labels.keys():
        images[camera_name], track_id_to_color_map = draw_2d_labels_at_an_image(
                basedir, capture_date, camera_name, frame_id, 
                track_id_to_color_map=track_id_to_color_map, labels=labels[camera_name])
        images[camera_name] = cv2.resize(images[camera_name], dsize=None, fx=0.25, fy=0.25)
        images[camera_name] = draw_a_text_box(images[camera_name], camera_name, (375,625), (250,50.,300), 1.5, 2, noise=False)
    
    # concatenate images
    images_yr = np.concatenate([images['ylw79D0'], images['red707B']], axis=1)
    images_bg = np.concatenate([images['blu79CF'], images['grn43E3']], axis=1)
    images_yr = cv2.resize(images_yr, dsize=(images_bg.shape[1], images_bg.shape[0]))
    image_concat = np.concatenate([images_yr, images_bg], axis=0)

    if window_name is not None:
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, 800, 800)
        cv2.moveWindow(window_name, 0, 0)
        cv2.imshow(window_name, image_concat)
        cv2.waitKey(0)
    
    if savedir is not None:
        frame_key = '{}_{:07d}'.format(capture_date, frame_id)
        fn_save = os.path.join(savedir, capture_date, '{}.png'.format(frame_key))
        if not os.path.exists(os.path.dirname(fn_save)):
            os.makedirs(os.path.dirname(fn_save), exist_ok=True)
        cv2.imwrite(fn_save, image_concat)
        print('{} saved.'.format(fn_save))

    return image_concat, track_id_to_color_map

def draw_projected_pointclouds_at_a_frame(basedir, capture_date, frame_id, track_ids=None,
        track_id_to_color_map=None, window_name=None, savedir=None):
    
    # load a point cloud of the entire scene at this frame
    pcd = dl.load_a_pointcloud(basedir, capture_date, frame_id)
    
    # project the points
    w,h = 1000,750
    image = np.zeros((h,w,3), dtype=np.uint8)
    def _project_points(v):
        nv = v.shape[0]
        R = np.array([[0.13637362, -0.98993436, -0.03784438],
                [-0.91489993, -0.1405043, 0.37843977],
                [-0.37994783, -0.01698538, -0.92485196]])
        T = np.array([0.0, -27, -80])
        D = np.array([0,0,0,0,0.])
        _w,_h = w/2,h/2
        K = np.array([[-2*_w, 0.0, _w], [0., 2*_h, _h], [0, 0, 1.]])
        return cv2.projectPoints(v, R, T, K, D)[0].reshape(nv,2).astype('int')

    mask = (pcd[:,0] != np.inf) & (pcd[:,2]>-5.)
    v_I = _project_points(pcd[mask,:])
    u, v = v_I[:,0], v_I[:,1]
    mask = (u>=0) & (v>=0) & (u<w) & (v<h)
    ids = (np.concatenate([v[mask],v[mask],v[mask]]),
            np.concatenate([u[mask],u[mask],u[mask]]),
            np.repeat([0,1,2], np.sum(mask)))
    image[ids] = 255
    
    # load instance-wise segmented point clouds 
    if track_id_to_color_map is None: track_id_to_color_map = {}
    pcds = dl.load_pointclouds_at_a_frame(basedir, capture_date, frame_id, track_ids)
    
    for tid, pcd in pcds.items():
        if tid not in track_id_to_color_map.keys():
            track_id_to_color_map[tid] = generate_a_random_color(np.uint8)
        color = track_id_to_color_map[tid]

        v_I = _project_points(pcd)
        u, v = v_I[:,0], v_I[:,1]
        mask = (u>=0) & (v>=0) & (u<w) & (v<h)
        ones = np.ones(np.sum(mask), dtype=int)
        image[(v[mask], u[mask], ones*0)] = color[0]
        image[(v[mask], u[mask], ones*1)] = color[1]
        image[(v[mask], u[mask], ones*2)] = color[2]
    
    text_str = '{:07d}'.format(frame_id)
    image = draw_a_text_box(image, text_str, (50,50), (200,120,150.), 1, 2, noise=False)

    if window_name is not None:
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, 800, 800)
        cv2.moveWindow(window_name, 0, 0)
        cv2.imshow(window_name, image)
        cv2.waitKey(0)
    
    if savedir is not None:
        frame_key = '{}_{:07d}'.format(capture_date, frame_id)
        fn_save = os.path.join(savedir, capture_date, '{}.png'.format(frame_key))
        if not os.path.exists(os.path.dirname(fn_save)):
            os.makedirs(os.path.dirname(fn_save), exist_ok=True)
        cv2.imwrite(fn_save, image)
        print('{} saved.'.format(fn_save))

    return image, track_id_to_color_map 
