from django.http import HttpResponse, HttpResponseRedirect
import time
import os


from ocr import Ocr
from pdf import Pdf

import json
import base64

import cv2
import numpy as np

from app import mergelines
from app import pdf2img

ocr_engine = Ocr()
pdf_engine = Pdf()

def test(request):
	return HttpResponse("the service is online.")
	
def index(request):
	return HttpResponseRedirect("/index.html")

def table(request):
	return HttpResponseRedirect("/table.html")


def ocr(request):
	in_memory_file = request.FILES['img'].read()
	#in_memory_file = io.BytesIO()

	nparr = np.fromstring(in_memory_file, np.uint8)
	img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

	print('Image size: {}x{}'.format(img.shape[1], img.shape[0]))
	
	table = request.POST.get('table','no') 
	istable = False 
	if table == 'yes':
		istable =  True

	
	start_time = time.time()
	ocr_result, rois, hocr = ocr_engine.run_ocr(img, istable)

	print("CRNN time: %.03fs" % (time.time() - start_time))
	
	
	data = {"results": []}
	for i in range(len(rois)):
		data["results"].append({
			'position': rois[i],
			'text': ocr_result[i],
			'hocr': hocr[i]
		})
		
	pages = []
	page = {'content':[ocr_result], 'hocr': [hocr], 'bbox': [rois]}
	
	pages.append(page)
	dl = mergelines.Hocr_DL(pages)
	content = dl.get_content()
	
	data['dl'] = content

	return HttpResponse(json.dumps(data), content_type='application/json')



	
def rtocr(request):
	
	data = {'code':403, 'msg':'No image data passthrough'}
	
	#if 'img' in request.POST and request.POST['img']:
	#	img_base64 = request.POST['img']
	if request.method == 'POST':
		jsondata = json.loads(request.body.decode())
		img_base64 = jsondata['img'];
		
		imgdata = base64.b64decode(img_base64)

		'''
		file=open('1.png','wb')
		file.write(imgdata)
		file.close()
		'''
		
		nparr = np.fromstring(imgdata, np.uint8)
		img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
		
		#cv2.imshow("ori", img)
		#cv2.waitKey(0)
		print('Image size: {}x{}'.format(img.shape[1], img.shape[0]))
		
		#create frame
		WHITE = [255,255,255]
		frame = cv2.copyMakeBorder(img,400,400,30,30,cv2.BORDER_CONSTANT,value=WHITE)
		#cv2.imshow("frame", frame)
		#cv2.waitKey(0)
		
		istable = False
		ocr_result, rois, hocr = ocr_engine.run_ocr(img, istable)
		
			
		data = {"results": []}
		for i in range(len(rois)):
			data["results"].append({
				'position': rois[i],
				'text': ocr_result[i],
				'hocr': hocr[i]
			})
			
		pages = []
		page = {'content':[ocr_result], 'hocr': [hocr], 'bbox': [rois]}
	
		pages.append(page)
		dl = mergelines.Hocr_DL(pages)
		content = dl.get_content()
		
		data['dl'] = content

	response = HttpResponse(json.dumps(data), content_type='application/json')
	response["Access-Control-Allow-Origin"] = "*"
	response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
	response["Access-Control-Max-Age"] = "1800"
	response["Access-Control-Allow-Headers"] = "*"
	
	return response
	
def rtpdf(request):
	
	data = {'code':403, 'msg':'No pdf data passthrough'}
	
	#if 'img' in request.POST and request.POST['img']:
	#	img_base64 = request.POST['img']
	if request.method == 'POST':
		
		pdf = request.FILES.get('file')
		if pdf != None:
			data['data'] = pdf_engine.runtime_pdf(pdf)
			data['msg'] = 'OK'
			data['code'] = '200'
		else:
			data['data'] = ''
			data['msg'] = 'OK'
			data['code'] = '200'
		

	response = HttpResponse(json.dumps(data), content_type='application/json')
	response["Access-Control-Allow-Origin"] = "*"
	response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
	response["Access-Control-Max-Age"] = "1800"
	response["Access-Control-Allow-Headers"] = "*"
	
	return response
	
	
		
def pdf2jpg(request):
	
	data = {'code':403, 'msg':'No pdf data passthrough'}
	
	#if 'img' in request.POST and request.POST['img']:
	#	img_base64 = request.POST['img']
	if request.method == 'POST':
		
		pdf = request.FILES['pdf'].name
		page = request.POST.get('page','0') 
		if pdf != None:
			data['data'] = pdf2img.parse(pdf, int(page))
			data['msg'] = 'OK'
			data['code'] = '200'
		else:
			data['data'] = ''
			data['msg'] = 'OK'
			data['code'] = '200'
		

	response = HttpResponse(json.dumps(data), content_type='application/json')
	response["Access-Control-Allow-Origin"] = "*"
	response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
	response["Access-Control-Max-Age"] = "1800"
	response["Access-Control-Allow-Headers"] = "*"
	
	return response
	
	
		
def file2jpg(request):
	
	data = {'code':403, 'msg':'No pdf data passthrough'}
	
	#if 'img' in request.POST and request.POST['img']:
	#	img_base64 = request.POST['img']
	if request.method == 'POST':
	
		
		if request.FILES != None:
		
			filename = request.FILES['file'].name
			filename = filename.lower()
			filechucks = request.FILES['file'].chunks()
			
			destination = open(filename, 'wb')
			for chunk in filechucks:
				destination.write(chunk)
			destination.close()
			
			if filename[-4:] == '.pdf':
				data['data'] = pdf2img.parse(filename)
				data['msg'] = 'OK'
				data['code'] = '200'
			elif filename[-4:] == '.jpg' or filename[-4:] == '.png' or filename[-4:] == '.bmp':
				f = open(filename, 'rb')
				base64_data = 'data:image/'+filename[-3:]+';base64,' + base64.b64encode(f.read()).decode()
				f.close()
				data['data'] = [base64_data]
				data['msg'] = 'OK'
				data['code'] = '200'
			else:
				data['data'] = ''
				data['msg'] = 'error format'
				data['code'] = '401'
				
			os.remove(filename)
		else:
			data['data'] = ''
			data['msg'] = 'no data'
			data['code'] = '400'
		

	response = HttpResponse(json.dumps(data), content_type='application/json')
	response["Access-Control-Allow-Origin"] = "*"
	response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
	response["Access-Control-Max-Age"] = "1800"
	response["Access-Control-Allow-Headers"] = "*"
	
	return response
	

def jpg2ocr(request):

	if request.method == 'POST':
	
		data = {}
		data['msg'] = 'success'
		data['code'] = '200'
		#标记通道繁忙
		state = os.path.exists('state.txt')
		if state == False:
			f = open('state.txt', "w")
			f.write('busy')
			f.close()
			
		else:
			
			print('worker busy...')
			
			data['msg'] = 'current workers are busy, please retry 10 seconds later'
			data['code'] = '501'
			response = HttpResponse(json.dumps(data), content_type='application/json')
			
			response["Access-Control-Allow-Origin"] = "*"
			response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
			response["Access-Control-Max-Age"] = "1800"
			response["Access-Control-Allow-Headers"] = "*"
			
			return response
		#endif
		
		
		base64_str = request.POST.get('img','').replace("data:image/png;base64," , '')
		
		imgString = base64.b64decode(base64_str)
		nparr = np.fromstring(imgString,np.uint8)  
		img = cv2.imdecode(nparr,cv2.IMREAD_COLOR)
		

   
		print('Image size: {}x{}'.format(img.shape[1], img.shape[0]))
		
		table = request.POST.get('table','no') 
		istable = False 
		if table == 'yes':
			istable =  True

		
		start_time = time.time()
		ocr_result, rois, hocr = ocr_engine.run_ocr(img, istable)

		print("CRNN time: %.03fs" % (time.time() - start_time))
		
		
		data['results'] = []
		for i in range(len(rois)):
			data["results"].append({
				'position': rois[i],
				'text': ocr_result[i],
				'hocr': hocr[i]
			})
			
		pages = []
		page = {'content':[ocr_result], 'hocr': [hocr], 'bbox': [rois]}
		
		pages.append(page)
		dl = mergelines.Hocr_DL(pages)
		content = dl.get_content()
		
		data['dl'] = content
		
		
		#删除标记
		os.remove('state.txt')
	
	response = HttpResponse(json.dumps(data), content_type='application/json')
	response["Access-Control-Allow-Origin"] = "*"
	response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
	response["Access-Control-Max-Age"] = "1800"
	response["Access-Control-Allow-Headers"] = "*"
	
	return response

	
	
	