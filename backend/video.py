import numpy as np
import cv2
import sys
from multiprocessing import Process, Queue
import select
import signal
import pygame 


class AlarmException(Exception):
    pass

def alarmHandler(signum, frame):
    raise AlarmException

from multiprocessing.pool import ThreadPool
from collections import deque
import time

def process_frame(frame):
	try:
		# # some intensive computation...
		# frame = cv2.medianBlur(frame, 19)
		# frame = cv2.medianBlur(frame, 19)
		# frame = cv2.imread('face.jpg')
	   # Added
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		#cv2.imshow('frame',gray)

		#faces = face_cascade.detectMultiScale(gray, 1.3, 5)
		faces = face_cascade.detectMultiScale(gray, 1.3, 5)
		for (x,y,w,h) in faces:
			cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),1)
			
			roi_gray = gray[y:y+h, x:x+w]
			roi_color = frame[y:y+h, x:x+w]
			eyes = eye_cascade.detectMultiScale(roi_gray,1.3,15)
			hat = cv2.resize(hat_raw, (w/4,h/4))
			y_offset = y - h/4
			x_offset = x + w/3

			for c in range(0,3):
				# print "Y:" + str(y_offset)
				# print "X:" + str(x_offset)
				# print len(frame)
				# print(y_offset+hat.shape[0])
				# print(x_offset+hat.shape[1])
				# print("HAT:" + str(len(hat)))
				# print hat[:,:,3]
				# print frame[y_offset:y_offset+hat.shape[0], x_offset:x_offset+hat.shape[1], c]
				frame[y_offset:y_offset+hat.shape[0], x_offset:x_offset+hat.shape[1], c] = hat[:,:,c] * (hat[:,:,3]/255.0) +  frame[y_offset:y_offset+hat.shape[0], x_offset:x_offset+hat.shape[1], c] * (1.0 - hat[:,:,3]/255.0)                

			for (ex,ey,ew,eh) in eyes:
				# eye_position = frame[ex:ex+ew,ey:ey+eh]
				eye = cv2.resize(eye_raw, (ew, eh))
				# eye_array = eye[0:ew,0:eh]
				y_offset = y + ey
				x_offset = x + ex;
				for c in range(0,3):
					frame[y_offset:y_offset+eye.shape[0], x_offset:x_offset+eye.shape[1], c] = eye[:,:,c] * (eye[:,:,3]/255.0) +  frame[y_offset:y_offset+eye.shape[0], x_offset:x_offset+eye.shape[1], c] * (1.0 - eye[:,:,3]/255.0)                 

			mouths = mouth_cascade.detectMultiScale(roi_gray,1.3,110)
			if len(mouths) > 0:
				for i in range(len(mouths)):
					print i
					(mx,my,mw,mh) = mouths[i]
					for (ex, ey, ew, eh) in eyes:
						if (ex <= mx+mw) and (ex+ew >= mx) and (ey <= my+mh) and (ey+eh >= my):
							np.delete(mouths, i)

			for (ex,ey,ew,eh) in mouths:
				ew_l = int(ew * 2.5)
				eh_l = int(eh * 2.5)
				mouth = cv2.resize(mouth_raw, (ew_l, eh_l))
				y_offset = y + int(ey / 1.1)
				x_offset = x + ex / 2
				for c in range(0,3):
					frame[y_offset:y_offset+mouth.shape[0], x_offset:x_offset+mouth.shape[1], c] = mouth[:,:,c] * (mouth[:,:,3]/255.0) +  frame[y_offset:y_offset+mouth.shape[0], x_offset:x_offset+mouth.shape[1], c] * (1.0 - mouth[:,:,3]/255.0)                 
	except ValueError:
		pass
	return frame

face_cascade = cv2.CascadeClassifier('haar/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haar/haarcascade_eye.xml')
mouth_cascade = cv2.CascadeClassifier('haar/haarcascade_mcs_mouth.xml')


eye_raw = cv2.imread('eye.png', -1)
mouth_raw = cv2.imread('beard1.png', -1)
hat_raw = cv2.imread('hat.png', -1)

cap = cv2.VideoCapture(0)

# threaded_mode = True
# threadn = cv2.getNumberOfCPUs()
# pool = ThreadPool(processes = threadn)
# pending = deque()


# while True:
#     while len(pending) > 0 and pending[0].ready():
#         res = pending.popleft().get()
#         cv2.imshow('threaded video', res)
#     if len(pending) < threadn:
#         ret, frame = cap.read()
#         if threaded_mode:
#             task = pool.apply_async(process_frame, (frame.copy(), "blah"))
#         else:
#             task = DummyTask(process_frame(frame))
#         pending.append(task)
#     ch = 0xFF & cv2.waitKey(1)
#     if ch == ord(' '):
#         threaded_mode = not threaded_mode
#     if ch == 27:
#         break
def switch_hats():
	print "WE GOT THE HATTTS"


def nonBlockingRawInput(prompt='', timeout=1):
    signal.signal(signal.SIGALRM, alarmHandler)
    signal.alarm(timeout)
    try:
        text = raw_input(prompt)
        signal.alarm(0)
        print 'got itttt'
    except AlarmException:
        print '\nPrompt timeout. Continuing...'
    signal.signal(signal.SIGALRM, signal.SIG_IGN)
    return ''


# while True:
# 	while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
# 	  line = sys.stdin.readline()
# 	  if line:
# 	  	if(line.contains('a')):
# 	  		switch_hats()
# 	  else: # an empty line means stdin has been closed
# 	    print('eof')
# 	    exit(0)
# 	else:

while True:
		key = pygame.key.get_pressed()
		if key[pygame.K_r]:
			print "YOLO KING KEV"
		junk, frame = cap.read()
		result = process_frame(frame.copy())
		cv2.imshow('threaded video', result)
		#cv2.waitKey(5)
		nonBlockingRawInput()


class DummyTask:
	def __init__(self, data):
		self.data = data
	def ready(self):
		return True
	def get(self):
		return self.data


