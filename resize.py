#### **************************************************
"""

Provide name of folder whose img are to be converted 

USAGE: python resize.py Test 		#for 'Test' folder 

after converting ... change data folder name Test_data or something ....

and then again run this file for Train data or it will replace the values

"""
#### **************************************************

import numpy as np 
import cv2
import os

import numpy, imageio, glob, sys, random

from pathlib import Path

# import argparse

# parser = argparse.ArgumentParser()

# parser.add_argument('-f','--folder', help='Imput file name', required=True)
# args = parser.parse_args()

# # if args.f.is_dir():
# name_of = args

# else:	
	# print ('no such file exists')


# print sys.argv[1]

core_dir = os.getcwd() # os.getcwd() gives this '/home/kunal/Documents/Sem8/ML/convert_img'

my_dir = os.path.join(core_dir,'data') 
check_train_test = os.path.join(my_dir,sys.argv[1])
name_of_folder = sys.argv[1]

my_dir = Path(my_dir) 

check_train_test = Path(check_train_test)

if my_dir.is_dir():
	if check_train_test.is_dir(): #check id data/Test or Train is present
		pass
	else:
		os.makedirs('data/%s' %name_of_folder)		
else:	
	os.makedirs('data/%s' %name_of_folder) #create a folder to store resized images

curr_dir = os.path.abspath("data") #'/home/kunal/Documents/Sem8/ML/convert_img/data'

all_folder_names = os.listdir(sys.argv[1]) 		#folder in which Test images are present


dir_path = os.path.abspath(sys.argv[1]) #folder Test's dir (path) '/home/kunal/Documents/Sem8/ML/convert_img/Test'


conv_file_folder = os.path.join(curr_dir,sys.argv[1])

os.chdir(conv_file_folder) #going into the curr_dir

for label in all_folder_names:

	char_folder = os.path.join(curr_dir,sys.argv[1],label) #'/home/kunal/Documents/Sem8/ML/convert_img/data/Test/digit_0'
	my_dir = Path(char_folder) 
	if my_dir.is_dir():
		pass
	else:	
		os.mkdir(label) #create a folder to store resized images

	i=0
	dirname = os.path.join(dir_path, label) #'/home/kunal/Documents/Sem8/ML/convert_img/Test/digit_0'
	for file in os.listdir(dirname):        #getting all the names of the images '****.png' 300test 1700train
	                                        #
		if (file.endswith('.png')):

		    # fullname = os.path.join(dirname, file)
		    # if (os.path.getsize(fullname) > 0):

			file_img = os.path.join(dirname,file) #'/home/kunal/Documents/Sem8/ML/convert_img/Test/digit_0/66576.png'
			img = cv2.imread(file_img)	
		  
			img_new = cv2.resize(img,(28,28))

			resized_img_file = os.path.join(char_folder,file)

			resized_img_file = Path(resized_img_file)
			if resized_img_file.is_file():
				pass
			else:
				cv2.imwrite(os.path.join(char_folder,file),img_new)
			
			i+=1
		
		else:
			i+=1

	print ('currently resizing folder %s' %label)

__name__=='__main__'