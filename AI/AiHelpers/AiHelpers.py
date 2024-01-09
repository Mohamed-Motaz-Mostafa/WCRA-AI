#import sys
from keras.models import load_model
from copy import deepcopy
import numpy as np

print('loding model..........')
model=load_model('AI/ourAiModel')

print ('model loded sucessfuly .....')
def runAiModel(square):
    image = deepcopy(square)
    image = [image]
    image = np.array(image)
    image = (image/127)-1
    temp = model.predict(image)
    temp=temp[0]
    print('temp =======================>>>>' ,temp)
    modelOutput = np.where(temp == np.amax(temp))
    modelOutput= modelOutput[0][0]
    print('model Output  : ' ,modelOutput)
    return modelOutput

