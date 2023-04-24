from zipfile import ZipFile
import sys
import os

datapath= sys.argv[1]
os.makedirs(datapath, exist_ok=True)

with ZipFile('datasets/dataset2.zip', 'r') as f:
    f.extractall(datapath)