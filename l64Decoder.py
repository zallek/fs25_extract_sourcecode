# 1.0.0.0:
# - support for fs25
#
# 1.0.0.1
# - added option to save in a format supported by luau decompiler


import os
import argparse

os.system('color 0E')

print("===========================")
print("L64 Decoder 1.0.0.1")
print("===========================")

# Set up command line argument parsing
parser = argparse.ArgumentParser(description='Decode .l64 files in a specified directory')
parser.add_argument('folder_path', help='Path to the folder containing .l64 files')
args = parser.parse_args()

# Use the provided folder path instead of a fixed base directory
baseDirectory = os.path.abspath(args.folder_path)

if not os.path.exists(baseDirectory):
	os.makedirs(baseDirectory, exist_ok=True)

ge10_key2 = [0x14, 0x0B, 0x09, 0x02, 0x08, 0x03, 0x03, 0x03]
ge10_key3 = [0x05, 0x0f, 0x0b, 0x01, 0x08, 0x02, 0x03, 0x03, 0x08, 0x04, 0x03, 0x01, 0x04, 0x07, 0x08, 0x14]

count = 0
errorCount = 0
validFormat = False

def scanFile(path):
	file = open(path, "r+b")
	array = bytearray(file.read())
	shortPath = os.path.relpath(path, baseDirectory)

	global count
	global errorCount

	if array[1] == 0xEF and (array[0] == 0x02 or array[0] == 0x03):
		if array[0] == 0x02:
			for i in range(2, len(array)):
				x = i - 0x01
				array[i] = (array[i] + x + ge10_key2[x & 0x07]) & 0xFF
		else:
			for i in range(2, len(array)):
				array[i] = (array[i] + i + ge10_key3[(i - 0x01) & 0x0F]) & 0xFF

		array[0] = 0x01
		array[1] = 0x03

		if validFormat:
			array = array[1:]

		file.seek(0)
		file.write(array)
		file.close()

		count +=1

		filename, extension = os.path.splitext(path)
		os.rename(path, filename + ".lua")

		print('.l64: "{0}" decoded!'.format(shortPath))
	else:
		errorCount +=1
		print('Unknown .l64 format: "{0}"'.format(shortPath))

def scanDir(src, subpath):
	srcDir = os.path.join(src, subpath)

	with os.scandir(srcDir) as it:
		for path in it:
			if path.name.endswith('.l64'):
				scanFile(os.path.join(srcDir, path.name))
			elif path.is_dir():
				scanDir(src, os.path.join(subpath, path.name))

while True:
	choice = input("Save in a format supported by luau decompiler? (y/n): ").strip().lower()
	validFormat = choice == 'y'
	break

scanDir(baseDirectory, '')

if count > 0:
	print('Successfully decoded {0} files.'.format(count))

if errorCount > 0:
	print('Failed to decode {0} files.'.format(errorCount))

if count == 0 and errorCount == 0:
	print('No files found!')

os.system('pause')