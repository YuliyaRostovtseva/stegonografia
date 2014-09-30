#!/usr/bin/python
# -*- coding: UTF-8 -*-

# КМЗИ. ЛР№3. Стеганография в изображения. Сокрытие файла

from PIL import Image
import sys	

def getArgs():
	import argparse
	parser = argparse.ArgumentParser(prog = "steghide")
	parser.add_argument ('container', help = "image container")
	parser.add_argument ('outBMP',  help = "output image file (BMP)")
	parser.add_argument ('inffile', type = argparse.FileType(mode='rb'), help = "file for hiding")
 	return parser.parse_args()
	
# устанавливает младший бит числа num битом bit
def setLSB(num, bit):
	if bit == 0:
		num = num & 254
	else:
		num = num | 1
	return num

def main():	
	args = getArgs()
	
	# пытаемся открыть изображение-контейнер
	contImg = 0
	try:
		contImg = Image.open(args.container)
	except Exception as err:
		print "Can't open container file"
		print("Error {0}".format(err))
		sys.exit(1)
	
	# получаем байты, в младшие биты которых будем записывать
	# полезную информацию
	raw = list(contImg.tobytes())
		
	# считываем содердимое ифнормационного файла
	inf = args.inffile.read()
	args.inffile.close()
	
	if len(inf) * 8 + 20 > len(raw): # если количество бит, которые необходимо спрятать, больше, чем число байт, в которые можно прятать
		print "Information file is too big"
		sys.exit(-1)
	
	# спрячем размер информационного файла
	infSize = len(inf)
	for i in range(20): # отведём под размер 20 бит
		raw[i] = chr(setLSB(ord(raw[i]), infSize % 2))
		infSize /= 2
		
	# теперь спрячем сам файл
	for i in range (len(inf)):
		byte = ord(inf[i]) # байт, котоырй будем прятать
		for j in range (8):
			raw[20 + i * 8 + j] = chr(setLSB(ord(raw[20 + i * 8 + j]), byte % 2))
			byte /= 2
	
	# запишем результат в новое изображение
	# сохраняем обязательно в .bmp, т.к. иначе будет сжатие
	# и информация может потеряться
	outimg = Image.frombytes(contImg.mode, contImg.size, ''.join(raw)) # создаем новое изображение на основе изменённых байт
	outimg.save(args.outBMP, "BMP")
	contImg.close()
	
if __name__ == "__main__":
	main()