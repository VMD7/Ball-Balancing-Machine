'''
*****************************************************************************************
*
*        		===============================================
*           		Nirikshak Bot (NB) Theme (eYRC 2020-21)
*        		===============================================
*
*  This script is to implement Task 1B of Nirikshak Bot (NB) Theme (eYRC 2020-21).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD project under National Mission on Education using ICT (NMEICT)
*
*****************************************************************************************
'''

# Team ID:			1425
# Author List:		Vijay Devane, Mohan Thete
# Filename:			task_1b.py
# Functions:		applyPerspectiveTransform, detectMaze, writeToCsv, solve_maze


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv, csv)               ##
##############################################################
import numpy as np
import cv2
import csv
##############################################################


################# ADD UTILITY FUNCTIONS HERE #################
## You can define any utility functions for your code.      ##
## Please add proper comments to ensure that your code is   ##
## readable and easy to understand.                         ##
##############################################################
def solve_maze(img, coordinate,size_of_cell):
	"""
	Purpose:
	---
	Takes a each cell image, its coordinates and size of each cell as input and convert this cell into a unique encode and return its decimal equivalent value.
	""" 
	size = Cell_Size=size_of_cell
	h = Cell_Size*(coordinate[0]+1)
	w = Cell_Size*(coordinate[1]+1)
	h0= Cell_Size*coordinate[0]
	w0= Cell_Size*coordinate[1]

	## This takes one cell at a time ##
	block = img[h0:h,w0:w]

	## Here we applied simple logic. According the wall is ##
	## present or not in the image the bool operator gives ##
	## value 1 or 0 respectively when it multiplied by     ##
	## respective weight and summation of all sides gives  ##
	## binary number. Then we convert this number in       ##
	## decimal value.                                      ##
	left  = bool(block[int(size/2),0]) *1
	up    = bool(block[0,int(size/2)]) *10
	right = bool(block[int(size/2),int(size-1)])*100
	down  = bool(block[int(size-1),int(size/2)])*1000
	edge = up+down+left+right
	stredge=str(edge)
	binary_to_decimal_encode = int(stredge,2)
	
	return binary_to_decimal_encode

##############################################################


def applyPerspectiveTransform(input_img):

	"""
	Purpose:
	---
	takes a maze test case image as input and applies a Perspective Transfrom on it to isolate the maze

	Input Arguments:
	---
	`input_img` :   [ numpy array ]
		maze image in the form of a numpy array
	
	Returns:
	---
	`warped_img` :  [ numpy array ]
		resultant warped maze image after applying Perspective Transform
	
	Example call:
	---
	warped_img = applyPerspectiveTransform(input_img)
	"""

	warped_img = None

	##############	ADD YOUR CODE HERE	##############
	gray = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
	gray_blur = cv2.GaussianBlur(gray,(5,5),1)
	_, thresh = cv2.threshold(gray_blur, 127, 255, cv2.THRESH_BINARY_INV)
	contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	for contour in contours:
		epsilon = 0.01*cv2.arcLength(contour,True)
		approx = cv2.approxPolyDP(contour,epsilon,True)
		area = cv2.contourArea(approx)

		## We are assuming that shape of maze is quadrilateral only ##
		if len(approx)==4:
			if area >=5000 and area<=260100:
				rect = np.zeros((4, 2), dtype="float32")
				l=[approx[0][0],approx[1][0],approx[2][0],approx[3][0]]

				## Setting the corner points of an image in order ##
				s = np.sum(l,axis=1)
				rect[0] = l[np.argmin(s)]
				rect[2] = l[np.argmax(s)]
				diff = np.diff(l, axis=1)
				rect[1] = l[np.argmin(diff)]
				rect[3] = l[np.argmax(diff)]

	pts1 = np.float32([[rect[0][0],rect[0][1]], [rect[1][0],rect[1][1]],[rect[3][0],rect[3][1]],[rect[2][0],rect[2][1]]]) 
	pts2 = np.float32([[0, 0], [500, 0], [0, 500], [500, 500]]) 
	matrix = cv2.getPerspectiveTransform(pts1, pts2) 
	result = cv2.warpPerspective(gray, matrix, (500,500))
	warped_img = result

	##################################################

	return warped_img


def detectMaze(warped_img):

	"""
	Purpose:
	---
	takes the warped maze image as input and returns the maze encoded in form of a 2D array

	Input Arguments:
	---
	`warped_img` :    [ numpy array ]
		resultant warped maze image after applying Perspective Transform
	
	Returns:
	---
	`maze_array` :    [ nested list of lists ]
		encoded maze in the form of a 2D array

	Example call:
	---
	maze_array = detectMaze(warped_img)
	"""

	maze_array = []

	##############	ADD YOUR CODE HERE	##############
	_,img2 = cv2.threshold(warped_img,127,255,cv2.THRESH_BINARY_INV)
	binary_img = img2
	array_of_edges = []
	cell_size=50

	## This for loop gives binary image, coordinates of each cell ##
	## and the cell size to the solve_maze function and return    ##
	## the encoded maze in the form of 2d array.                  ##
	for i in range (10):
		array_of_edges.append([])
		for j in range(10):
			sz = [i,j]
			edge = solve_maze(binary_img, sz,cell_size)
			array_of_edges[i].append(edge)
	maze_array = array_of_edges

	##################################################

	return maze_array


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
def writeToCsv(csv_file_path, maze_array):

	"""
	Purpose:
	---
	takes the encoded maze array and csv file name as input and writes the encoded maze array to the csv file

	Input Arguments:
	---
	`csv_file_path` :	[ str ]
		file path with name for csv file to write
	
	`maze_array` :		[ nested list of lists ]
		encoded maze in the form of a 2D array
	
	Example call:
	---
	warped_img = writeToCsv('test_cases/maze00.csv', maze_array)
	"""

	with open(csv_file_path, 'w', newline='') as file:
		writer = csv.writer(file)
		writer.writerows(maze_array)


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
# 
# Function Name:    main
#        Inputs:    None
#       Outputs:    None
#       Purpose:    This part of the code is only for testing your solution. The function first takes 'maze00.jpg'
# 					as input, applies Perspective Transform by calling applyPerspectiveTransform function,
# 					encodes the maze input in form of 2D array by calling detectMaze function and writes this data to csv file
# 					by calling writeToCsv function, it then asks the user whether to repeat the same on all maze images
# 					present in 'test_cases' folder or not. Write your solution ONLY in the space provided in the above
# 					applyPerspectiveTransform and detectMaze functions.

if __name__ == "__main__":

	# path directory of images in 'test_cases' folder
	img_dir_path = 'test_cases/'

	# path to 'maze00.jpg' image file
	file_num = 0
	img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'

	print('\n============================================')
	print('\nFor maze0' + str(file_num) + '.jpg')

	# path for 'maze00.csv' output file
	csv_file_path = img_dir_path + 'maze0' + str(file_num) + '.csv'
	
	# read the 'maze00.jpg' image file
	input_img = cv2.imread(img_file_path)

	# get the resultant warped maze image after applying Perspective Transform
	warped_img = applyPerspectiveTransform(input_img)

	if type(warped_img) is np.ndarray:

		# get the encoded maze in the form of a 2D array
		maze_array = detectMaze(warped_img)

		if (type(maze_array) is list) and (len(maze_array) == 10):

			print('\nEncoded Maze Array = %s' % (maze_array))
			print('\n============================================')
			
			# writes the encoded maze array to the csv file
			writeToCsv(csv_file_path, maze_array)

			cv2.imshow('warped_img_0' + str(file_num), warped_img)
			cv2.waitKey(0)
			cv2.destroyAllWindows()
		
		else:

			print('\n[ERROR] maze_array returned by detectMaze function is not complete. Check the function in code.\n')
			exit()
	
	else:

		print('\n[ERROR] applyPerspectiveTransform function is not returning the warped maze image in expected format! Check the function in code.\n')
		exit()
	
	choice = input('\nDo you want to run your script on all maze images ? => "y" or "n": ')

	if choice == 'y':

		for file_num in range(1, 10):
			
			# path to image file
			img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'

			print('\n============================================')
			print('\nFor maze0' + str(file_num) + '.jpg')

			# path for csv output file
			csv_file_path = img_dir_path + 'maze0' + str(file_num) + '.csv'
			
			# read the image file
			input_img = cv2.imread(img_file_path)

			# get the resultant warped maze image after applying Perspective Transform
			warped_img = applyPerspectiveTransform(input_img)

			if type(warped_img) is np.ndarray:

				# get the encoded maze in the form of a 2D array
				maze_array = detectMaze(warped_img)

				if (type(maze_array) is list) and (len(maze_array) == 10):

					print('\nEncoded Maze Array = %s' % (maze_array))
					print('\n============================================')
					
					# writes the encoded maze array to the csv file
					writeToCsv(csv_file_path, maze_array)

					cv2.imshow('warped_img_0' + str(file_num), warped_img)
					cv2.waitKey(0)
					cv2.destroyAllWindows()
				
				else:

					print('\n[ERROR] maze_array returned by detectMaze function is not complete. Check the function in code.\n')
					exit()
			
			else:

				print('\n[ERROR] applyPerspectiveTransform function is not returning the warped maze image in expected format! Check the function in code.\n')
				exit()

	else:

		print('')

