'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 3A of Pharma Bot (PB) Theme (eYRC 2022-23).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			[ Team-ID ]
# Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:			task_3a.py
# Functions:		detect_all_nodes,detect_paths_to_graph, detect_arena_parameters, path_planning, paths_to_move
# 					[ Comma separated list of functions in this file ]

####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv)                    ##
##############################################################
import numpy as np
import cv2
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################
def graph(paths,lower_red,upper_red):
	mask= cv2.inRange(image, lower_red, upper_red)
	cnts = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	for c in cnts[0]:
		M = cv2.moments(c)
		cX = int(M["m10"] / M["m00"])
		cY = int(M["m01"] / M["m00"])
		scX=str(cX)
		scX=int(scX[0])+64
		scX=chr(scX)
		scY=str(cY)
		scY=scY[0]
		paths[scX+scY]={}
		b,g,r=image[cY,cX+20]
		if(b==0 and g==0 and r==0):
			rcX=str(cX+100)
			rcX=int(rcX[0])+64
			rcX=chr(rcX)
			rcY=str(cY)
			rcY=rcY[0]
			paths[scX+scY][rcX+rcY]=1
		b,g,r=image[cY,cX-20]
		if(b==0 and g==0 and r==0):
			lcX=str(cX-100)
			lcX=int(lcX[0])+64
			lcX=chr(lcX)
			lcY=str(cY)
			lcY=lcY[0]
			paths[scX+scY][lcX+lcY]=1    
		b,g,r=image[cY+20,cX]
		if(b==0 and g==0 and r==0):
			ucX=str(cX)
			ucX=int(ucX[0])+64
			ucX=chr(ucX)
			ucY=str(cY+100)
			ucY=ucY[0]
			paths[scX+scY][ucX+ucY]=1      
		b,g,r=image[cY-20,cX]
		if(b==0 and g==0 and r==0):
			dcX=str(cX)
			dcX=int(dcX[0])+64
			dcX=chr(dcX)
			dcY=str(cY-100)
			dcY=dcY[0]
			paths[scX+scY][dcX+dcY]=1
	return paths 



##############################################################

def detect_all_nodes(image):
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a list of
	nodes in which traffic signals, start_node and end_node are present in the image

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`traffic_signals, start_node, end_node` : [ list ], str, str
			list containing nodes in which traffic signals are present, start and end node too
	
	Example call:
	---
	traffic_signals, start_node, end_node = detect_all_nodes(maze_image)
	"""    
	traffic_signals = []
	start_node = ""
	end_node = ""

	##############	ADD YOUR CODE HERE	##############

	#Traffic signals

	lower_red = np.array([0, 0, 255])
	upper_red = np.array([0, 0, 255])
	mask= cv2.inRange(image, lower_red, upper_red)
	cnts = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	for c in cnts[0]:
		M = cv2.moments(c)
		cX = int(M["m10"] / M["m00"])
		cY = int(M["m01"] / M["m00"])
		cX=str(cX)
		cX=int(cX[0])+64
		cX=chr(cX)
		cY=str(cY)
		cY=cY[0]
		traffic_signals.append(cX+cY)
		traffic_signals.sort()


    #Start Node

	lower_red = np.array([0, 255, 0])
	upper_red = np.array([0, 255, 0])
	mask= cv2.inRange(image, lower_red, upper_red)
	cnts = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	for c in cnts[0]:
		if len(c)==4 and cv2.contourArea(c)==144:
			M = cv2.moments(c)
			cX = int(M["m10"] / M["m00"])
			cY = int(M["m01"] / M["m00"])
			cX=str(cX)
			cX=int(cX[0])+64
			cX=chr(cX)
			cY=str(cY)
			cY=cY[0]
			start_node=cX+cY
		else:
			continue	

    #End Node	

	lower_red = np.array([189, 43, 105])
	upper_red = np.array([189, 43, 105])
	mask= cv2.inRange(image, lower_red, upper_red)
	cnts = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	for c in cnts[0]:
		M = cv2.moments(c)
		cX = int(M["m10"] / M["m00"])
		cY = int(M["m01"] / M["m00"])
		cX=str(cX)
		cX=int(cX[0])+64
		cX=chr(cX)
		cY=str(cY)
		cY=cY[0]
		end_node=cX+cY
	##################################################

	return traffic_signals, start_node, end_node


def detect_paths_to_graph(image):
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a dictionary of the
	connect path from a node to other nodes and will be used for path planning

	HINT: Check for the road besides the nodes for connectivity 

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`paths` : { dictionary }
			Every node's connection to other node and set it's value as edge value 
			Eg. : { "D3":{"C3":1, "E3":1, "D2":1, "D4":1}, 
					"D5":{"C5":1, "D2":1, "D6":1 }  }

			Why edge value 1? -->> since every road is equal

	Example call:
	---
	paths = detect_paths_to_graph(maze_image)
	"""    

	paths = {}

	##############	ADD YOUR CODE HERE	##############
	
	lower_red = np.array([255, 0, 0])
	upper_red = np.array([255, 0, 0])
	path=graph(paths,lower_red,upper_red)
	paths.update(path)
	lower_red = np.array([0, 0, 255])
	upper_red = np.array([0, 0, 255])
	path=graph(paths,lower_red,upper_red)
	paths.update(path)
	lower_red = np.array([0, 255, 0])
	upper_red = np.array([0, 255, 0])
	path=graph(paths,lower_red,upper_red)
	paths.update(path)
	lower_red = np.array([189, 43, 105])
	upper_red = np.array([189, 43, 105])
	path=graph(paths,lower_red,upper_red)
	paths.update(path)
	

	##################################################

	return paths



def detect_arena_parameters(maze_image):
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a dictionary
	containing the details of the different arena parameters in that image

	The arena parameters are of four categories:
	i) traffic_signals : list of nodes having a traffic signal
	ii) start_node : Start node which is mark in light green
	iii) end_node : End node which is mark in Purple
	iv) paths : list containing paths

	These four categories constitute the four keys of the dictionary

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`arena_parameters` : { dictionary }
			dictionary containing details of the arena parameters
	
	Example call:
	---
	arena_parameters = detect_arena_parameters(maze_image)

	Eg. arena_parameters={"traffic_signals":[], 
	                      "start_node": "E4", 
	                      "end_node":"A3", 
	                      "paths": {}}
	"""    
	arena_parameters = {}

	##############	ADD YOUR CODE HERE	##############
	traffic_signals,start_node,end_node=detect_all_nodes(maze_image)
	arena_parameters["traffic_signals"]=traffic_signals
	arena_parameters["start_node"]=start_node
	arena_parameters["end_node"]=end_node
	##################################################
	
	return arena_parameters

def path_planning(graph, start, end):

	"""
	Purpose:
	---
	This function takes the graph(dict), start and end node for planning the shortest path

	** Note: You can use any path planning algorithm for this but need to produce the path in the form of 
	list given below **

	Input Arguments:
	---
	`graph` :	{ dictionary }
			dict of all connecting path
	`start` :	str
			name of start node
	`end` :		str
			name of end node


	Returns:
	---
	`backtrace_path` : [ list of nodes ]
			list of nodes, produced using path planning algorithm

		eg.: ['C6', 'C5', 'B5', 'B4', 'B3']
	
	Example call:
	---
	arena_parameters = detect_arena_parameters(maze_image)
	"""    

	backtrace_path=[]

	##############	ADD YOUR CODE HERE	##############
	
	##################################################


	return backtrace_path

def paths_to_moves(paths, traffic_signal):

	"""
	Purpose:
	---
	This function takes the list of all nodes produces from the path planning algorithm
	and connecting both start and end nodes

	Input Arguments:
	---
	`paths` :	[ list of all nodes ]
			list of all nodes connecting both start and end nodes (SHORTEST PATH)
	`traffic_signal` : [ list of all traffic signals ]
			list of all traffic signals
	---
	`moves` : [ list of moves from start to end nodes ]
			list containing moves for the bot to move from start to end

			Eg. : ['UP', 'LEFT', 'UP', 'UP', 'RIGHT', 'DOWN']
	
	Example call:
	---
	moves = paths_to_moves(paths, traffic_signal)
	"""    
	
	list_moves=[]

	##############	ADD YOUR CODE HERE	##############
	
	##################################################

	return list_moves

######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THIS FUNCTION #########	

if __name__ == "__main__":

	# # path directory of images
	img_dir_path = "test_images/"

	for file_num in range(0,10):
			
			img_key = 'maze_00' + str(file_num)
			img_file_path = img_dir_path + img_key  + '.png'
			# read image using opencv
			image = cv2.imread(img_file_path)
			
			# detect the arena parameters from the image
			arena_parameters = detect_arena_parameters(image)
			print('\n============================================')
			print("IMAGE: ", file_num)
			print(arena_parameters["start_node"], "->>> ", arena_parameters["end_node"] )

			# path planning and getting the moves
			back_path=path_planning(arena_parameters["paths"], arena_parameters["start_node"], arena_parameters["end_node"])
			moves=paths_to_moves(back_path, arena_parameters["traffic_signals"])

			print("PATH PLANNED: ", back_path)
			print("MOVES TO TAKE: ", moves)

			# display the test image
			cv2.imshow("image", image)
			cv2.waitKey(0)
			cv2.destroyAllWindows()