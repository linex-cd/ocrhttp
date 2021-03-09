# OCR HTTP Service

## Deploy

install
 
./intall.sh [port]

uninstall

./remove.sh [port]

'''
	path('file2jpg', api.file2jpg),
	path('jpg2ocr', api.jpg2ocr),
	path('rtocr', api.rtocr),
	path('rtpdf', api.rtpdf),
'''
## PAGES

#### GET /

##### route to index

#### GET /index

##### page for text ocr

#### GET /table

##### page for table ocr

## API

#### POST /imgfile2ocr

##### upload image file to ocr

- post headers

		Content-Type: multipart/form-data;

- post body

		img: (binary)
		table: yes | no


#### POST /base64img2ocr

##### post image base64 string to ocr

- post headers

		Content-Type: application/json;


- post body

		{'img': 'data:image/[jpg|png|bmp];base64,' +(base64 string)}


#### POST /base64imgs2ocr

##### post images base64 string to ocr

- post headers

		Content-Type: application/json;


- post body

		{'imgs': ['data:image/[jpg|png|bmp];base64,' +(base64 string)]}



#### POST /pdf2text

##### api for pdf to extract text

- post headers

		Content-Type: multipart/form-data;

- post body

		file: (binary)


#### POST /pdf2ocr

##### api for pdf to ocr

- post headers

		Content-Type: multipart/form-data;

- post body

		file: (binary)


#### POST /pdf2base64img

##### api for converting ONE page of pdf to jpg image [base64]

- post headers

		Content-Type: multipart/form-data;

- post body

		file: (binary)
		page: (number)


#### POST /pdf2base64imgarray

##### api for converting ALL pages of pdf to jpg image [base64]

- post headers

		Content-Type: multipart/form-data;

- post body

		file: (binary)

















