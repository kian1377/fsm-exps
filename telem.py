import numpy as np
import astropy.units as u
from IPython.display import clear_output, display
import subprocess
import glob
from pathlib import Path
import os
import shutil

import magpyx
from magpyx.utils import ImageStream
import purepyindi
from purepyindi import INDIClient
import purepyindi2
from purepyindi2 import IndiClient

cam_path = Path('/opt/MagAOX/rawimages/campupil/')
fsm_path = Path('/opt/MagAOX/rawimages/fsm/')

def toggle(on, channel, client):
    client.wait_for_properties([f'telem_{channel}.writing'])
    if on:
        client[f'telem_{channel}.writing.toggle'] = purepyindi.SwitchState.ON
    else:
        client[f'telem_{channel}.writing.toggle'] = purepyindi.SwitchState.OFF

def toggle_telem_campupil(on, client):
    client.wait_for_properties(['telem_campupil.writing'])
    if on:
        client[f'telem_campupil.writing.toggle'] = purepyindi.SwitchState.ON
    else:
        client[f'telem_campupil.writing.toggle'] = purepyindi.SwitchState.OFF

def toggle_telem_fsm(on, client):
    client.wait_for_properties(['telem_fsm.writing'])
    if on:
        client[f'telem_fsm.writing.toggle'] = purepyindi.SwitchState.ON
    else:
        client[f'telem_fsm.writing.toggle'] = purepyindi.SwitchState.OFF

def toggle_telem_fsm_and_cam(on, client):
    client.wait_for_properties(['telem_campupil.writing, telem_fsm.writing'])
    if on:
        client[f'telem_fsm.writing.toggle'] = purepyindi.SwitchState.ON
        client[f'telem_campupil.writing.toggle'] = purepyindi.SwitchState.ON
    else:
        client[f'telem_fsm.writing.toggle'] = purepyindi.SwitchState.OFF
        client[f'telem_campupil.writing.toggle'] = purepyindi.SwitchState.OFF

def unpack_telem_data(telem_path, data_path):
    subprocess.run(['xrif2fits', '-d', str(telem_path), '-D', str(data_path)])
    clear_output()

def parse_telem_fnames(data_path):
    sorted(glob.glob(str(data_path)))

def make_dir(dir_path):
    subprocess.run(['mkdir',str(dir_path)])

def move_files(source_path, target_path):
    file_names = os.listdir(str(source_path))
    for fname in file_names:
        shutil.move(str(source_path/fname), str(target_path/fname))
        # src = str(source_path/fname)
        # dest = str(target_path)
        # subprocess.run(['mv', src, dest], check=True)

def delete_all_data(dir_path):
    directory = str(dir_path)
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

