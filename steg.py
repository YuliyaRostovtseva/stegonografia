#!/usr/bin/python
# -*- coding: UTF-8 -*-

# КМЗИ. ЛР№3. Стеганография в изображения.

from PIL import Image
import sys

def getArgs():
	import argparse
	parser = argparse.ArgumentParser(prog = "steg")
	parser.add_argument ('input_file', help = "image container ")
	parser.add_argument ('output_file',  help = "output file (BMP or hidden file)")
	parser.add_argument ('file_for_hiding', nargs='?', type = argparse.FileType(mode='rb'), help = "file for hiding")
 	return parser.parse_args()

# устанавливает младший бит числа num битом bit
def setLSB(num, bit):
	if bit == 0:
		num = num & 254
	else:
		num = num | 1
	return num
	
def hiding(container, outBMP, inffile):
	# пытаемся открыть изображение-контейнер
	contImg = 0
	try:
		contImg = Image.open(container)
	except Exception as err:
		print "Can't open container file"
		print("Error {0}".format(err))
		sys.exit(1)
	
	# получаем байты, в младшие биты которых будем записывать
	# полезную информацию
	raw = list(contImg.tobytes())
		
	# считываем содержимое информационного файла
	inf = inffile.read()
	inffile.close()
	
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
	outimg.save(outBMP, "BMP")
	contImg.close()
	
def extracting(container, resfname):
	# пытаемся открыть изображение-контейнер
	inimg = 0
	try:
		inimg = Image.open(container)
	except Exception as err:
		print "Can't open container file"
		print("Error {0}".format(err))
		sys.exit(1)
	
	# получаем байты, в младших битах которых спрятан файл
	raw = list(inimg.tobytes())
		
	# достанем первые 20 бит - количество байт, спрятанных в остальной части
	size = 0
	for i in range(20):
		size += ( ord(raw[i]) % 2) * 2 ** i
		
	byteList = [] # байты спрятанного файла
	# теперь достанем size * 8 бит
	for j in range (size):
		byte = 0
		for i in range (8):
			byte += (ord(raw[20 + j * 8 + i]) % 2) * 2 ** i
		
		# в byte - очередной байт числа
		# запишем его в список
		byteList.append(byte)
	
	# запишем получившийся список в файл
	resfile = open(resfname, 'wb')
	resfile.write(''.join( [chr(x) for x in byteList] ))
	resfile.close()

def main():	
	args = getArgs()
	if args.file_for_hiding:
		hiding(args.input_file, args.output_file, args.file_for_hiding)
	else:
		extracting(args.input_file, args.output_file)
	
if __name__ == "__main__":
	main()