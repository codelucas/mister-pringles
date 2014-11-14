import numpy as np
import cv2
try:

	face_cascade = cv2.CascadeClassifier('/Users/facebook/mister-pringles/haarcascade_frontalface_default.xml')
	#face_cascade = cv2.CascadeClassifier('poo')
	eye_cascade = cv2.CascadeClassifier('/Users/facebook/mister-pringles/haarcascade_eye.xml')

	print face_cascade
	print "\n\n\n\n"
	print eye_cascade
	img = cv2.imread('face.jpg')
	eye_raw = cv2.imread('eye.png', -1)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	#cv2.imshow('img',gray)

	#faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	faces = face_cascade.detectMultiScale(gray, 1.3, 2)
	print len(faces)
	for (x,y,w,h) in faces:
		cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
		
		roi_gray = gray[y:y+h, x:x+w]
		roi_color = img[y:y+h, x:x+w]
		eyes = eye_cascade.detectMultiScale(roi_gray)
		for (ex,ey,ew,eh) in eyes:
			print ew
			print eh
			print ex
			print ey
			# eye_position = img[ex:ex+ew,ey:ey+eh]
			eye = cv2.resize(eye_raw, (ew, eh))
			# eye_array = eye[0:ew,0:eh]
			print "y:" + str(eye.shape[0])
			print "x:" + str(eye.shape[1])
			y_offset = y + ey
			x_offset = x + ex;
			# cv2.addWeighted(eye_position,0,eye_array,1,1,dst)
			for c in range(0,3):
				img[y_offset:y_offset+eye.shape[0], x_offset:x_offset+eye.shape[1], c] = eye[:,:,c] * (eye[:,:,3]/255.0) +  img[y_offset:y_offset+eye.shape[0], x_offset:x_offset+eye.shape[1], c] * (1.0 - eye[:,:,3]/255.0)                 
			#img[y + ey:y + ey+eye.shape[0], x + ex:x + ex+eye.shape[1]] = eye
			#cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

	cv2.imshow('img',img)
	input()
	
except KeyboardInterrupt:
	pass




 
