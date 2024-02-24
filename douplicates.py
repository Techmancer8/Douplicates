import os
from tqdm import tqdm
from os.path import getsize as size
from PIL import Image, ImageChops
import argparse


folder = 'PATH/TO/IMAGE/FOLDER'
doup_folder = './Douplicates'

images=list()
c = 0
if not os.path.isdir(doup_folder): os.mkdir(doup_folder)
def move(f):
    # Moves file to folder be removed
    path = f'{doup_folder}/{os.path.split(f)[-1]}'
    if os.path.exists(path): path+='2'
    os.rename(f,path)
    global c
    c+=1

for root,x,files in os.walk(folder):
    for i in files:
        name,ext = os.path.splitext(i)
        if ext not in ['.jpg','.jpeg','.png','.webp']: 
            continue
        path = root+'/'+i
        images.append(path.replace('\\','/'))

b = '{desc:<40}: {percentage:3.0f}%|{bar}'

imglist1 = tqdm(images,bar_format=b)
for image1 in imglist1:
    images.pop(0)
    imglist1.set_description(os.path.split(image1)[-1])
    imglist2 = tqdm(images,leave=False,bar_format=b)
    for image2 in imglist2:
        if image1==image2:continue
        imglist2.set_description(os.path.split(image2)[-1])

        diff = ImageChops.difference(Image.open(image1),Image.open(image2))
            
        if not diff.getbbox():#not different, doup found
            if size(image1) > size(image2) or os.path.splitext(image2)[1] == '.webp' or len(os.path.split(image1)) > len(os.path.split(image2)):
                move(image2)
            else:
                move(image1)
                break

print(f'Moved {c} files')