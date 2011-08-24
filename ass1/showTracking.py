#!/usr/bin/python
#===============================================================================
#
#         FILE:  showTracking.py
#
#        USAGE:  ./showTracking.py  
#
#  DESCRIPTION:  The Assignment 1 of COMP9517 
#
#      OPTIONS:  ---
# REQUIREMENTS:  ---
#         BUGS:  ---
#        NOTES:  ---
#       AUTHOR:  Steven(Silin) YOU, steven@gosteven.com
#      COMPANY:  (on my own)
#      VERSION:  1.0
#      CREATED:  08/09/2011 14:00:31
#     REVISION:  ---
#===============================================================================
import cv2.cv as cv
import os
import sys
import glob
import math
import time


sys.setrecursionlimit(5000)
    
isShowImg = 0
path = 'data/'
#for infile in glob.glob(os.path.join(path,'*.jpg')):
#    imagefile = infile
for num in range(70,140):
    imagefile = path + "v3_" + str(num) + ".jpg"
    infile = imagefile
    print "----read image file----"
    print infile
    outputFileName = os.path.basename(imagefile)
    outimg = "outimg/_"+outputFileName
    a = cv.LoadImage(outimg)
    cv.ShowImage("Tracking"+ str(num),a)
    time.sleep(0.2)
    
