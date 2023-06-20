# -*- coding: utf-8 -*-
"""Untitled9.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wUElyXr35UEOYUVck1dbn6Qahxr7SJgb

# Identitas Diri

Nama : Mohammad Dimas Noufal \
Email : dimasnoufal26@gmail.com \
Learning Path : Belajar Pengembangan Machine Learning \
Materi : Proyek Akhir : Image Classification Model Deployment \

# Import (Library)
"""

# Commented out IPython magic to ensure Python compatibility.
import zipfile
import os
import shutil
import pathlib
import tensorflow as tf

!pip install split-folders
import splitfolders as sf

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
# %matplotlib inline

from tensorflow import keras
from google.colab import files
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications import Xception
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GlobalAveragePooling2D
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Dense

"""# Dataset (Kaggle)"""

os.environ['KAGGLE_USERNAME'] = 'mohammaddimasnoufal'
os.environ['KAGGLE_KEY']      = 'e581a5892989a998495d96ef77108e01'

!kaggle datasets download -d kmader/food41

local_zip = '/content/food41.zip'
zip_ref = zipfile.ZipFile(local_zip, 'r')
zip_ref.extractall('food41')
zip_ref.close()

baseDir = 'food41/images'
labels = os.listdir(baseDir)
labels

def remove_label(label):
  shutil.rmtree(os.path.join(baseDir, label))
  labels.remove(label)

remove_label('chicken_wings')
remove_label('hummus')
remove_label('fish_and_chips')
remove_label('eggs_benedict')
remove_label('sashimi')
remove_label('miso_soup')
remove_label('tacos')
remove_label('edamame')
remove_label('onion_rings')
remove_label('baklava')
remove_label('croque_madame')
remove_label('spring_rolls')
remove_label('waffles')
remove_label('red_velvet_cake')
remove_label('fried_calamari')
remove_label('pad_thai')
remove_label('breakfast_burrito')
remove_label('paella')
remove_label('lobster_bisque')
remove_label('beignets')
remove_label('caesar_salad')
remove_label('pulled_pork_sandwich')
remove_label('poutine')
remove_label('shrimp_and_grits')
remove_label('cheesecake')
remove_label('french_toast')
remove_label('macaroni_and_cheese')
remove_label('mussels')
remove_label('risotto')
remove_label('crab_cakes')
remove_label('nachos')
remove_label('beef_tartare')
remove_label('ceviche')
remove_label('donuts')
remove_label('hamburger')
remove_label('gyoza')
remove_label('lasagna')
remove_label('pizza')
remove_label('bibimbap')
remove_label('lobster_roll_sandwich')
remove_label('scallops')
remove_label('spaghetti_carbonara')
remove_label('churros')
remove_label('escargots')
remove_label('hot_and_sour_soup')
remove_label('chicken_curry')
remove_label('omelette')
remove_label('frozen_yogurt')
remove_label('spaghetti_bolognese')
remove_label('hot_dog')
remove_label('cannoli')
remove_label('pancakes')
remove_label('steak')
remove_label('seaweed_salad')
remove_label('tiramisu')
remove_label('club_sandwich')
remove_label('grilled_salmon')
remove_label('french_onion_soup')
remove_label('foie_gras')
remove_label('chicken_quesadilla')
remove_label('beef_carpaccio')
remove_label('greek_salad')
remove_label('carrot_cake')
remove_label('prime_rib')
remove_label('cheese_plate')
remove_label('pork_chop')
remove_label('deviled_eggs')
remove_label('apple_pie')
remove_label('huevos_rancheros')
remove_label('tuna_tartare')
remove_label('strawberry_shortcake')
remove_label('chocolate_mousse')
remove_label('falafel')
remove_label('caprese_salad')
remove_label('beet_salad')
remove_label('dumplings')
remove_label('bread_pudding')
remove_label('french_fries')
remove_label('guacamole')
remove_label('samosa')
remove_label('chocolate_cake')
remove_label('peking_duck')
remove_label('pho')
remove_label('garlic_bread')
remove_label('fried_rice')
remove_label('panna_cotta')
remove_label('oysters')
remove_label('takoyaki')
remove_label('ravioli')
remove_label('ice_cream')
remove_label('cup_cakes')
remove_label('sushi')
remove_label('creme_brulee')
remove_label('ramen')
remove_label('clam_chowder')
remove_label('filet_mignon')
remove_label('gnocchi')

labels

sf.ratio(
    baseDir,
    output = os.path.join('food41/image'),
    seed   = None,
    ratio  = (0.8, 0.2)
)

imageDir = 'food41/image'

trainDirBaby = os.path.join(imageDir, 'train/baby_back_ribs')
trainDirBrus = os.path.join(imageDir, 'train/bruschetta')
trainDirGrilled = os.path.join(imageDir, 'train/grilled_cheese_sandwich')
trainDirMacarons = os.path.join(imageDir, 'train/macarons')

valDirBaby = os.path.join(imageDir, 'val/baby_back_ribs')
valDirBrus = os.path.join(imageDir, 'val/bruschetta')
valDirGrilled = os.path.join(imageDir, 'val/grilled_cheese_sandwich')
valDirMacarons = os.path.join(imageDir, 'val/macarons')

"""# Train set dan Val set"""

trainSet = (
      len(os.listdir(trainDirBaby))
    + len(os.listdir(trainDirBrus))
    + len(os.listdir(trainDirGrilled))
    + len(os.listdir(trainDirMacarons))
)

valSet = (
      len(os.listdir(valDirBaby))
    + len(os.listdir(valDirBrus))
    + len(os.listdir(valDirGrilled))
    + len(os.listdir(valDirMacarons))
)

print(f'Train Set      : {trainSet}')
print(f'Validation Set : {valSet}')

trainDir = os.path.join(imageDir, 'train')
valDir   = os.path.join(imageDir, 'val')

print(os.listdir(trainDir))
print(os.listdir(valDir))

"""# Train"""

trainDatagen = ImageDataGenerator(
    rescale            = 1./255,
    rotation_range     = 30,
    shear_range        = 0.2,
    zoom_range         = 0.2,
    horizontal_flip    = True,
    fill_mode          = 'nearest',
)

valDatagen = ImageDataGenerator(
    rescale         = 1./255
)

trainGen = trainDatagen.flow_from_directory(
    trainDir,
    target_size = (200, 200),
    batch_size  = 50,
    shuffle     = True,
    color_mode  = 'rgb',
    class_mode  = 'categorical',
)

valGen = valDatagen.flow_from_directory(
    valDir,
    target_size = (200, 200),
    batch_size  = 50,
    shuffle     = True,
    color_mode  = 'rgb',
    class_mode  = 'categorical',
)

baseModel = Xception(weights="imagenet", include_top=False, input_shape=(200, 200, 3))

baseModel.trainable = False

baseModel.summary()
print(f'Base Model Layer : {len(baseModel.layers)}')

model = Sequential([
    baseModel,
    GlobalAveragePooling2D(),
    Dense(4, activation='softmax')
])

model.summary()

model.compile(
    optimizer = 'adam',
    loss      = 'categorical_crossentropy',
    metrics   = ['accuracy']
)

class myCallback(tf.keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs={}):
    if logs.get('accuracy') >= 0.90 and logs.get('val_accuracy') >= 0.90:
      print('\nAccuracy and Validation Accuracy reach > 90%')
      self.model.stop_training = True

callbacks = myCallback()

reduceLROP   = tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', patience=3)

epoch = 10

history = model.fit(
    trainGen,
    epochs           = epoch,
    validation_data  = valGen,
    verbose          = 2,
    callbacks        = [callbacks]
)

"""# Grafik

"""

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(len(acc))

plt.plot(epochs, acc, 'r', label='Accuracy')
plt.plot(epochs, val_acc, 'b', label='Val_accuracy')
plt.title('Accuracy & Val_accuracy')
plt.legend(loc=0)
plt.figure()
plt.show()

plt.plot(epochs, loss, 'r', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation_loss')
plt.title('Loss & Validation_Loss')
plt.legend(loc=0)
plt.figure()
plt.show()

print(trainGen.class_indices)

"""# Validasi Photo"""

uploaded = files.upload()

for fn in uploaded.keys():

  path = fn
  img = image.load_img(path, target_size=(150, 150))

  imgplot = plt.imshow(img)
  x = image.img_to_array(img)
  x = np.expand_dims(x, axis=0)
  images = np.vstack([x])

  classes = model.predict(images, batch_size=32)
  print(fn)
  if classes.all() == 0:
        print('baby_back_ribs')
  elif classes.all() == 1:
      print('bruschetta')
  elif classes.all() == 2:
      print('grilled_cheese_sandwich')
  elif classes.all() == 3:
      print('macarons')
  else:
      print('Unclassified')

"""# TF-Lite"""

exportDir = 'saved_model/'
tf.saved_model.save(model, exportDir)

converter    = tf.lite.TFLiteConverter.from_saved_model(exportDir)
tflite_model = converter.convert()

with open('model.tflite', 'wb') as t:
    t.write(tflite_model)