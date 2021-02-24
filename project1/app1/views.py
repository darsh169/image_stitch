from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse,FileResponse
from rest_framework.parsers import JSONParser
import cv2
import numpy as np
import matplotlib.pyplot as plt
import requests
import base64
# from django.shortcuts import render

# Create your views here.

def send_img(response):
    img = open('app1/test.jpeg', 'rb')
    image = FileResponse(img)
    return image



def Stitch(request):

	#Read the images from urls
	url=request.GET['img1']
	# url = 'https://miro.medium.com/max/500/1*XAiD2UEaF-pQmkQZ1V--wg.jpeg'
	resp = requests.get(url, stream=True).raw
	image1 = np.asarray(bytearray(resp.read()), dtype="uint8")
	image1 = cv2.imdecode(image1, cv2.IMREAD_COLOR)
	img1=cv2.resize(image1,(500,300))

	url=request.GET['img2']
	# url = 'https://miro.medium.com/max/2400/1*VR6nUTu_rwlJJd3DBX22UQ.jpeg'
	resp = requests.get(url, stream=True).raw
	image2 = np.asarray(bytearray(resp.read()), dtype="uint8")
	image2 = cv2.imdecode(image2, cv2.IMREAD_COLOR)
	img2=cv2.resize(image2,(500,300))

	#Create stitched image using OpenCV Stitcher
	stitcher=cv2.Stitcher.create()
	(status,result)=stitcher.stitch([img1,img2])
	if status==cv2.STITCHER_OK:
	  # print("Successful")
	  result=cv2.resize(result,(800,400))
	  # cv2_imshow(result)
	  msg="Successful"
	else:
	  msg="Process Unsuccessful"

	#manipulate the stitched image for better representation
	#the points can be changed and automated using image parameters
	pts1 = np.float32([[10,35],[350,35],[10,800],[350,800]])
	pts2 = np.float32([[0,0],[350,0],[0,800],[350,800]])

	M = cv2.getPerspectiveTransform(pts1,pts2)
	#transform the image
	result = cv2.warpPerspective(result,M,(800,400))
	# cv2_imshow(dst)

	cv2.imwrite("app1/test.jpeg",result)

	# op=cv2.imread("app1/test.jpeg")

	return redirect('/img')
	# return JsonResponse([op],safe=False)

