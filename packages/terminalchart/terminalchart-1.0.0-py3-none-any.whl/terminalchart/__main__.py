import argparse

# x = [1,2,3,5,6,7,8 ,9,10,11,12,13,14,15,16,17,18,20,21,23,25,27,28,29,30,31,32,33,34,35]
# y = [1,5,4,9,2,1,11,5, 2,22,12,12,12,12,15,24,20,23,22,25, 5,14, 4, 5,15, 8,22,28,1,2,15]
character = ''

def formatter(x,y,character):
	'''
	takes arrays of x and y coordinates and maps them with the character to create a string of chart
	'''
	print_array = dict()
	maxy = max(y)
	out = ''
	out = out+str(x)+'\n'
	out = out+str(y)+'\n'
	for i in list(range(1, max(x)+1)):
		print_array[i] = dict()
		if i not in x:
			print_array[i] = [' ']*(maxy+1)
		else:
			print_array[i] = [character]*y[x.index(i)] + [' ']*(maxy+1 - y[x.index(i)])

	for i in list(range(len(print_array[1])-1, -1, -1)):
		line = '{0: >2}|'.format(i+1)
		for j in list(range(1, max(x)+1)): 
			line = line + '{0: >{width}}'.format(print_array[j][i], width=len(character)) 
		out=out+line+'\n'

	line = '   '

	for i in list(range(1,len(print_array)+1)):
		line = line + '{0: ^{width}}'.format(i, width=len(character))
	xaxis= '   '+'-'*len(print_array)*len(character)
	out = out+xaxis+'\n'
	out = out+line+'\n'
	return out


def terminalchart(raw_args=None):
	'''
	main func
	'''
	parser = argparse.ArgumentParser(description='It will take x and y values as an input and output a chart on the commandline or to a file.')
	parser.add_argument("-t", "--terminal", nargs=2, required=False, help="append x and y values with the command if values are short. \
																	Like -t '1,2,3' '3,2,3' or like -t '1 2 3' '3 2 3'")
	parser.add_argument("-f", "--file",     nargs=1, required=False, help="add values in a file. like x: 1 2 3, y:3 2 3 or like\
																	 x: 1,2,3, y:3,2,3 and pass the input like:\
																	  -f input_file, recommended for large set of values")
	parser.add_argument("-c", "--character", required=False, help="pass the character you want to be displayed on chart, will \
																	default to %%& if none given")
	parser.add_argument("-o", "--output", required=True, help="where you want your output to be, -o t for terminal, -o output_file for file")

	args = parser.parse_args(raw_args)

	if args.character:
		character = '{0: ^{width}}'.format(vars(args)["character"], width=len(vars(args)["character"])+2) 
	else:
		character = '{0: ^{width}}'.format('%&', width=4)

	if args.file:
		file = open(vars(args)["file"][0])
		x , y = file.read().rstrip().replace(' \n', ',').replace('\n', ',').split(',')
		x = [int(item) for item in x.split('x:')[1].replace('\'','').replace(' ', ',').replace(',,', ',').split(',')]
		y = [int(item) for item in y.split('y:')[1].replace('\'','').replace(' ', ',').replace(',,', ',').split(',')]
		if args.output == 't':
			print (formatter(x,y,character))
		else:
			file = open(vars(args)["output"], 'w+')
			file.write(formatter(x,y,character))
			file.close()

	elif args.terminal:
		x = [int(item) for item in args.terminal[0].replace(' ', ',').replace(',,', ',').split(',')]
		y = [int(item) for item in args.terminal[1].replace(' ', ',').replace(',,', ',').split(',')]
		if args.output == 't':
			print (formatter(x,y,character))
		else:
			file = open(vars(args)["output"], 'w+')
			file.write(formatter(x,y,character))
			file.close()
	else:
		print ('Don\'t pass wrong information, read the help carefully')

if __name__ == '__main__':
	terminalchart()