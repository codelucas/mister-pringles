from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
# from cgi import parse_header, parse_multipart
import cgi
import requests
import numpy as np
import cv2


PORT_NUMBER = 8000
global count

count = 0
face_cascade = cv2.CascadeClassifier('/Users/facebook/mister-pringles/haar/haarcascade_frontalface_default.xml')
#face_cascade = cv2.CascadeClassifier('poo')
eye_cascade = cv2.CascadeClassifier('/Users/facebook/mister-pringles/haar/haarcascade_eye.xml')




def googlify(filez):

	# print face_cascade
	# print "\n\n\n\n"
	# print eye_cascade
	img = cv2.imread(filez)
	eye_raw = cv2.imread('eye.png', -1)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	#cv2.imshow('img',gray)

	#faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	print len(faces)
	for (x,y,w,h) in faces:
		cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),1)
		
		roi_gray = gray[y:y+h, x:x+w]
		roi_color = img[y:y+h, x:x+w]
		eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 2)
		for (ex,ey,ew,eh) in eyes:
			print ew
			print end_headers
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

	# result = cv2.imencode('.jpg',img)
	cv2.imwrite("pictures/new-" + filez + ".jpg", img)
	# return result
	#cv2.imshow('img',img)


class myHandler(BaseHTTPRequestHandler):

	#Handler for the GET requests
	def do_POST(self):
		global count

		self.send_response(200)
		# self.send_header('Content-type','text/html')
		self.end_headers()
		# Send the html message
		self.wfile.write("Hello World !")

		url = self.rfile.read(int(self.headers.getheader('Content-Length')))
		response = requests.get(url)
		with open("pictures/" + str(count), 'wb') as fd:
			for chunk in response.iter_content(1024):
				fd.write(chunk)

		fd.close()
		

		googlify("pictures/" + str(count))
		self.send_header('Content-type','image/jpg')
		fp = file("pictures/new-" + str(count) + ".jpg", 'rb')
		# print img
		# print type(img)

		count = count + 1

		while True:
			bytes = fp.read(8192)
			if bytes:
				self.wfile.write(bytes)
			else:
				return

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()
