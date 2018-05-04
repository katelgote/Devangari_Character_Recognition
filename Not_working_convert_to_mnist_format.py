
"""
This file is taken from 
https://github.com/davidflanagan/notMNIST-to-MNIST/blob/master/convert_to_mnist_format.py

Necessary modifications are done
"""

# This python script converts a sample of the notMNIST dataset into 
# the same file format used by the MNIST dataset. If you have a program
# that uses the MNIST files, you can run this script over notMNIST to
# produce a new set of data files that should be compatible with
# your program.
#
# Instructions:
#
# 1) if you already have a MNIST data/ directory, rename it and create 
#    a new one
#

#
# 2) Run this script to convert the data to MNIST files, then compress them.
#    These commands will produce files of the same size as MNIST
#    notMNIST is larger than MNIST, and you can increase the sizes if you want.

#------------------------------------------------------------------------------------------------------------------------------
"""

300 images in each folder for Test

# $ python convert_to_mnist_format.py data/Test 300 MNIST_data/t10k-labels-idx1-ubyte MNIST_data/t10k-images-idx3-ubyte
# $ python convert_to_mnist_format.py data/Train 1700 MNIST_data/train-labels-idx1-ubyte MNIST_data/train-images-idx3-ubyte
# $ gzip MNIST_data/*ubyte

"""

import numpy, imageio, glob, sys, os, random

from pathlib import Path

###***********************************************************************

"""
CHANGES MADE HERE by Kunal Telgote

"""

core_dir = os.getcwd() # os.getcwd() gives this '/home/kunal/Documents/Sem8/ML/final'

my_dir = os.path.join(core_dir,'MNIST_data') 

my_dir = Path(my_dir) 

if my_dir.is_dir():
  pass
else:  
  os.mkdir('MNIST_data')  

# __name__=='__main__'

# print sys.argv

###***********************************************************************

def get_labels_and_files(folder, number):
  # Make a list of lists of files for each label
  filelists = []

#----------------------------------------------------------------------------------------------
  train_test_folder = sys.argv[1]

  all_folder_names = os.listdir(train_test_folder) #folder in which Test/train images are

#----------------------------------------------------------------------------------------------

  for label in all_folder_names:
    filelist = []
    filelists.append(filelist);
    dirname = os.path.join(folder, label)
    for file in os.listdir(dirname):
      if (file.endswith('.png')):
        fullname = os.path.join(dirname, file)
        if (os.path.getsize(fullname) > 0):
          filelist.append(fullname)
        else:
          print('file ' + fullname + ' is empty')
    # sort each list of files so they start off in the same order
    # regardless of how the order the OS returns them in
    filelist.sort()

  # Take the specified number of items for each label and
  # build them into an array of (label, filename) pairs
  # Since we seeded the RNG, we should get the same sample each run
  labelsAndFiles = []
  for label in range(0,30):      #*********************************  #30 total no. folders in Test for each class
    filelist = random.sample(filelists[label], number)
    for filename in filelist:
      labelsAndFiles.append((label, filename))

  return labelsAndFiles

def make_arrays(labelsAndFiles):
  images = []
  labels = []
  for i in range(0, len(labelsAndFiles)):

    # display progress, since this can take a while
    if (i % 100 == 0):
      sys.stdout.write("\r%d%% complete" % ((i * 100)/len(labelsAndFiles)))
      sys.stdout.flush()

    filename = labelsAndFiles[i][1]
    try:
      image = imageio.imread(filename)
      images.append(image)
      labels.append(labelsAndFiles[i][0])
    except:
      # If this happens we won't have the requested number
      print("\nCan't read image file " + filename)

  count = len(images)
  imagedata = numpy.zeros((count,32,32), dtype=numpy.uint8)
  labeldata = numpy.zeros(count, dtype=numpy.uint8)
  for i in range(0, len(labelsAndFiles)):
    imagedata[i] = images[i]
    labeldata[i] = labels[i]
  print("\n")
  return imagedata, labeldata

def write_labeldata(labeldata, outputfile):
  header = numpy.array([0x0805, len(labeldata)], dtype='>i4')
  with open(outputfile, "wb") as f:
    f.write(header.tobytes())
    f.write(labeldata.tobytes())

def write_imagedata(imagedata, outputfile):
  header = numpy.array([0x0808, len(imagedata), 36, 36], dtype='>i4')
  with open(outputfile, "wb") as f:
    f.write(header.tobytes())
    f.write(imagedata.tobytes())
    


def main(argv):
  # Uncomment the line below if you want to seed the random
  # number generator in the same way I did to produce the
  # specific data files in this repo.
  # random.seed(int("notMNIST", 36))

  labelsAndFiles = get_labels_and_files(argv[1], int(argv[2]))
  random.shuffle(labelsAndFiles)
  imagedata, labeldata = make_arrays(labelsAndFiles)
  write_labeldata(labeldata, argv[3])
  write_imagedata(imagedata, argv[4])

if __name__=='__main__':
  main(sys.argv)

