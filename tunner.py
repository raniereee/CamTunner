import numpy as np
import cv2
import sys
import pytesseract
from PIL import Image
import time, getopt
from pytesser import *

class Tunner():

	def __init__(self, argv):

		try:
			opts, args = getopt.getopt(argv,"hu:o:t:",["url=","out=","trn="])
		except getopt.GetoptError:
			print 'tunner.py -u <url cam> -o <output dir> -t <trained data>'
			sys.exit(2)
		for opt, arg in opts:
			if opt == '-h':
				print 'tunner.py -u <url cam> -o <output dir> -t <trained data>'
				sys.exit()
			elif opt in ("-u", "--url"):
				self.url = arg
			elif opt in ("-o", "--out"):
				self.outdir = arg
			elif opt in ("-t", "--trn"):
				self.trainedata = arg


		try:
			self.train_cascade = cv2.CascadeClassifier(self.trainedata)
		except:
			print "Fail to load xml file"
			sys.exit(2)

		self.capture = cv2.VideoCapture(self.url)

		ret, img = self.capture.read()

		self.element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
		self.kernel = np.ones((2,2),np.uint8)

		height, width, channels = img.shape

		self.left_margin  =  (width/6)*1
		self.right_margin =  (width/6)*5

		cv2.namedWindow('Original Image')
		cv2.createTrackbar('Binary CTRL: ','Original Image',0,255, self.nothing)
		cv2.imshow("Original Image", img)

		self.font = cv2.FONT_HERSHEY_SIMPLEX


	def loop(self):

		placa = ""
		self.capture.release()
		capture = cv2.VideoCapture(self.url)
		ret, img = capture.read()
		height, width, channels = img.shape

		contador = 0
		threshold_limiar = 50
		while ret:
			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			plates = self.train_cascade.detectMultiScale(gray, 1.09, 5)

			for (x,y,w,h) in plates:

			    roi = img[y:y+h, x:x+w]

			    #if (x > linha_inferior)  and (x < linha_superior) and (w > 158) and (h > 43) and (w < 214 ) and (h < 80):
			    if (x > self.left_margin)  and (x < self.right_margin) and (w > 140) and (h > 40) and (w < 214 ) and (h < 80):
				cv2.putText(img, "Calibrated!",     (10,500), self.font, 1, (0,0,255), 3)
				cv2.putText(img, "PLATE: " + placa, (10,600), self.font, 1, (0,0,255), 3)

			    cv2.imshow("ROI", roi)

			    roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

			    cv2.imwrite(self.outdir + "/%010d" % contador + "gray.jpg" , roi_gray)

			    xxx,thresh = cv2.threshold(roi_gray, threshold_limiar ,255,1)

			    temp = cv2.erode(thresh,self.element)

			    dilated = cv2.dilate(temp, self.element)
			    cv2.imshow("roi_dilated", dilated)

			    cv2.imwrite(self.outdir + "/%010d" % contador + "_dil.jpg" , dilated)

			    image = self.get_image(self.outdir + "/%010d" % contador + "_dil.jpg")
			    placa = pytesseract.image_to_string(image , lang="lrm")
			    contador = contador + 1

			    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

			threshold_limiar = cv2.getTrackbarPos('Binary CTRL: ','Original Image')
			cv2.line(img, (self.left_margin,0), (self.left_margin, height), (255,0,0), 1)
			cv2.line(img, (self.right_margin,0), (self.right_margin, height),(255,0,0), 1)

			cv2.imshow("Original Image", img)

			ret, img = capture.read()

			k = cv2.waitKey(50) & 0xFF
			if k == 27:
				cv2.destroyAllWindows()
				break

		
	def nothing(self, x):
		pass

	def get_image(self, f):
	    return Image.open(f)

if __name__ == "__main__":
	t = Tunner(sys.argv[1:])
	t.loop()
