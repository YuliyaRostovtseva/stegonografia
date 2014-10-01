#!/usr/bin/python
# -*- coding: UTF-8 -*-

# ����. �й3. ������������� � �����������.

from PIL import Image
import sys

def getArgs():
	import argparse
	parser = argparse.ArgumentParser(prog = "steg")
	parser.add_argument ('input_file', help = "image container ")
	parser.add_argument ('output_file',  help = "output file (BMP or hidden file)")
	parser.add_argument ('file_for_hiding', nargs='?', type = argparse.FileType(mode='rb'), help = "file for hiding")
 	return parser.parse_args()

# ������������� ������� ��� ����� num ����� bit
def setLSB(num, bit):
	if bit == 0:
		num = num & 254
	else:
		num = num | 1
	return num
	
def hiding(container, outBMP, inffile):
	# �������� ������� �����������-���������
	contImg = 0
	try:
		contImg = Image.open(container)
	except Exception as err:
		print "Can't open container file"
		print("Error {0}".format(err))
		sys.exit(1)
	
	# �������� �����, � ������� ���� ������� ����� ����������
	# �������� ����������
	raw = list(contImg.tobytes())
		
	# ��������� ���������� ��������������� �����
	inf = inffile.read()
	inffile.close()
	
	if len(inf) * 8 + 20 > len(raw): # ���� ���������� ���, ������� ���������� ��������, ������, ��� ����� ����, � ������� ����� �������
		print "Information file is too big"
		sys.exit(-1)
	
	# ������� ������ ��������������� �����
	infSize = len(inf)
	for i in range(20): # ������ ��� ������ 20 ���
		raw[i] = chr(setLSB(ord(raw[i]), infSize % 2))
		infSize /= 2
		
	# ������ ������� ��� ����
	for i in range (len(inf)):
		byte = ord(inf[i]) # ����, ������� ����� �������
		for j in range (8):
			raw[20 + i * 8 + j] = chr(setLSB(ord(raw[20 + i * 8 + j]), byte % 2))
			byte /= 2
	
	# ������� ��������� � ����� �����������
	# ��������� ����������� � .bmp, �.�. ����� ����� ������
	# � ���������� ����� ����������
	outimg = Image.frombytes(contImg.mode, contImg.size, ''.join(raw)) # ������� ����� ����������� �� ������ ��������� ����
	outimg.save(outBMP, "BMP")
	contImg.close()
	
def extracting(container, resfname):
	# �������� ������� �����������-���������
	inimg = 0
	try:
		inimg = Image.open(container)
	except Exception as err:
		print "Can't open container file"
		print("Error {0}".format(err))
		sys.exit(1)
	
	# �������� �����, � ������� ����� ������� ������� ����
	raw = list(inimg.tobytes())
		
	# �������� ������ 20 ��� - ���������� ����, ���������� � ��������� �����
	size = 0
	for i in range(20):
		size += ( ord(raw[i]) % 2) * 2 ** i
		
	byteList = [] # ����� ����������� �����
	# ������ �������� size * 8 ���
	for j in range (size):
		byte = 0
		for i in range (8):
			byte += (ord(raw[20 + j * 8 + i]) % 2) * 2 ** i
		
		# � byte - ��������� ���� �����
		# ������� ��� � ������
		byteList.append(byte)
	
	# ������� ������������ ������ � ����
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