import re
import sys

def error(msg):
	print(msg)
	sys.exit(1)

def getBoard(filepath):
	try:
		file = open(filepath, 'r')
	except OSError:
		error("No such file : " + filepath)
	with file:
		board = []
		array = [line for line in re.sub(r'#.*', '', file.read()).split('\n') if line != '']
		size = re.search(r'\d+', array[0]).group()
		if not size.isnumeric():
			error('invalid file format : size is requiered');
		array[0] = re.sub(r''+size, '', array[0], count=1)
		size = int(size)
		array = [line for line in array if line != '']
		if len(array) == size:
			for i in range(0, size):
				line_arr = []
				array[i] = array[i].replace('\n', '');
				line = array[i].split(' ')
				for j in range(0, len(line)):
					if line[j] and line[j].isnumeric():
						line_arr.append(int(line[j]))
				if len(line_arr) > 0:
					board.append(line_arr)
		elif len(array) == size*size:
			line = []
			for i in range(0, size*size):
				array[i] = re.sub(' ', '', array[i])
				if array[i].isnumeric():
					line.append(int(array[i]))
					if len(line) == size:
						board.append(line)
						line = []
		else:
			error("invalid file format : wrong size " + filepath)
		met = []
		if size < 3 or size != len(board):
			error("invalid file format : wrong size " + filepath)
		for i in range(0, len(board)):
			if len(board[i]) != size:
				error("invalid file format : wrong line size " + filepath)
			for j in range(0, len(board[i])):
				if board[i][j] < 0 or board[i][j] > size*size:
					error("invalid value : "+ board[i][j])
				if board[i][j] in met:
					error("invalid value not unique")
				met.append(board[i][j])
		return (board)