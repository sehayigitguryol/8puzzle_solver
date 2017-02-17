#!usr/bin/python
import os
import pwd
import re
import sys
import copy
import random
import numpy as np
from operator import itemgetter
import operator
import heapq
import timeit


def hFunc(state):
#manhattan distance is used
	count=0
	for i in digits:
		(x_state,y_state)=index_2d(state,i)
		
		(x_final,y_final)=index_2d(finalConfig,i)
		count=count+abs(x_state-x_final)+abs(y_state-y_final)
 	return count

def index_2d(array, value):
    for row, col in enumerate(array):
        if value in col:
            return (row, col.index(value))

#switches 0 with the up cell and calculates its hvalue
def look_up(array, row_zero,col_zero):
	if row_zero>0:
		new_array = copy.deepcopy(array)
		number= new_array[row_zero-1][col_zero]
		new_array[row_zero][col_zero]=number
		new_array[row_zero-1][col_zero]=0
 		return new_array
 	else:
 		l=[]
 		return l
#switches 0 with the down cell and calculates its hvalue
def look_down(array, row_zero,col_zero):
	if row_zero<2:	
		new_array = copy.deepcopy(array)
		number= new_array[row_zero+1][col_zero]
		new_array[row_zero][col_zero]=number
		new_array[row_zero+1][col_zero]=0
 	
 		return new_array
 	else:
 		l=[]
 		return l
#switches 0 with the left cell and calculates its hvalue
def look_left(array, row_zero,col_zero):
	if col_zero>0:
		new_array = copy.deepcopy(array)
		number= new_array[row_zero][col_zero-1]
		new_array[row_zero][col_zero]=number
		new_array[row_zero][col_zero-1]=0
 		return new_array
 	else:
 		l=[]
 		return l
#switches 0 with the right cell and calculates its h value
def look_right(array, row_zero,col_zero):
	if col_zero<2:
		new_array = copy.deepcopy(array)
		number= new_array[row_zero][col_zero+1]
		new_array[row_zero][col_zero]=number
		new_array[row_zero][col_zero+1]=0
 		return new_array
 	else:
 		l=[]
 		return l

def solvable_checker(array):
	inversion=0
	for i in range(0,8):
		for j in range(i+1,9):
			if array[i] > array[j] and array[i]!= 0 and array[j]!=0:
				inversion+=1
				

	if inversion%2==1:
		print "This puzzle cannot be solved"
		return False
	else:				
		return True		




def path_extracter(start,visited):
	searched=finalConfig
	path=[searched]
	
	while not searched==start:
	
		if not isGreedy:
			searchedTuple= [item for item in visited if item[0] == searched]
			searchedTuple.sort(key=itemgetter(1))
			(_,searched,_)=searchedTuple.pop(0)
			
		else:
			searchedTuple =[item for item in visited if item[0] == searched]
			(_,searched)=searchedTuple.pop(0)

		path.append(searched)


	path.reverse()

	for p in path:
	
		print p

	numberOfMoves= len(path)	
	print "Number of Moves:" ,numberOfMoves-1
	return path,numberOfMoves-1


def greedy(start):
	openList=[]
	closeList=[]
	optimalPath=[]
	expand=0
	openList.append(start)
	
	
	while openList:
		
		
		current= openList.pop(0)
		
		if current==finalConfig:
			#optimal path shit
			#print optimalPath
			#optimalPath.append((current,prev,f_current))
			
			
			print "Number of states that expanded ", expand
			(path,numberOfMoves)=path_extracter(start,optimalPath)
		
			return path;
		
			
		closeList.append(current)
		(row_zero_current,col_zero_current)=index_2d(current, 0)
		successors=[look_up(current,row_zero_current,col_zero_current),
				look_down(current,row_zero_current,col_zero_current),
				look_left(current,row_zero_current,col_zero_current),
				look_right(current,row_zero_current,col_zero_current)]
		best_neighbor=[]

		for successor in successors:
			if successor and successor not in closeList:
				best_neighbor.append((successor,hFunc(successor)))
		

		if  best_neighbor:
			best_neighbor.sort(key=itemgetter(1))
			(neighbor,hvalue)= best_neighbor.pop(0)	
		
		
		
			openList.append(neighbor)
			optimalPath.append((neighbor,current))
			expand+=1
	print current		

	if current!=finalConfig:
		print "Couldn't find"
		return 0

								


#Each tuple contains (current position, previous position, fvalue of current, g value of current)
def a_and_wa_star(start,w):
	openList=[]
	closeList=[]
	optimalPath=[]
	expand=0
	openList.append((start,hFunc(start),0))
	
	
	while openList>0:
		
		openList.sort(key=itemgetter(1))
		(current,f_current,g_current)= openList.pop(0)
		
		#buraya bak
		if current==finalConfig:
			#optimal path shit
			#print optimalPath
			#optimalPath.append((current,prev,f_current))
			
			print "Number of states that expanded ", expand
			path=path_extracter(start,optimalPath)
			return path;
		
			
		closeList.append(current)
		(row_zero_current,col_zero_current)=index_2d(current, 0)
		successors=[look_up(current,row_zero_current,col_zero_current),
				look_down(current,row_zero_current,col_zero_current),
				look_left(current,row_zero_current,col_zero_current),
				look_right(current,row_zero_current,col_zero_current)]
				
		for successor in successors:
			if successor:
				
				if successor not in closeList	:
					
					#going one node to another costs 1 
					temp_g= g_current+1
					inOpenSet =[item for item in openList if item[0] == successor]
				#	print inOpenSet
					if not inOpenSet:
						##expanding a new node calculate its f and g values
						h_successor= hFunc(successor)
						openList.append((successor,temp_g+w*h_successor,temp_g))
						expand+=1
						g_successor= [item[2] for item in inOpenSet]
						if temp_g>= g_successor:
							pass
						else:
							
							
							
							optimalPath.append((successor,current,temp_g+h_successor))
					

	print "Number of states that expanded ", expand						
	return 0;

									
								
					
	



####Main block#######
isGreedy= False 
finalConfig= [[1,2,3],[4,5,6],[7,8,0]]

digits=[1,2,3,4,5,6,7,8]

digit=[1,2,3,4,5,6,7,8,0]



random.shuffle(digit)

init=[[0 for x in range(3)] for y in range(3)] 
for i in range (0,9):
	init[i%3][i/3]= digit[i]

user_decision= int(raw_input("Please enter corresponding Algorithm number\n"
	+" For A* algorithm type 1\n"+" For WA* algorithm type 2\n"+ " For Greedy Best-First Search algorithm type 3\n"))


if user_decision==2:
	w= int(raw_input("Please enter weight"))

	print "Initial configuration: \n", init
	start_time = timeit.default_timer()

	if solvable_checker(digit):
		a_and_wa_star(init,w)

	algorithm_exec = timeit.default_timer() - start_time
	print "Execution of algorithm took: " , algorithm_exec

elif user_decision==1:
	print "Initial configuration: \n", init
	start_time = timeit.default_timer()
	if solvable_checker(digit):
		a_and_wa_star(init,1)

	algorithm_exec = timeit.default_timer() - start_time
	print "Execution of algorithm took: " , algorithm_exec

else:
	print "Initial configuration: \n", init
	start_time = timeit.default_timer()
	isGreedy=True
	print isGreedy
	if solvable_checker(digit):
		greedy(init)
	algorithm_exec = timeit.default_timer() - start_time
	print "Execution of algorithm took: " , algorithm_exec


#greedy(Matrix)
#####################


 
