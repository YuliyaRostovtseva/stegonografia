#!/usr/bin/python
# -*- coding: UTF-8 -*-

# КМЗИ. ЛР№3. Стеганография в изображения. Извлечение файла из изображения

from PIL import Image
import sys	

def getArgs():
	import argparse
	parser = argparse.ArgumentParser(prog = "stegout")
	parser.add_argument ('container', help = "image container")
	parser.add_argument ('resfile', type = argparse.FileType(mode='wb'), help = "extreacted file")
 	return parser.parse_args()
	
def main():	
	args = getArgs()
	
	# пытаемся открыть изображение-контейнер
	inimg = 0
	try:
		inimg = Image.open(args.container)
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
	args.resfile.write(''.join( [chr(x) for x in byteList] ))
	args.resfile.close()
	
if __name__ == "__main__":
	main()