# -*- coding: utf-8 -*-
"""Auto_File_Process.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PRDRacxbSVYUaOiykNkrC4yEWNH_JUU8
"""

import os
import numpy as np
import sys
import os
import glob
import re

#from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
from keras.applications.vgg16 import decode_predictions
from werkzeug.utils import secure_filename
from PIL import Image
import shutil

model_path = 'my_doc_model_1.h5'
model=load_model(model_path)
#model._make_predict_function()

def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))
    
    x = image.img_to_array(img)
    
    x = np.expand_dims(x, axis=0)
    
    x = preprocess_input(x)
    
    preds = model.predict(x)
    
    return preds

def auto_files(fl_in_path,fl_out_path):
    #1 get all files in the folder
    file_list = os.listdir(fl_in_path)
    saved_path=os.getcwd()
    os.chdir(fl_in_path)
    
    #if os.path.isfile
    for file in file_list:
        #print(file)
        
        fl_path= os.path.join(fl_in_path, file)
        result = model_predict(fl_path, model)
        y_classes = result.argmax(axis=-1)
        #print("class is ----",y_classes)
        word_dict = {'advertisement': 0,
                     'email': 1,
                     'form': 2,
                     'handwritten': 3,
                     'invoice': 4,
                     'memo': 5,
                     'news_article': 6,
                     'resume': 7,
                     'scientific_publication': 8,
                     'specification': 9}
        result = [cat for cat, val in word_dict.items() if val == y_classes]
        prediction = ''.join(result)
        #print(prediction)
        
        
        output_files = os.path.join(fl_out_path, prediction+'-'+file)
        print(output_files)
        shutil.move(fl_path, output_files)
        #os.rename(file,output_files)
            
        #return str(result)
    os.chdir(saved_path)
    print("Done....!!!")
    
    #2 call ML predict function for each image file
fl_in_path='C:/MyFolders/ML-POC/Document_Classification/autofiles'
fl_out_path='C:/MyFolders/ML-POC/Document_Classification/auto_out/' 
auto_files(fl_in_path, fl_out_path)