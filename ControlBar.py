'''
使用方法 : 拉動控制條改變參數
結果 : 
    終端顯示
    Threshold1 -> Canny第一個閾值
    Threshold2 -> Canny第二個閾值
    kernel -> 高斯模糊的參數 Line.52
'''
import cv2
import numpy as np
ImagePath = r'D:\python_computer_vision\aaa.png'
VideoPath = r'D:\media\railway_video\headup.mp4'

def Find_Parameter(VIDEO_FORMAT, PATH):  
    class TrackBar:
        def __init__(self):
            cv2.namedWindow("Trackbars")
            cv2.resizeWindow("Trackbars", 300, 150)
            cv2.createTrackbar("Threshold1", "Trackbars", 100, 255, self.nothing)
            cv2.createTrackbar("Threshold2", "Trackbars", 100, 255, self.nothing)
            cv2.createTrackbar("BlurKernel", "Trackbars", 0, 11, self.nothing)

        def nothing(self):
            pass        

        def valTrackbars(self): 
            self.Threshold1 = cv2.getTrackbarPos("Threshold1", "Trackbars")
            self.Threshold2 = cv2.getTrackbarPos("Threshold2", "Trackbars")
            self.kernel = cv2.getTrackbarPos("BlurKernel", "Trackbars")
            if self.kernel==0 or self.kernel % 2==0:
                self.kernel = self.kernel + 1
            return [self.Threshold1, self.Threshold2, self.kernel]

    bar = TrackBar()
    if VIDEO_FORMAT:
        cap = cv2.VideoCapture(VideoPath)
        frame_counter = 0
    while True:
        if VIDEO_FORMAT:
            ret, img = cap.read()
            FPS = 20
            if not ret:
                continue
            frame_counter+=1
            if frame_counter == int(cap.get(cv2.CAP_PROP_FRAME_COUNT)):
                frame_counter = 0
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        else:
            img = cv2.imread(PATH)
            FPS = 3
        result = bar.valTrackbars()
        print(f'Threshold1 : {result[0]}, Threshold2 : {result[1]}, kernel : {result[2]}')
        img = cv2.resize(img, (300, 500))
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #imgThreshold = cv2.threshold(imgGray, result[0], result[1])
        imgBlur = cv2.GaussianBlur(imgGray, (result[2], result[2]), 0, 0)
        imgCan = cv2.Canny(imgBlur, result[0], result[1])
        cv2.imshow('img', img)
        cv2.imshow('imgThresold', imgCan)
        if cv2.waitKey(FPS) == ord('q'):
            break


if __name__ == "__main__":
    Find_Parameter(False, ImagePath) # -> (True:輸入影片/False:輸入照片 , 影片/照片路徑)
    #Find_Parameter(True, VideoPath)
