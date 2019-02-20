from keras.models import load_model
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense

from keras.preprocessing.image import img_to_array, load_img
import numpy as np
import tensorflow as tf
from model import DirectionModel as DM

'''
Lables
{'back': 0, 'front': 1, 'left': 2, 'right': 3}
'''
#Size of the image and is color
input_shape = (150, 150, 3)

model = DM.make_model(input_shape)
model = load_model('first_model.h5')



correct = 0


back1 = "test/back.jpg"
back_one, _ = DM.process_image(back1, model)
if back_one == 0: correct +=1

back2 = "test/back2.jpg"
back_two, _ = DM.process_image(back2, model)
if back_two == 0: correct +=1

front1 = "test/front.jpg"
front_one, _ = DM.process_image(front1, model)
if front_one == 1: correct +=1

front2 = "test/f.png"
front_two, _ = DM.process_image(front2, model)
if front_two == 1: correct +=1

front3 = "test/front2.jpg"
front_three, _ = DM.process_image(front3, model)
if front_three == 1: correct +=1

right1 = "test/right.jpg"
right_one, _ = DM.process_image(right1, model)
if right_one == 3: correct +=1

right2 = "test/right.jpg"
right_two, _ = DM.process_image(right2, model)
if right_two == 3: correct +=1

right3 = "test/right2.jpg"
right_three, _ = DM.process_image(right3, model)
if right_three == 3: correct +=1


left = "test/left.jpg"
left_one, _ = DM.process_image(left, model)
if left_one == 2: correct +=1

left2 = "test/left2.jpg"
left_two, _ = DM.process_image(left2, model)
if left_two == 2: correct +=1


print("Accruacy:", correct/10)

print("Should be 0  B1:{}  B2{}".format(back_one, back_two))
print("Should be 1  F1:{}  F2{}  F3{}".format(front_one, front_two, front_three))
print("Should be 2  L1:{}  L2{} ".format(left_one, left_two))
print("Should be 3  R1:{}  R2{}  R3{}".format(right_one, right_two, right_three))


