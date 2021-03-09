
from django.urls import path
from django.conf.urls.static import static

from . import api

urlpatterns = [
	path('', api.index),
	path('index', api.index),
	path('table', api.table),
	
	path('imgfile2ocr', api.imgfile2ocr), #ocr
	path('base64img2ocr', api.base64img2ocr), #jpg2ocr #rtocr
	path('base64imgs2ocr', api.base64imgs2ocr), #jpg2ocr #rtocr
	path('pdf2text', api.pdf2text),
	path('pdf2ocr', api.pdf2ocr),
	path('pdf2base64img', api.pdf2base64img), #pdf2jpg
	path('pdf2base64imgarray', api.pdf2base64imgarray),#file2jpg
	
	#old
	path('ocr', api.imgfile2ocr),
	path('jpg2ocr', api.base64img2ocr),
	path('rtocr', api.base64img2ocr),
	path('pdf2jpg', api.pdf2base64img),
	path('file2jpg', api.pdf2base64imgarray),
	
]+ static("/", document_root="./app/www/")