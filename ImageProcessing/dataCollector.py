from ImageHelpers import *
# from gpiozero import Button 
# captureSwitch = Button(2)

if __name__ == '__main__':
    i = int(input('enter the base counter: '))
    while (True):
        #925 7923 4989
        #iz2tA0
        # if capturSwitch.is_pressed:
        # key = cv2.waitKey(0) # waits for a key to be pressed
        key = input('do you wnat to catpure (y or n): ')
        if key == 'y':
            #playVideo()
            img = captureImage(showImage= False)
            #img = cv2.imread('fname64.png')
            print ('shape: ',img.shape)
            # img = cv2.imread("BoardTest2.png")
            cv2.imwrite('./rawData/'+str(i)+'.png',img)
            ret1 , pts1 = findPoints(img, inputMode= 'image', showPoints= False)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            if ret1:
                print("ret1 successful")
                #print ('shape: ',img.shape)
                img = fourPointsTransform(img, pts1, returnMode = 'image', showWarpedImage= False)
                print ('shape: ',img.shape)
                splitBoard(img, 'image', 'store', False, name='' + str(i) + '-')
                i += 1
            else:
                print("board identification Failed")
                cv2.waitKey(0)
                cv2.destroyAllWindows()
        elif key == 'n':
            print('Data Collector Is Out...')
            break