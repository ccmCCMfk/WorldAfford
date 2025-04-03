import os
import cv2
import numpy as np
from PIL import Image
import json

def process_json(img_path,json_path,save_path,viz_path):
    k_ratio=3
    image=np.array(Image.open(img_path).convert("RGB"))
    k_size = int(np.sqrt(image.shape[0] * image.shape[1]) / k_ratio)
    if k_size % 2 == 0:
        k_size += 1
    mask = np.zeros((image.shape[0],image.shape[1]))
    with open(json_path, 'r') as load_f:
        json_data = json.load(load_f)
        shapes=json_data['shapes']
        for shape in shapes:
            point=shape['points'][0]
            x = point[1]
            y = point[0]
            row = int(x)
            col = int(y)
            mask[row, col] += 1.0
        mask = cv2.GaussianBlur(mask, (k_size, k_size), 0)
        mask = (mask - np.min(mask)) / (np.max(mask) - np.min(mask) + 1e-10)*255.0
        cv2.imwrite(save_path,mask)
        mask_2=np.zeros((image.shape[0],image.shape[1],3))
        mask_2[:,:,0]=mask
        fuse=mask_2*0.7+image*0.3
        cv2.imwrite(viz_path,fuse)

# img_root=r"/data/new_dataset/GroudTruth/testset/egocentric"
# save_root=r"/data/new_dataset/GroudTruth/testset/masks"
# img_save_root=r"/data/new_dataset/GroudTruth/testset/GT"
# viz_root=r"/data/new_dataset/GroudTruth/testset/viz"
img_root=r"/data/new_dataset/datasetformultipleobjects/test_gt/environment/"
save_root=r"/data/new_dataset/datasetformultipleobjects/test_gt/masks"
img_save_root=r"/data/new_dataset/datasetformultipleobjects/test_gt/GT"
viz_root=r"/data/new_dataset/datasetformultipleobjects/test_gt/viz"
affs=os.listdir(img_root)
img_list=[]
for aff in affs:
    aff_path=os.path.join(img_root,aff)
    objs=os.listdir(aff_path)
    for obj in objs:
        obj_path=os.path.join(aff_path,obj)
        images=os.listdir(obj_path)
        for img in images:
            if img[-4:]=="json":
                continue
            if img[-6:]=="_1.png" or img[-6:]=="_2.png":
                continue
            img_list.append(img)
            img_path = os.path.join(obj_path, img)

            if os.path.exists(img_path[:-3] + "json"):

                save_path = os.path.join(save_root, aff,obj, img[:-3] + "png")
                viz_path = os.path.join(viz_root, aff, obj,img[:-3] + "png")

                if not os.path.exists(os.path.join(save_root, aff,obj)):
                    os.makedirs(os.path.join(save_root, aff,obj))
                if not os.path.exists(os.path.join(viz_root, aff,obj)):
                    os.makedirs(os.path.join(viz_root, aff,obj))

                process_json(img_path, img_path[:-3] + "json", save_path, viz_path)
                print(save_path)

            elif os.path.exists(img_path[:-4] + "_1.png"):

                save_path = os.path.join(save_root, aff,obj, img[:-3] + "png")
                viz_path = os.path.join(viz_root, aff,obj, img[:-3] + "png")

                if not os.path.exists(os.path.join(save_root, aff,obj)):
                    os.makedirs(os.path.join(save_root, aff,obj))
                if not os.path.exists(os.path.join(viz_root, aff,obj)):
                    os.makedirs(os.path.join(viz_root, aff,obj))

                mask = np.array(Image.open(img_path[:-4] + "_1.png"))
                mask = mask[:, :, 3]
                k_ratio = 3
                image = np.array(Image.open(img_path).convert("RGB"))
                k_size = int(np.sqrt(mask.shape[0] * mask.shape[1]) / k_ratio)
                if k_size % 2 == 0:
                    k_size += 1
                mask = cv2.GaussianBlur(mask, (k_size, k_size), 0)
                mask = (mask - np.min(mask)) / (np.max(mask) - np.min(mask) + 1e-10) * 255.0
                cv2.imwrite(save_path, mask)
                mask_2 = np.zeros((image.shape[0], image.shape[1], 3))
                mask_2[:, :, 0] = mask
                fuse = mask_2 * 0.7 + image * 0.3
                cv2.imwrite(viz_path, fuse)

                print(save_path)