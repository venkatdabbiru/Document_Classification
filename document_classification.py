# -*- coding: utf-8 -*-
"""Document_Classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cFs9i2-c73gAnqNQ5D6GZ1dw-9mkG4-V
"""

!pip install pydicom

!pip install pillow

!pip install kaggle

from google.colab import files
files.upload()

!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/

#change permissions
!chmod 600 ~/.kaggle/kaggle.json

#!kaggle datasets download -d nbhativp/first-half-training
!kaggle datasets download -d pdavpoojan/the-rvlcdip-dataset-test

#####!wget /content/first-half-training.zip
#####!pip install curl
#####!curl -O https://drive.google.com/file/d/0Bz1dfcnrpXM-MUt4cHNzUEFXcmc/view/rvl-cdip.tar.gz
#!wget https://drive.google.com/file/d/0Bz1dfcnrpXM-MUt4cHNzUEFXcmc/view/rvl-cdip.tar.gz
#dataset = pd.read_csv(rawdata)
#!wget /content/rvl-cdip.tar.gz
#!curl https://docs.google.com/uc?id=0Bz1dfcnrpXM-MUt4cHNzUEFXcmc&export=download

#!curl -O https://drive.google.com/file/d/0Bz1dfcnrpXM-MUt4cHNzUEFXcmc/view/rvl-cdip.tar.gz

######!tar --gunzip --extract --verbose --file=/content/rvl-cdip.tar.gz

from zipfile import ZipFile
file_name = "the-rvlcdip-dataset-test.zip"

with ZipFile(file_name, 'r') as zip:
  zip.extractall()
  print('Done')

from keras.layers import Input, Lambda, Dense, Flatten
from keras.models import Model
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array

from sklearn.model_selection import train_test_split

from keras.models import Sequential
import numpy as np
from glob import glob
import matplotlib.pyplot as plt
import sys
import os
import re

import warnings
warnings.filterwarnings('ignore')
from io import BytesIO
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from keras import backend as K
import shutil

files = glob('/content/test/.ipynb_checkpoints/*')
for f in files:
    os.remove(f)

mydir ='/content/test/.ipynb_checkpoints'
try:
    shutil.rmtree(mydir)
except OSError as e:
    print ("Error: %s - %s." % (e.filename, e.strerror))

dataDIR = '/content/test/'

Categories = glob('/content/test/'+'*')

Categories

Categories[0]

cat= []
splitpattern='/*/*/*'
for i in range(len(Categories)):
  Cat_ = Categories[i]
  #samples=sample.astype('float16')
  Category = Cat_.split('/')[-1]
  cat.append(Category)

cat

count_file=0

for path, sub, files in os.walk(dataDIR):
  print("RootPath is: ", path)
  print("Subfolders are: ", sub)
  print("File at Subfolder are: ", files)
  for filename in files:
    if filename.endswith('.tif'):
        try:
            img = Image.open(path +'/'+filename)  # open the image file
            img.verify()  # verify that it is, in fact an image
        except (IOError, SyntaxError) as e:
            print(path +'/'+filename)
            os.remove(path +'/'+filename)
  print('*'*25)
 # It identifies the bad/corrupted image and remove them as well. 
 # Or if you want you can only print the bad/corrupted file name and remove the final script to delete the file.

IMAGE_SIZE = [224, 224]

vgg = VGG16(input_shape=(IMAGE_SIZE +[3]), weights='imagenet', include_top=False)

for layer in vgg.layers:
  layer.trainable = False

x = Flatten()(vgg.output)

prediction = Dense(len(cat), activation='softmax')(x)

model = Model(inputs=vgg.input, outputs=prediction)

model.summary()

model.compile(
    loss='categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

datagen = ImageDataGenerator(validation_split=0.2, rescale=1./255,
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   horizontal_flip=True)

#datagen = ImageDataGenerator(validation_split=0.2,
#                             featurewise_center=True,
#                             featurewise_std_normalization=True,
#                             rotation_range=90,
#                             width_shift_range=0.1,
#                             height_shift_range=0.1,
#                             zoom_range=0.2)

#test_datagen = ImageDataGenerator(rescale=1./255)

training_set = datagen.flow_from_directory(dataDIR,
                                           target_size=(224,224),
                                           batch_size=128,
                                           class_mode='categorical',
                                           subset='training')

test_set = datagen.flow_from_directory(dataDIR,
                                           target_size=(224,224),
                                           batch_size=128,
                                           class_mode='categorical',
                                           subset='validation')

label_map = (training_set.class_indices)

label_map

epochs = 5
batch_size = 128
nb_train_samples=2000
nb_validation_samples =200

if K.image_data_format() == 'channels_first':
  input_shape = (3,224,224)
else:
  input_shape = (224,224,3)
#try:
r =model.fit_generator(
      training_set,
      steps_per_epoch=nb_train_samples,
      validation_steps=nb_validation_samples,
      validation_data= test_set,
      epochs=epochs)
#except Exception as e:
#  print(e)

model.save("my_doc_model_1.h5") #using h5 extension
print("model save!!!")

model.save("doc_model.bin")
pickle.dump(model, open('model_doc.pkl', 'wb'))









