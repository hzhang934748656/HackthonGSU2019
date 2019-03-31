
img_path = "fish2_test.png"
from keras.models import load_model
from matplotlib.pyplot import imshow
from keras.preprocessing import image
from keras.applications.imagenet_utils import preprocess_input
import numpy as np
width,height = 256,256
model = load_model("mymodel.h5")

#img_path = '00.png'
img = image.load_img(img_path,target_size = (width,height))
imshow(img)
x = image.img_to_array(img)
x = np.expand_dims(x,axis = 0)
x = preprocess_input(x)

result = model.predict(x)


img_path = "banana_test.png"
img = image.load_img(img_path,target_size = (width,height))
imshow(img)
x = image.img_to_array(img)
x = np.expand_dims(x,axis = 0)
x = preprocess_input(x)

result = model.predict(x)


a= result>0.5
if a[0][0]==True:
    goal = 'apple'
elif a[0][1]==True:
    goal = 'banana'
elif a[0][2]==True:
    goal = 'bus'
else:
    goal ='fish'
print(goal)