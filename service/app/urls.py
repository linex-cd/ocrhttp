
from django.urls import path
from django.conf.urls.static import static

from . import api

urlpatterns = [
	path('', api.index),
	path('index', api.index),
	path('table', api.table),
	path('test', api.test),
	path('ocr', api.ocr),
	path('pdf2jpg', api.pdf2jpg),
	path('file2jpg', api.file2jpg),
	path('jpg2ocr', api.jpg2ocr),
	path('rtocr', api.rtocr),
	path('rtpdf', api.rtpdf),

]+ static("/", document_root="./app/www/")