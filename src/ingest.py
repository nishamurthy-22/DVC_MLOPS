from zipfile import ZipFile
import sys
import os
import yaml

datapath= sys.argv[1]
os.makedirs(datapath, exist_ok=True)

params = yaml.safe_load(open('params.yaml'))

with ZipFile(f"datasets/{params['yolov5']['dpath']}", 'r') as f:
    f.extractall(datapath)