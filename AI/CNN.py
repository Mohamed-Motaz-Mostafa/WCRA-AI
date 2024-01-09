from tensorflow import keras
from keras import layers
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


# Normalize: 0,255 -> 0,1
train_images = (train_images / 127.0) -1
test_images  = (test_images / 127.0) -1
print("data normalized")

#                 0         1       2
class_names = ['Empty', 'White', 'Black']

# model...
model = keras.models.Sequential()
model.add(layers.Conv2D(3, (3,3), strides=(1,1), padding="valid", activation='relu', input_shape=(190,190,3)))
model.add(layers.MaxPool2D((5,5)))
model.add(layers.Conv2D(3, 3, activation='relu'))
model.add(layers.MaxPool2D((2,2)))
model.add(layers.Flatten())
model.add(layers.Dense(100, activation='relu'))
model.add(layers.Dense(3,activation='relu'))
print(model.summary())

# loss and optimizer
loss = keras.losses.SparseCategoricalCrossentropy(from_logits=True)
optim = keras.optimizers.Adam(lr=1e-4)
metrics = ["accuracy"]

model.compile(optimizer=optim, loss=loss, metrics=metrics)

# training
batch_size = 150
epochs = 100

model.fit(train_images, train_labels, epochs=epochs,
          batch_size=batch_size, verbose=2,shuffle=True)

model.save("ourAiModel.pb")

print('*********************************************************************************************')
# evaulate
model.evaluate(test_images,  test_labels, batch_size=batch_size, verbose=2)

# print('*********************************************************************************************')
# prediction = model.predict(test_images)
# print('predictions', prediction)
# predictionLabels =[]
# for i in prediction:
#     predictionLabels.append(class_names[list(i).index(max(list(i)))])
# print("prediction labels: ",predictionLabels)