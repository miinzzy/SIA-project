# -*- coding: utf-8 -*-
"""1번_미로_train.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15J-aTwKn7UxH6aXHsdwgcY1juabeawZq

## 필요 모듈 설치
"""

#!pip uninstall -y segmentation-models-pytorch
!pip install pretrainedmodels==0.7.4
!pip install efficientnet_pytorch==0.6.3
!pip install timm==0.4.12
!pip install -U git+https://github.com/albu/albumentations --no-cache-dir

"""## 구글 드라이브 연동"""

import os

import numpy as np
import torch
import random
import cv2
import matplotlib.pyplot as plt

seed = 719
random.seed(seed)
os.environ['PYTHONHASHSEED'] = str(seed)
np.random.seed(seed)
torch.manual_seed(seed)
torch.cuda.manual_seed(seed)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

from google.colab import drive
drive.mount('/gdrive')

workspace_path = '/gdrive/My Drive/Colab Notebooks/SIA'
segmentation_path = os.path.join(workspace_path, 'segmentation_models')

import sys
sys.path.append(segmentation_path)  # segmentation 소스코드 경로 설정

br_train_path = os.path.join(workspace_path, 'LV2_training_set')
x_train_dir = os.path.join(br_train_path, 'images')
y_train_dir = os.path.join(br_train_path, 'labels')

br_valid_path = os.path.join(workspace_path, 'LV2_validation_set')
x_valid_dir = os.path.join(br_valid_path, 'images')
y_valid_dir = os.path.join(br_valid_path, 'labels')

train_building = os.path.join(y_train_dir, 'building')
train_road = os.path.join(y_train_dir, 'road')
valid_building = os.path.join(y_valid_dir, 'building')
valid_road = os.path.join(y_valid_dir, 'road')

building_train_list = []
building_valid_list = []
road_train_list = []
road_valid_list = []

building_train_list = os.listdir(train_building)
building_valid_list = os.listdir(valid_building)
road_train_list = os.listdir(train_road)
road_valid_list = os.listdir(valid_road)

br_train_path = os.path.join(workspace_path, 'LV2_training_set')
n_x_train_dir = os.path.join(br_train_path, 'images')
n_y_train_dir = os.path.join(br_train_path, 'labels_n')

br_valid_path = os.path.join(workspace_path, 'LV2_validation_set')
n_x_valid_dir = os.path.join(br_valid_path, 'images')
n_y_valid_dir = os.path.join(br_valid_path, 'labels_n')

"""#label 이미지 생성"""

import cv2 as cv
import matplotlib.cm as cm
import json
from pathlib import Path

# x, y 좌표로 나눠주는 함수
def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

# train data - building & road 동시 추출
def buidings_roads_train_masking():
    json_list = building_train_list

    for json_name in json_list:

        print(Path(json_name).stem)

        with open(os.path.join(train_building, json_name), "r") as b_json_data, open(os.path.join(train_road, json_name), "r") as r_json_data :

            mask = np.zeros((1024, 1024,3), dtype="uint8")

            b_json_object = json.load(b_json_data)
            r_json_object = json.load(r_json_data)

            for b_element in b_json_object["features"]:
              
              b_imcoords = b_element["properties"]["building_imcoords"]
              
              if b_imcoords == "":
                continue
                
              b_splited_imcoords = b_imcoords.split(",")
              b_divided_imcoords = list_chunk(b_splited_imcoords, 2)
              
              b_polygon = np.array(b_divided_imcoords)
              b_polygon = np.array(b_polygon, np.float64)
              b_polygon = np.array(b_polygon, np.int32)
              
              mask1 = cv2.fillPoly(mask, [b_polygon], (200,200,200))
            
            for r_element in r_json_object["features"]:
              
              r_imcoords = r_element["properties"]["road_imcoords"]
              
              if r_imcoords == "":
                continue
                
              r_splited_imcoords = r_imcoords.split(",")
              r_divided_imcoords = list_chunk(r_splited_imcoords, 2)

              r_polygon = np.array(r_divided_imcoords)
              r_polygon = np.array(r_polygon, np.float64)
              r_polygon = np.array(r_polygon, np.int32)
                          
              mask2 = cv2.fillPoly(mask1, [r_polygon], (255,255,255))
  
            plt.imshow(mask2)
            plt.show()
            cv2.imwrite(os.path.join(n_y_train_dir, Path(json_name).stem+ '.png'), mask2)

buidings_roads_train_masking()

# valid data - building & road 동시 추출
def buidings_roads_valid_masking():
    json_list = building_valid_list

    for json_name in json_list:

        print(Path(json_name).stem)

        with open(os.path.join(valid_building, json_name), "r") as b_json_data, open(os.path.join(valid_road, json_name), "r") as r_json_data :

            mask = np.zeros((1024, 1024,3), dtype="uint8")

            b_json_object = json.load(b_json_data)
            r_json_object = json.load(r_json_data)

            for b_element in b_json_object["features"]:
              
              b_imcoords = b_element["properties"]["building_imcoords"]
              
              if b_imcoords == "":
                continue
                
              b_splited_imcoords = b_imcoords.split(",")
              b_divided_imcoords = list_chunk(b_splited_imcoords, 2)
              
              b_polygon = np.array(b_divided_imcoords)
              b_polygon = np.array(b_polygon, np.float64)
              b_polygon = np.array(b_polygon, np.int32)
              
              mask1 = cv2.fillPoly(mask, np.int32([b_polygon]), (200,200,200))
            
            for r_element in r_json_object["features"]:
              
              r_imcoords = r_element["properties"]["road_imcoords"]
              
              if r_imcoords == "":
                continue
                
              r_splited_imcoords = r_imcoords.split(",")
              r_divided_imcoords = list_chunk(r_splited_imcoords, 2)

              r_polygon = np.array(r_divided_imcoords)
              r_polygon = np.array(r_polygon, np.float64)
              r_polygon = np.array(r_polygon, np.int32)
                          
              mask2 = cv2.fillPoly(mask1, np.int32([r_polygon]), (255,255,255))
  
            plt.imshow(mask2)
            plt.show()
            cv2.imwrite(os.path.join(n_y_valid_dir, Path(json_name).stem+ '.png'), mask2)

buidings_roads_valid_masking()

"""# 샘플 이미지, 레이블 시각화"""

img_list = os.listdir(n_x_train_dir)
v_mask = '/gdrive/My Drive/Colab Notebooks/SIA/label'
check = '/gdrive/My Drive/Colab Notebooks/SIA/check'

for img in img_list:
  img_path = os.path.join(n_x_train_dir, img)
  mask_path = os.path.join(v_mask, img)
  image = cv2.imread(img_path)
  image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  mask = cv2.imread(mask_path)
  mask = cv2.cvtColor(mask, cv2.COLOR_BGR2RGB)
  new_img = cv2.bitwise_or(mask, image)
  plt.imshow(new_img)
  plt.show()
  cv2.imwrite(os.path.join(check, img), new_img)

"""## 데이터로더 정의"""

from torch.utils.data import DataLoader
from torch.utils.data import Dataset as BaseDataset

class Dataset(BaseDataset):
    
    CLASSES = ['building', 'road']
    
    def __init__(
            self, 
            images_dir, 
            masks_dir, 
            classes=None, 
            augmentation=None, 
            preprocessing=None,
    ):
        self.ids = os.listdir(images_dir)
        self.images_fps = [os.path.join(images_dir, image_id) for image_id in self.ids]
        self.masks_fps = [os.path.join(masks_dir, image_id) for image_id in self.ids]
        
        # convert str names to class values on masks
        self.class_values = [self.CLASSES.index(cls.lower()) for cls in classes]

        for i in range(len(self.masks_fps)):
          self.mask_ids = np.unique(cv2.imread(self.masks_fps[i], 0))[1:]
          if len(self.mask_ids) == len(self.class_values):
            break
        
        self.augmentation = augmentation
        self.preprocessing = preprocessing
    
    def __getitem__(self, i):
        
        # read data
        image = cv2.imread(self.images_fps[i])
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mask = cv2.imread(self.masks_fps[i], 0)
        
        # extract certain classes from mask (e.g. cars)
        masks = [(mask == self.mask_ids[v]) for v in self.class_values]
        mask = np.stack(masks, axis=-1).astype('float')
        
        # apply augmentations
        if self.augmentation:
            sample = self.augmentation(image=image, mask=mask)
            image, mask = sample['image'], sample['mask']
        
        # apply preprocessing
        if self.preprocessing:
            sample = self.preprocessing(image=image, mask=mask)
            image, mask = sample['image'], sample['mask']
            
        return image, mask
        
    def __len__(self):
        return len(self.ids)

# helper function for data visualization
def visualize(**images):
    """PLot images in one row."""
    n = len(images)
    plt.figure(figsize=(16,5))
    for i, (name, image) in enumerate(images.items()):
        plt.subplot(1, n, i + 1)
        plt.xticks([])
        plt.yticks([])
        plt.title(' '.join(name.split('_')).title())
        plt.imshow(image)
    plt.show()

# Lets look at data we have

dataset = Dataset(n_x_train_dir, n_y_train_dir, classes=['building','road'])

for i in range(3):
  n = np.random.choice(len(dataset))
  image, mask = dataset[n]  # get some sample
  visualize(
    image=image,
    mask_building=mask[:, :, 0].squeeze(),
    mask_road=mask[:, :, 1].squeeze(),
    )

"""## 데이터증대"""

import albumentations as albu

def get_training_augmentation():
    train_transform = [

        albu.HorizontalFlip(p=0.5),

        albu.ShiftScaleRotate(scale_limit=0.5, rotate_limit=0, shift_limit=0.1, p=1, border_mode=0),

        albu.PadIfNeeded(min_height=320, min_width=320, always_apply=True, border_mode=0),
        albu.RandomCrop(height=320, width=320, always_apply=True),

        albu.IAAAdditiveGaussianNoise(p=0.2),
        albu.IAAPerspective(p=0.5),

        albu.OneOf(
            [
                albu.CLAHE(p=1),
                albu.RandomBrightness(p=1),
                albu.RandomGamma(p=1),
            ],
            p=0.9,
        ),

        albu.OneOf(
            [
                albu.IAASharpen(p=1),
                albu.Blur(blur_limit=3, p=1),
                albu.MotionBlur(blur_limit=3, p=1),
            ],
            p=0.9,
        ),

        albu.OneOf(
            [
                albu.RandomContrast(p=1),
                albu.HueSaturationValue(p=1),
            ],
            p=0.9,
        ),
    ]
    return albu.Compose(train_transform)


def get_validation_augmentation():
    """Add paddings to make image shape divisible by 32"""
    test_transform = [
        albu.PadIfNeeded(384, 480)
    ]
    return albu.Compose(test_transform)


def to_tensor(x, **kwargs):
    return x.transpose(2, 0, 1).astype('float32')


def get_preprocessing(preprocessing_fn):
    """Construct preprocessing transform
    
    Args:
        preprocessing_fn (callbale): data normalization function 
            (can be specific for each pretrained neural network)
    Return:
        transform: albumentations.Compose
    
    """
    
    _transform = [
        albu.Lambda(image=preprocessing_fn),
        albu.Lambda(image=to_tensor, mask=to_tensor),
    ]
    return albu.Compose(_transform)

augmented_dataset = Dataset(
    n_x_train_dir, 
    n_y_train_dir, 
    augmentation=get_training_augmentation(), 
    classes=['building', 'road'],
)

# same image with different random transforms
for i in range(3):
    image, mask = augmented_dataset[23]
    visualize(image=image,              
              mask_building=mask[:, :, 0].squeeze(),
              mask_road=mask[:, :, 1].squeeze(),
              )

"""## 모델 생성 및 훈련"""

import torch
import numpy as np
import time
import segmentation_models_pytorch as smp

ENCODER = 'se_resnext50_32x4d'
ENCODER_WEIGHTS = 'imagenet'
CLASSES = ['building', 'road']
ACTIVATION = 'sigmoid' # could be None for logits or 'softmax2d' for multiclass segmentation
DEVICE = 'cuda'

# create segmentation model with pretrained encoder
model = smp.Unet(
    encoder_name=ENCODER, 
    encoder_weights=ENCODER_WEIGHTS, 
    classes=len(CLASSES), 
    activation=ACTIVATION,
)

preprocessing_fn = smp.encoders.get_preprocessing_fn(ENCODER, ENCODER_WEIGHTS)

train_dataset = Dataset(
    n_x_train_dir, 
    n_y_train_dir, 
    augmentation=get_training_augmentation(), 
    preprocessing=get_preprocessing(preprocessing_fn),
    classes=CLASSES,
)

valid_dataset = Dataset(
    n_x_valid_dir, 
    n_y_valid_dir, 
    augmentation=get_validation_augmentation(), 
    preprocessing=get_preprocessing(preprocessing_fn),
    classes=CLASSES,
)

train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True, num_workers=2)
valid_loader = DataLoader(valid_dataset, batch_size=2, shuffle=False, num_workers=1)

loss = smp.utils.losses.DiceLoss()
metrics = [
    smp.utils.metrics.IoU(threshold=0.5),
]

optimizer = torch.optim.Adam([ 
    dict(params=model.parameters(), lr=0.0001),
])

train_epoch = smp.utils.train.TrainEpoch(
    model, 
    loss=loss, 
    metrics=metrics, 
    optimizer=optimizer,
    device=DEVICE,
    verbose=True,
)

valid_epoch = smp.utils.train.ValidEpoch(
    model, 
    loss=loss, 
    metrics=metrics, 
    device=DEVICE,
    verbose=True,
)

max_score = 0

iou = []
miou = 0

save_dir = os.path.join(workspace_path, 'ckpt')
os.makedirs(save_dir, exist_ok=True)

num_valid_images = len(os.listdir(n_x_valid_dir))

for i in range(0, 500):
    print('\nEpoch: {}'.format(i))
    train_logs = train_epoch.run(train_loader)
    
    start_time = time.time()
    valid_logs = valid_epoch.run(valid_loader)
    end_time = time.time()
    
    # do something (save model, change lr, etc.)
    if max_score < valid_logs['iou_score']:
        max_score = valid_logs['iou_score']
        torch.save(model, os.path.join(save_dir, 'best_model_1204.pth'))
        print('Model saved!')
        
    if i == 400:
        optimizer.param_groups[0]['lr'] = 1e-5
        print('Decrease decoder learning rate to 1e-5!')

    iou.append(valid_logs['iou_score'])
    print(max_score)
    print("fps: ", (end_time - start_time)/ num_valid_images)

print('max_score = '+str(max_score))

"""## 이미지 시각화"""

best_model = torch.load(os.path.join(save_dir, 'best_model_1204.pth'))

valid_dataset_vis = Dataset(
    n_x_valid_dir, n_y_valid_dir, 
    classes=CLASSES,
)

def color(mask):
  new_mask = np.zeros(mask[0].shape, np.uint8)

  for i, value in enumerate(mask):
    new_mask[value == 1] = i+1
  return new_mask

for i in range(5):
    n = np.random.choice(len(valid_dataset))
    
    image_vis = valid_dataset_vis[n][0].astype('uint8')
    image, gt_mask = valid_dataset[n]

    gt_mask = gt_mask.squeeze()
    x_tensor = torch.from_numpy(image).to(DEVICE).unsqueeze(0)
    pr_mask = best_model.predict(x_tensor)

    pr_mask = pr_mask.squeeze().cpu().numpy().round()

    visualize(
        image=image_vis, 
        both_ground_mask = color(gt_mask),
        both_mask = color(pr_mask),
    )