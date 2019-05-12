import numpy as np
import cv2
import pygame
import time

def InsertLogo(i, j):
	if (j+rowsLogo < rowsFrame and i+colsLogo<colsFrame):
		background[j:j+rowsLogo, i:i+colsLogo] = faceMask[imageIndex];
def InsertLogoEnd(i, j):
	if (j+rowsLogo < rowsFrame and i+colsLogo<colsFrame):
		background[j:j+rowsLogo, i:i+colsLogo] = endImage;


background = cv2.imread('background.png');
faceMask = [];
imageIndex = 0;
faceMask.append(cv2.imread('img1.png'));
faceMask.append(cv2.imread('img2.png'));
faceMask.append(cv2.imread('img3.png'));
faceMask.append(cv2.imread('img4.png'));

imageLocation = [];
imageLocation.append((3,3));
imageLocation.append((153,3));
imageLocation.append((303,3));
imageLocation.append((453,3));

ansLocation = [];
ansLocation.append((3,303));
ansLocation.append((153,303));
ansLocation.append((303,303));
ansLocation.append((453,303));

ans = [];
for i in range(4):
	ans.append(False);

end = 0;
endImage = cv2.imread('end.png');
endImage = cv2.resize(endImage, (200, 200));

for index in range(4):
	faceMask[index] = cv2.resize(faceMask[index], (50, 150));
rowsFrame, colsFrame, channelsFrame = background.shape;
targetBlue = 0;
targetGreen = 255;
targetRed = 0;

cap = cv2.VideoCapture(0);
while(True):
	# Capture frame-by-frame
	ret, frame = cap.read();
	frame=cv2.flip(frame,1);
	
	
	#顯示背景
	background = cv2.imread('background.png');
	
	#以下畫藍點
	x = 0;
	y = 0;
	imageIndex = 0;
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV);
	lower_blue = np.array([110, 50, 50], dtype=np.uint8);
	upper_blue = np.array([130,255,255], dtype=np.uint8);
	mask = cv2.inRange(hsv, lower_blue, upper_blue)
	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
	mask = cv2.erode(mask, kernel, iterations = 1)
	mask = cv2.dilate(mask, kernel, iterations = 1)
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
	if len(cnts) > 0:
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		if radius > 10:
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
			cv2.circle(background, center, 5, (0, 0, 255), -1)
	
	#以下跟藍點跑
	x = int(x);
	y = int(y);
	for i in range(4):
		imageIndex = i;
		Ix,Iy = imageLocation[i];
		rowsLogo,colsLogo,channelsLogo = faceMask[i].shape;
		if (x>Ix and x<Ix+50) and (y>Iy and y<Iy+150) and (x-25>=0 and y-75>=0):
			imageLocation[i] = (x-25,y-75);
		InsertLogo(Ix,Iy);
	
	#判斷是否在圖片正確
	for i in range(4):
		imageIndex = i;
		Ix,Iy = imageLocation[i];
		ansX,ansY = ansLocation[i];
		r1 = pygame.Rect(Ix,Iy,50,150);
		r2 = pygame.Rect(ansX,ansY,50,150);
		if (r1.colliderect(r2)):
			ans[i] = True;
		else:
			ans[i] = False;
	end = 0;
	for i in range(4):
		if ans[i] == True:
			end = end + 1;
	if end == 4:
		rowsLogo,colsLogo,channelsLogo = endImage.shape;
		InsertLogoEnd(50,50);
	
	#畫矩形
	imageIndex = 0;
	x=0;
	y=3;
	for index in range(4):
		imageIndex = index;
		x = 150*imageIndex + 3;
		rowsLogo,colsLogo,channelsLogo = faceMask[imageIndex].shape;
		startX = x;
		startY = y;
		for i in range(rowsLogo):
			startY = startY + 1;
			startX = x;
			for j in range(colsLogo):
				startX = startX + 1;
				if startX==x+1 or startX==colsLogo+x or startY==y+1 or startY==rowsLogo:
					background[startY][startX][0]=targetBlue;
					background[startY][startX][1]=targetGreen;
					background[startY][startX][2]=targetRed;
	x=0;y=3;
	for index in range(4):
		imageIndex = index;
		x = 150*imageIndex + 3;
		rowsLogo,colsLogo,channelsLogo = faceMask[imageIndex].shape;
		startX = x;
		y=3;
		vary = 300;
		y = y + vary;
		startY = y;
		for i in range(rowsLogo):
			startY = startY + 1;
			startX = x;
			for j in range(colsLogo):
				startX = startX + 1;
				if startX==x+1 or startX==colsLogo+x-1 or startY==y+1 or startY==rowsLogo+y:
					background[startY][startX][0]=0;
					background[startY][startX][1]=0;
					background[startY][startX][2]=255;
					
	
	
	
	
	cv2.imshow('frame',frame);
	cv2.imshow('img', background);
	if cv2.waitKey(1) & 0xFF == ord('q') or end == 4:
		time.sleep(5);
		break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
