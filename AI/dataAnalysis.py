import numpy as np

npzShuffeled = np.load("OutFileShuffeled.npz")
print("file loaded")
print("file headers: ", npzShuffeled.files)

train_images = npzShuffeled["dataShuffeled"][:15066]
test_images = npzShuffeled["dataShuffeled"][15066:]
train_labels = npzShuffeled["lableShuffeled"][:15066]
test_labels = npzShuffeled["lableShuffeled"][15066:]
print("data splitted")
print("data shape: ", train_images.shape)

emptyCounter = 0
whiteCounter = 0
blackCounter = 0

for i in test_labels:
    if i == 0:
        emptyCounter += 1
    if i == 1:
        whiteCounter += 1
    if i == 2:
        blackCounter += 1

print("the number of empty piecese is: ", emptyCounter)
print("the number of white piecese is: ", whiteCounter)
print("the number of black piecese is: ", blackCounter)