import os
import cv2

data_dir = "gtsrb"
# img = cv.imread('messi5.jpg')
if not data_dir in os.listdir(os.getcwd()):
    raise Exception("Wrong directory path")

if not os.path.isdir(data_dir):
    raise Exception("path is not a directory")

images = list()
labels = list()

for i in range(1):
    if f"{i}" not in os.listdir(data_dir):
        raise Exception(f"Directory Missing : {i}")
    sign_dir = os.path.join(data_dir ,f"{i}")
    for image in os.listdir(sign_dir):
        try:
            image_path = os.path.join(sign_dir , image)
            img = cv2.imread(os.path.join(image_path))
            resized_img = cv2.resize(img , (30 , 30))
            resized_img = resized_img / 255.0
            images.append(resized_img)
            labels.append(i)
        except:
            raise Exception(f"Image not loadable : {os.path.join(sign_dir , image)}")
        
print(images)
print(labels)