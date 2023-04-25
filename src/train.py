import sys 
import yaml
import os

sys.path.insert(0, 'model/yolov5')
import train

def main():
    train.run(data='ped.yaml', imgsz=320, weights=params['yolov5']['weights'],epochs= 1,workers=1)

if __name__ == "__main__":
    params = yaml.safe_load(open('params.yaml'))
    # print(params['yolov5']['weights'])
    datapath= sys.argv[1]
    os.makedirs(datapath, exist_ok=True)
    fl = open(os.path.join(datapath,'train.txt'),'w')
    fl.write('train.txt')
    fl.close()
    main()
