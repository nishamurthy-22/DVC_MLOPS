import sys 
import yaml
import os

sys.path.insert(0, 'model/yolov5')
import val

def main():
    val.run(data="model/yolov5/data/ped.yaml",weights=params['yolov5']['weights'],workers=1, half=False, imgsz=320)

if __name__ == "__main__":
    params = yaml.safe_load(open('params.yaml'))
    datapath= sys.argv[1]
    os.makedirs(datapath, exist_ok=True)
    fl = open(os.path.join(datapath,'predict.txt'),'w')
    fl.write('predict.txt')
    fl.close()  
    main()