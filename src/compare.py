import yaml
import os
import pandas as pd
import sys

datapath= sys.argv[1]
os.makedirs(datapath, exist_ok=True) 

fl = open(os.path.join(datapath,'compare.txt'),'w')
fl.write('compare.txt')
fl.close()

params = yaml.safe_load(open('params.yaml'))
count=params['yolov5']['count']

train_met = 'runs/train/exp'
val_met = 'runs/val/exp'

if count!=1:
    train_met = train_met + str(count)
    val_met = val_met + str(count)

df1= pd.read_csv(os.path.join(train_met,'metrics.csv'))
df2=pd.read_csv(os.path.join(val_met,'metrics.csv'))

print(df1)
print(df2)

f1_train=df1.iloc[0,5]
f1_val=df2.iloc[0,5]

if (f1_train > f1_val):
    print('Current trained model is better than previous model. Hence registering')
    print(os.path.join(train_met,'weights','best.pt'))
    params['yolov5']['weights'] = os.path.join(train_met,'weights','best.pt')
    params['yolov5']['count']= params['yolov5']['count'] + 1
    yaml.dump(params, open('params.yaml', 'w'), sort_keys=False)
    
else:
    print("Previous model is better than current trained model.")
    params['yolov5']['count'] = params['yolov5']['count'] + 1
    yaml.dump(params, open('params.yaml', 'w'), sort_keys=False)

