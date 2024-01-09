from multiprocessing.connection import wait
import numpy as np 
import cv2
from copy import deepcopy
import subprocess

def playVideo():
    cap = cv2.VideoCapture(0)
    while(True):
        ret, frame = cap.read()
        cv2.imshow('frame',frame)
        ch = cv2.waitKey(1)
        if ch & 0xff == ord('q'):
            break

def captureImage(showImage = True ):

    bashCmd = ['libcamera-still', '-n','-o' ,'/home/pi/Grad-Project/ImageProcessing/rawData/tempFrame.png', '>', '/dev/null']

    process= subprocess.Popen(bashCmd, stdout=subprocess.PIPE)

    output,error= process.communicate()
    frame = cv2.imread("/home/pi/Grad-Project/ImageProcessing/rawData/tempFrame.png")
    if showImage:
        cv2.imshow('img1',frame) #display the captured image
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    return frame
def boardPreProcessor(board, showBoard = False):
    Board = deepcopy(board)
    #cv2.imshow('board',Board)
    gray = cv2.cvtColor(Board,cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,255,-25)
    thresh2 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,255,-25)
    thresh_erode = cv2.erode(thresh,(5,5),iterations=1)
    thresh_erode = cv2.dilate(thresh,(5,5),iterations=1)
    normalBoard = cv2.erode(thresh2,(5,5),iterations=1)
    invertedBoard = cv2.dilate(thresh2,(5,5),iterations=1)
    normalBoard = cv2.cvtColor(normalBoard,cv2.COLOR_GRAY2BGR)
    invertedBoard = cv2.cvtColor(invertedBoard,cv2.COLOR_GRAY2BGR)
    if showBoard:
        cv2.imshow('threh eroded',normalBoard)
        cv2.imshow('threh eroded2',invertedBoard)
    return normalBoard , invertedBoard

def splitBoard(image, inputMode = 'image', returnMode = 'store', showCells = True, name = ''):
    '''
    @param: image >>> input image or image path
    @param: inputMode >>> chose to use image or path as input 
    @param: returnMode >>> chose whether to return the image of save it to file
    @param: showCells >>> chose to show the images for debugging or not 
    @param: name >>> name of file if inputMode is "path"
    @return: list of np.arrays representing the board squares
    '''
    cells = []
    img = np.array(0)
    if inputMode == 'image':
        img = deepcopy(image)

    elif inputMode == 'path':
        img = cv2.imread(image)

    counter = 0 
    pexilMargin = int(5/1550*img.shape[0])
    
    for i in range(1,9):
        x = int(i/8 * img.shape[0]) - pexilMargin
        x_1 = int((i-1)/8 * img.shape[0]) + pexilMargin
        for j in range(1,9):
            y = int(j/8 * img.shape[1]) - pexilMargin
            y_1 = int((j-1)/8 * img.shape[0]) + pexilMargin
            cells.append(np.array(img[x_1:x,y_1:y]))
            # Unit Test code 
            cropedImage = np.array(img[x_1:x,y_1:y])
            #resizedImage = cv2.resize(cropedImage,(50,50))
            if showCells:
                cv2.imshow(name+str(counter),cropedImage)
                counter += 1
            if returnMode == "store":
                cv2.imwrite('./SplitedData/'+name+str(counter)+'.png' , cropedImage )
                counter += 1
    if returnMode == "cells":
        return cells
            
    if showCells:
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def findPoints( image ,inputMode = 'path', showPoints= False ) :

    # This is a termination criteria
    criteria = ( cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER ,30 , 0.001)
    
    if inputMode == 'path':
        img = deepcopy(cv2.imread (image)) # Reads the image
        
    elif inputMode == 'image':
        img = deepcopy(image)

    gray = cv2.cvtColor (img ,cv2.COLOR_BGR2GRAY ) # Converts the image to grayscale .
    ret = False
    
    # Find the chessboard inner corners
    ret , corners = cv2.findChessboardCornersSB( gray , (7 ,7), cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_NORMALIZE_IMAGE + cv2.CALIB_CB_FILTER_QUADS )
    
    # If corners are found , object and image points are added .
    # This section is not needed but can provide futher understanding of the program
    # as it displays the identified chessboard corners on top of the image .
    if showPoints == True:
        if ret == True :
            cv2.cornerSubPix( gray , corners , (11 ,11) , ( -1 , -1) , criteria )
            cv2.drawChessboardCorners( img , (7 ,7) , corners , ret )
            cv2.imshow('img' , img )
            cv2.waitKey(0)
        cv2.destroyAllWindows ()

    if ret:
        Top_Left_x=2* corners[0][0][0] - corners[8][0][0]
        Top_Left_y = 2* corners[0][0][1] - corners[8][0][1]
        Top_Right_x = 2* corners[6][0][0] - corners[12][0][0]
        Top_Right_y = 2* corners[6][0][1] - corners[12][0][1]
        Bottom_Left_x = 2* corners[42][0][0] - corners[36][0][0]
        Bottom_Left_y = 2* corners[42][0][1] - corners[36][0][1]
        Bottom_Right_x = 2* corners[48][0][0] - corners[40][0][0]
        Bottom_Right_y = 2* corners[48][0][1] - corners[40][0][1]
        Bottom_Left = ( Bottom_Left_x , Bottom_Left_y )
        Bottom_Right = ( Bottom_Right_x , Bottom_Right_y )
        Top_Left = ( Top_Left_x , Top_Left_y )
        Top_Right = ( Top_Right_x , Top_Right_y )
    
        pts = np.array( [Top_Left, Top_Right, Bottom_Left, Bottom_Right], dtype="float32")
        return ret, pts
    else:
        return False, False

def orderPoints(pts ) :
    # Initialise a list . The entries will be ordered so that the entries will be:
    #[Top left , Top right , Bottom right , Bottom Left ]
    #The origin is in the top left corner , hence the top left corner will have the
    # smallest sum , the bottom right the largest sum , the top right the smallest difference
    # from the horizontal axis and the bottom left the largest difference from the same .
    Rect = np.zeros ((4 , 2) , dtype = "float32")
    s = pts.sum( axis = 1)
    Rect [0] = pts [np.argmin (s)]
    Rect [2] = pts [np.argmax (s)]
    diff = np.diff ( pts , axis = 1)
    Rect [1] = pts [np.argmin (diff)]
    Rect [3] = pts [np.argmax (diff)]
    # Return the coordinates .
    return Rect

def fourPointsTransform ( image , pts, returnMode = 'image', showWarpedImage = False) :

    Rect = orderPoints( pts )
    ( Topleft , TopRight , BottomRight , BottomLeft ) = Rect

    # Calculate the width of the image .
    # Maximum distance between top - right and top - left or bottom - left and bottom - right y- coordinates .
    widthA = np.sqrt ((( BottomRight [0] - BottomLeft [0]) ** 2) + ((BottomRight [1] - BottomLeft [1]) ** 2) )
    widthB = np.sqrt ((( TopRight [0] - Topleft [0]) ** 2) + (( TopRight[1] - Topleft [1]) ** 2) )
    maxWidth = max(int( widthA ) , int( widthB ) )

    # Calculate the height of the image .
    # Maximum distance between top - right and bottom - right or top - left and bottom - left y- coordinates .
    heightA = np.sqrt ((( TopRight [0] - BottomRight [0]) ** 2) + ((
    TopRight [1] - BottomRight [1]) ** 2) )
    heightB = np.sqrt ((( Topleft [0] - BottomLeft [0]) ** 2) + (( Topleft[1] - BottomLeft [1]) ** 2) )
    maxHeight = max(int( heightA ) , int( heightB ) )
    maxHeight=max(maxHeight,maxWidth)
    maxWidth=maxHeight
    # Create an array with the desired image structure .
    dst = np.array ([[0 , 0] ,[ maxWidth - 1 , 0] ,[ maxWidth - 1 , maxHeight - 1] ,[0 , maxHeight - 1]] , dtype = "float32")

    # Using cv2. getPerspectiveTransform we get the correct perspective transform .
    # Input is the location of the corners on the original image , and their destination .
    M = cv2.getPerspectiveTransform ( Rect , dst )
    
    Warped = cv2.warpPerspective ( image , M , ( maxWidth , maxHeight ) )
    if showWarpedImage:
        cv2.imshow("Warped Image",Warped)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    if returnMode == 'image':
        return Warped
    
    elif returnMode == 'store':
        cv2.imwrite('Warped.png',Warped)

def captureAiSequence():
    img = captureImage(showImage= True)
    ret1 , pts1 = findPoints(img, inputMode= 'image', showPoints= False)
    if ret1:
        print("ret1 successful")
        img = fourPointsTransform(img, pts1, returnMode = 'image', showWarpedImage= True)
        sequence = np.array(splitBoard(img, 'image', 'cells', False))
        return  sequence
    else :
        return 0

if __name__ == '__main__':
    img = cv2.imread("chpic.jpg")
    ret , pts = findPoints(img, inputMode= 'image', showPoints= True)
    #img = cv2.imread("chpic.jpg")
    if ret:
        img = fourPointsTransform(img, pts, returnMode = 'image', showWarpedImage= True)
        splitBoard(img, 'image', 'store', True, name='test')
    captureImage()