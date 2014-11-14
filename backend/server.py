from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
# from cgi import parse_header, parse_multipart
import cgi
import requests
import numpy as np
import cv2
import json


PORT_NUMBER = 8000
global count

count = 0
face_cascade = cv2.CascadeClassifier('haar/haarcascade_frontalface_default.xml')
#face_cascade = cv2.CascadeClassifier('poo')
eye_cascade = cv2.CascadeClassifier('haar/haarcascade_eye.xml')


def googlify(filez):

	img = cv2.imread(filez)
	eye_raw = cv2.imread('eye.png', -1)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	faces = face_cascade.detectMultiScale(gray, 1.3, 3)
	print len(faces)
	for (x,y,w,h) in faces:
		# cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),1)
		print "FOUND FACES" + str(len(faces))
		roi_gray = gray[y:y+h, x:x+w]
		roi_color = img[y:y+h, x:x+w]
		eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 1)
		for (ex,ey,ew,eh) in eyes:
			# eye_position = img[ex:ex+ew,ey:ey+eh]
			eye = cv2.resize(eye_raw, (ew, eh))
			# eye_array = eye[0:ew,0:eh]
			# print "y:" + str(eye.shape[0])
			# print "x:" + str(eye.shape[1])
			y_offset = y + ey
			x_offset = x + ex
			# cv2.addWeighted(eye_position,0,eye_array,1,1,dst)
			for c in range(0,3):
				img[y_offset:y_offset+eye.shape[0], x_offset:x_offset+eye.shape[1], c] = eye[:,:,c] * (eye[:,:,3]/255.0) +  img[y_offset:y_offset+eye.shape[0], x_offset:x_offset+eye.shape[1], c] * (1.0 - eye[:,:,3]/255.0)                 

	print "THE TOTAL NAME"  + str (filez)
	filename = filez + "-new" + ".jpg"
	cv2.imwrite(filename, img)

	return filename



class myHandler(BaseHTTPRequestHandler):


	def do_GET(self):
		sep = "/"
		f = open(self.path[1:])
		print "THE RETURNED FILE PATH: " + self.path[1:]
		self.wfile.write(f.read())
		return


	#Handler for the GET requests
	def do_POST(self):
		global count

		self.send_response(200)
		self.end_headers()
		url = self.rfile.read(int(self.headers.getheader('Content-Length')))
		print "json str is", url

		response = requests.get(url)
		with open("pictures/" + str(count), 'wb') as fd:
			for chunk in response.iter_content(1024):
				fd.write(chunk)

		fd.close()
		
		filename = googlify("pictures/" + str(count))

		count = count + 1

		self.wfile.write("localhost:8000/" + filename)
		self.wfile.close()

#googlify('/Users/facebook/Downloads/perfect.jpg')

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
