from keras.preprocessing.image import ImageDataGenerator,array_to_img, img_to_array, load_img
import os
from tqdm import tqdm

datagen = ImageDataGenerator(
    rotation_range=60,
    width_shift_range=0.3,
    height_shift_range=0.3,
    rescale=1./255,
    shear_range=0.3,
    zoom_range=0.3,
    horizontal_flip=False,
    fill_mode='nearest'
)




path = 'D:/MLDataset/ImageAnalysis/Direction/front/'
name = 'Front('
end = ').png'

for i in range(1,42):
    imagePath = path + name + str(i) + end
    img = load_img(imagePath)
    x = img_to_array(img)
    x = x.reshape((1,) + x.shape)


    print("Creating New Images pass:" , i)
    i = 0
    for batch in datagen.flow(x, batch_size= 1, save_to_dir="preview",
                          save_prefix="Front", save_format='.png'):
        i +=1
        if i >300:
            break


print("Finished Making data")