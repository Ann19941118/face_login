import cv2
import  numpy as np

img=cv2.imread('C:\\Users\\Schwarz\\Desktop\\zili\\Ann.jpg')  #原始图片
#缩放
rows,cols,channels = img.shape
img=cv2.resize(img, None, fx=0.5, fy=0.5)
rows,cols,channels = img.shape
#cv2.imshow('img',img)

#转换hsv
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#lower_blue = np.array([78,43,46])
lower_blue = np.array([60,43,46])
upper_blue = np.array([100,255,255])
mask = cv2.inRange(hsv, lower_blue, upper_blue)
#cv2.imshow('Mask', mask)

#腐蚀膨胀
erode = cv2.erode(mask, None, iterations=1)
#cv2.imshow('erode',erode)
dilate = cv2.dilate(erode, None, iterations=1)
#cv2.imshow('dilate',dilate)

#遍历替换
for i in range(rows):
    for j in range(cols):
        if dilate[i,j]==255:
            img[i,j]=(255,255,255)#此处替换颜色，为BGR通道

cv2.imwrite('C:\\Users\\Schwarz\\Desktop\\zili\\new4.jpg',img) #生成的新图片

cv2.waitKey(0)
cv2.destroyAllWindows()