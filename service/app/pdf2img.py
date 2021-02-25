import base64   
import cv2   
import fitz
import os

def parse(pdf_file):
	
	
	
	doc = fitz.open(pdf_file)
	
	base64_datas = []
	for page in doc:
		
		print("rendering page %i" % page.number)
				
		tmpfile = "%s-%i.png" % (pdf_file, page.number)
		
		# 默认图片大小为：792X612, dpi=96

		pix = page.getPixmap(alpha = False)  # render page to an image
		pix.writePNG(tmpfile)

		
		f = open(tmpfile, 'rb')

		base64_data = "data:image/png;base64," + base64.b64encode(f.read()).decode()
		f.close()
		
		os.remove(tmpfile)
		
		base64_datas.append(base64_data)
	return base64_datas
	

if __name__ == '__main__':


	pdf_file ="4.pdf"

	rs = parse(pdf_file, 1)
	print(rs)
