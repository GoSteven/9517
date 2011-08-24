#!/usr/bin/python
#===============================================================================
#
#         FILE:  task.py
#
#        USAGE:  ./task.py  
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

class Image:

    def __init__(self,param):
        self.ori = cv.LoadImage(param)
        self.img = cv.LoadImage(param)
        self.blrImg = cv.LoadImage(param)
        self.maxlable = 0
        #blur img
        cv.Smooth(self.img,self.blrImg,cv.CV_MEDIAN,5,5)
        #global lable 
        self.lable = cv.CreateImage(cv.GetSize(self.img),8,1)
        cv.Set(self.lable,0)

        cv.Threshold(self.img,self.img,100,255,cv.CV_THRESH_BINARY)
        cv.Threshold(self.blrImg,self.blrImg,80,255,cv.CV_THRESH_BINARY)

        self.grey = cv.CreateImage(cv.GetSize(self.ori),8,1)
        self.mask = cv.CreateImage(cv.GetSize(self.blrImg),8,1)
        cv.CvtColor(self.ori,self.grey,cv.CV_BGR2GRAY)
        cv.CvtColor(self.blrImg,self.mask,cv.CV_BGR2GRAY)

    def calculateMeanAndVariance(self,ori,mask):
        backGroundSum = 0
        foreGroundSum = 0
        backGroundCount = 0
        foreGroundCount = 0
        #calculate mean
        for i in range(ori.width):
            for j in range(ori.height):
                if (mask[j,i] == 255):
                    foreGroundSum += ori[j,i] + 0
                    foreGroundCount += 1
                else:
                    backGroundSum += ori[j,i] + 0
                    backGroundCount += 1
        backGroundMean = backGroundSum / backGroundCount
        foreGroundMean = foreGroundSum / foreGroundCount
        print "mean: background", backGroundMean, "foreGround", foreGroundMean
        meanString1 = "mean: "
        meanString2 = "background" + str(backGroundMean) 
        meanString3 = "foreGround" + str(foreGroundMean)

        #calculate variance
        varBackGroundSum = 0
        varForeGroundSum = 0
        for i in range(ori.width):
            for j in range(ori.height):
                if (mask[j,i] == 255):
                    varForeGroundSum += math.pow(foreGroundMean - ori[j,i], 2)
                else:
                    varBackGroundSum += math.pow(backGroundMean - ori[j,i], 2)
        varBackGround = varBackGroundSum / backGroundCount
        varForeGround = varForeGroundSum / foreGroundCount
        print "variance: background", varBackGround, "foreGround", varForeGround 
        varString1 = "variance: "
        varString2 = "background" + str(varBackGround)
        varString3 = "foreGround" + str(varForeGround)
        font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 0.3, 0.3, 0, 1, 8) 
#        cv.PutText(self.ori,meanString1,(20,20),font,cv.Scalar(200, 200, 20))
#        cv.PutText(self.ori,meanString2,(20,30),font,cv.Scalar(200, 200, 20))
#        cv.PutText(self.ori,meanString3,(20,40),font,cv.Scalar(200, 200, 20))
#        cv.PutText(self.ori,varString1,(20,50),font,cv.Scalar(200, 200, 20))
#        cv.PutText(self.ori,varString2,(20,60),font,cv.Scalar(200, 200, 20))
#        cv.PutText(self.ori,varString3,(20,70),font,cv.Scalar(200, 200, 20))




    def iterateNeibor(self,img,j,i):
        if (i>=0 and i<img.width and j>=0 and j<img.height and img[j,i] == 255):
            self.lableNeibor(img, j, i)

    def lableNeibor(self,img,j,i):
        if (self.lable[j,i] > 0):
            return
        self.lable[j,i] = self.maxlable
        self.iterateNeibor(img, j+1, i)
        self.iterateNeibor(img, j, i+1)
        self.iterateNeibor(img, j, i-1)
        self.iterateNeibor(img, j-1, i)
        
    def lableimg(self,src):
        grey  = cv.CreateImage(cv.GetSize(src),8,1)
        cv.CvtColor(src,grey,cv.CV_BGR2GRAY)
        self.removeWhiteLine(grey)
        for i in range(grey.width):
            for j in range(grey.height):
                if (grey[j,i] == 255 and self.lable[j,i] == 0):
                    self.maxlable = self.maxlable+1
                    self.lableNeibor(grey,j,i)

    def incr_item(self,dict, key):
        try:
            item = dict[key]
        except KeyError:
            item = 0
        dict[key] = item + 1
    def findMostCommonLable(self,grey,masklable):
        countLable = {}
        for i in range(grey.width):
            for j in range(grey.height):
                if (masklable[j,i]>0 and self.lable[j,i] == 255):
                    self.incr_item(countLable,masklable[j,i])
#        for w in sorted(countLable, key=countLable.get, reverse=True):
#            print w,countLable[w]
        for w in sorted(countLable, key=countLable.get, reverse=True):
            if (w>0):
                return w

    def setLevel(self,level):
        for i in range(self.lable.width):
            for j in range(self.lable.height):
                if (self.lable[j,i] == 255):
                    if (level == None):
                        self.lable[j,i] = 244
                    else:
                        self.lable[j,i] = level
    def lableimgBasedOnMask(self,src,masklable):
        grey  = cv.CreateImage(cv.GetSize(src),8,1)
        cv.CvtColor(src,grey,cv.CV_BGR2GRAY)
        self.removeWhiteLine(grey)
        for i in range(grey.width):
            for j in range(grey.height):
                if (grey[j,i] == 255 and self.lable[j,i] == 0):
                    self.maxlable = 255
                    self.lableNeibor(grey,j,i)
#                    cv.ShowImage("afterLable2",self.lable)
#                    cv.WaitKey(0)
                    level = self.findMostCommonLable(grey, masklable)
                    print "level", level
                    if (~ (level ==None)):
                        self.findCenterAndLablePlus(self.lable,level,255)
                    self.setLevel(level)
                    

    def findCenterAndLablePlus(self,lable,level,targetlevel):
        sumWidth = 0
        sumHeight = 0
        count = 0
        for i in range(self.lable.width):
            for j in range(self.lable.height):
                if (self.lable[j,i] == targetlevel):
                    sumWidth += i
                    sumHeight += j
                    count += 1
        if (count < 8):
            return
        meanWidth = sumWidth / count
        meanHeight = sumHeight / count
        font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 0.3, 0.3, 0, 1, 8) 
        try:
            level = float(level)
            cv.PutText(self.ori,str(int(level)),(meanWidth,meanHeight),font,cv.Scalar(10, 200, 200))
        except TypeError:
            level = 0.5

    def findCenterAndLable(self,lable,level):
        sumWidth = 0
        sumHeight = 0
        count = 0
        for i in range(self.lable.width):
            for j in range(self.lable.height):
                if (self.lable[j,i] == level):
                    sumWidth += i
                    sumHeight += j
                    count += 1
        if (count < 10):
            return
        meanWidth = sumWidth / count
        meanHeight = sumHeight / count
        font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 0.3, 0.3, 0, 1, 8) 
        cv.PutText(self.ori,str(level),(meanWidth,meanHeight),font,cv.Scalar(10, 200, 200))
#        cv.PutText(self.blrImg,str(level),(meanHeight,meanWidth),font,cv.Scalar(10, 200, 200))

    def removeWhiteLine(self,img):
        for i in range(6):
            count = 0
            for j in range(img.height):
                img[j,i] = 0
                if (img[j,i] == 255):
                    count += 1
            if (count > self.lable.height*3/4):
                for j in range(img.height):
                    img[j,i] = 0



    

sys.setrecursionlimit(100000)
    
isShowImg = 1
path = 'data/'
prePic = None
#for infile in glob.glob(os.path.join(path,'*.jpg')):
#    imagefile = infile

#for num in range(70,139):
#    imagefile = path + "v3_" + str(num) + ".jpg"
for num in range(1,5):
    imagefile = "testdata/test_" + str(num) + ".jpg" 
    infile = imagefile
    print "----read image file----"
    print infile
    pic = Image(imagefile)
    outputFileName = os.path.basename(imagefile)
    
    if (prePic == None or isShowImg == 1):
        pic.lableimg(pic.blrImg)
        #calculate mean and variance
        pic.calculateMeanAndVariance(pic.grey, pic.mask)
        for i in range(1, pic.maxlable):
            pic.findCenterAndLable(pic.lable,i)
        if (isShowImg == 1):
            cv.ShowImage("afterLable",pic.ori)
            cv.ShowImage("blrthrlab",pic.blrImg)
            cv.WaitKey(0)
        cv.SaveImage("outimg/_"+outputFileName, pic.ori)
        cv.SaveImage("outimg/0_"+outputFileName, pic.blrImg)
        prePic = pic
    else:
        pic.lableimgBasedOnMask(pic.blrImg,prePic.lable)
        cv.SaveImage("outimg/_"+outputFileName, pic.ori)
        
        if (isShowImg == 1):
            cv.ShowImage("afterLable2",prePic.ori)
            cv.WaitKey(0)
#    cv.WaitKey(0)
