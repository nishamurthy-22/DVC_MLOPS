import streamlit as st
import yaml
import os
import model.yolov5.detect as detect
import pandas as pd
import numpy as np
import shutil
import matplotlib.pyplot as plt
import json
import cv2

params = yaml.safe_load(open('params.yaml'))

def pipeline():
    st.subheader('Choose Dataset')
    opts = os.listdir('datasets')
    opts.sort()
    option = st.selectbox('',opts)
    if st.button('Run Pipeline'):
        st.subheader('Running YoloV5 Pipeline..........')
        params["yolov5"]['dpath'] = option
        yaml.dump(params, open('params.yaml', 'w'), sort_keys=False)
        
        if not os.system("dvc repro"):
            st.success('Pipeline executed successfully')
            st.balloons()
            st.snow()
            show_metrics()
        else:
            st.error("Pipleine execution failed")

def show_metrics():
    params = yaml.safe_load(open('params.yaml'))
    count = params['yolov5']['count'] - 1
    train_met = 'runs/train/exp'
    val_met = 'runs/val/exp'
    
    if count == 0:
        st.title('TRAIN A DATASET TO EVALUATE METRICS')
    else:
        if count!=1:
            train_met = train_met + str(count)
            val_met = val_met + str(count)
        
        df1= pd.read_csv(os.path.join(train_met,'metrics.csv'))
        df2=pd.read_csv(os.path.join(val_met,'metrics.csv'))
        
        coll1 = df2["F1-Score"]
        coll1 = coll1.to_numpy()
        coll1 = np.reshape(coll1,(3,1))
        
        coll2 = df1["F1-Score"]
        coll2 = coll2.to_numpy()
        coll2 = np.reshape(coll2,(3,1))
        
        chart_data = pd.DataFrame(np.concatenate((coll1,coll2), axis = 1), columns=['Old model', 'New model'])
        st.write("## F1-Score")
        st.line_chart(chart_data)
        col1, col2 = st.columns(2)
        col1.write("## New model")
        col1.write("### Confusion Matrix")
        col1.image(os.path.join(train_met,"confusion_matrix.png"))
        col1.write('\n')
        col1.write("### F1 Curve")
        col1.image(os.path.join(train_met,"F1_curve.png"))

        col2.write("## Previous best model")
        col2.write("### Confusion Matrix")
        col2.image(os.path.join(val_met,"confusion_matrix.png"))
        
        col2.write('\n')
        col2.write("### F1 Curve")
        col2.image(os.path.join(val_met,"F1_curve.png"))

        col1.write("### New model metrics")
        metrics_path = os.path.join(train_met,"metrics.csv")
        df = pd.read_csv(metrics_path)
        col1.write(df)

        col2.write("### Previous best metrics")
        metrics_path = os.path.join(val_met,"metrics.csv")
        df = pd.read_csv(metrics_path)
        col2.write(df)


def hero_page():
    st.image('assets/hero.jpeg', width=1000)

def predict_image():
    img = st.file_uploader("Upload Image")
    if img:
        with open(f'detect/image.png', "wb") as f:
            f.write(img.getbuffer())
        st.subheader('Predicting........')
        st.image('detect/image.png')
        detect.run(weights=params['yolov5']['weights'], source='detect/image.png')
        st.success('Prediction Successful')
        st.image('runs/detect/exp/image.png')


def main():
    st.set_page_config(layout="wide")
    st.title("MLOps Pipeline for Pedestrian Detection")
    pages = {
        "Choose one of the following":hero_page,
        "Train Dataset": pipeline,
        "Predict on an Image": predict_image,
        "Metrics": show_metrics,
    }

    st.sidebar.image('assets/PESLogo.jpg')
    
    st.markdown("""---""")
    st.sidebar.markdown("""---""")
    st.sidebar.title('Select Model -')
    opp = st.sidebar.selectbox('',("Choose one of the following",'yolov5'))

    if opp == "Choose one of the following":
        hero_page()
    elif opp == 'yolov5':
        selected_page = st.sidebar.selectbox('',pages.keys())
        pages[selected_page]()

if __name__ == '__main__':
    main()