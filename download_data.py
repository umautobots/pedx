import os
import sys
import subprocess

def wget(basedir, url):
    if 'linux' in sys.platform:
        cmd = 'wget -P {} {}'.format(basedir, url)
    elif 'darwin' in sys.platform:
        cmd = 'cd {} && {{ curl -O {} ; cd -; }}'.format(basedir, url)
    else:
        print('wget not implemented for the platform {}'.format(sys.platform))
        exit()
    print(cmd)
    if subprocess.call(cmd, shell=True) != 0: print('Error: {}'.format(cmd))

def extract(fn, dst):
    cmd = 'tar -xzvf {} -C {}'.format(fn, dst)
    print(cmd)
    if subprocess.call(cmd, shell=True) != 0: print('Error: {}'.format(cmd))

def remove(fn):
    cmd = 'rm {}'.format(fn)
    print(cmd)
    if subprocess.call(cmd, shell=True) != 0: print('Error: {}'.format(cmd))

def mkdir(dn):
    if not os.path.exists(dn):
        cmd = 'mkdir -p {}'.format(dn)
        print(cmd)
        if subprocess.call(cmd, shell=True) != 0: print('Error: {}'.format(cmd))

def download_data(basedir, capture_date):
    url = 'http://pedx.io/data/images-rectified_{}'.format(capture_date)
    dst = os.path.join(basedir, 'images')
    fn = os.path.join(basedir, url.split('/')[-1])
    mkdir(dst)
    wget(basedir, url)
    extract(fn, dst)

    url = 'http://pedx.io/data/pointclouds_{}'.format(capture_date)
    dst = os.path.join(basedir, 'pointclouds')
    fn = os.path.join(basedir, url.split('/')[-1])
    mkdir(dst)
    wget(basedir, url)
    extract(fn, dst)

    url = 'http://pedx.io/data/labels-2d_{}.tar.gz'.format(capture_date)
    dst = os.path.join(basedir, 'labels/2d')
    fn = os.path.join(basedir, url.split('/')[-1])
    mkdir(dst)
    wget(basedir, url)
    extract(fn, dst)

    url = 'http://pedx.io/data/labels-3d-segment_{}.tar.gz'.format(capture_date)
    dst = os.path.join(basedir, 'labels/3d/segment')
    fn = os.path.join(basedir, url.split('/')[-1])
    mkdir(dst)
    wget(basedir, url)
    extract(fn, dst)

    url = 'http://pedx.io/data/timestamps_{}.tar.gz'.format(capture_date)
    dst = os.path.join(basedir, 'timestamps')
    fn = os.path.join(basedir, url.split('/')[-1])
    mkdir(dst)
    wget(basedir, url)
    extract(fn, dst)

    url = 'http://pedx.io/data/preview_{}.mp4'.format(capture_date)
    dst = os.path.join(basedir, 'preview')
    mkdir(dst)
    wget(dst, url)

    # (Optional)
    # url = 'http://pedx.io/data/images-original_{}'.format(capture_date)
    # dst = os.path.join(basedir, 'images-original')
    # fn = os.path.join(basedir, url.split('/')[-1])
    # mkdir(dst)
    # wget(basedir, url)
    # extract(fn, dst)

def download_calib(basedir):
    url = 'http://pedx.io/data/calib.tar.gz'
    dst = os.path.join(basedir, 'calib')
    fn = os.path.join(basedir, url.split('/')[-1])
    mkdir(dst)
    wget(basedir, url)
    extract(fn, dst)


if __name__ == '__main__':

    # data will be downloaded into ./data directory
    basedir = 'data'
    mkdir(basedir)

    capture_dates = ['20171130T2000', '20171207T2024', '20171212T2030']
    for capture_date in capture_dates:
        download_data(basedir, capture_date)
    download_calib(basedir)
