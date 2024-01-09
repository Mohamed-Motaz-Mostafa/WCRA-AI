import numpy as np 
import cv2
from tempfile import TemporaryFile
import glob

hight = 190
width = 190
data = []
label = []
folders = ['empty', 'white', 'black']

for folder in folders:
	for filename in glob.glob(folder+'/*.png'):
		tempImage = cv2.imread(filename)
		if tempImage.shape is not (hight, width,3):
			tempImage = cv2.resize(tempImage, (hight, width))
		data.append(tempImage)
		label.append(np.array(folders.index(folder)))
	print('finished reading '+folder)

data = np.array(data)
label = np.array(label)

# this is a suffling algorithm
idx = np.random.permutation(len(data))
dataShuffeled,lableShuffeled = data[idx], label[idx]

np.savez_compressed("OutFile.npz", data=data, label=label)
np.savez_compressed('OutFileShuffeled.npz', dataShuffeled=dataShuffeled, lableShuffeled=lableShuffeled)
print('finished saving outFile')

npzFile = np.load("OutFile.npz")
npzFileSuffeled = np.load("OutFileShuffeled.npz")
print("finished loading outFile")

# print('data array shape: ', data.shape)
# print('label array shape: ', label.shape)
print('npzFile headers: ', npzFile.files)
print('npzFileSuffeled headers: ', npzFileSuffeled.files)
print('npzFile shape: ', npzFile['data'].shape)
print('npzFileShuffeled shape: ', npzFileSuffeled['dataShuffeled'].shape)