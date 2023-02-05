import os

import cv2
import numpy as np

class Preprocessor:
  def __init__(self, imagepath: str) -> None:
    if os.path.exists(imagepath):
      self._imagepath = os.path.abspath(imagepath)
    else:
      raise RuntimeError("Error: image does not exist")
  
  def _readImage(self) -> None:
    try:
      self._img = cv2.imread(self._imagepath)
      self._imgray = cv2.cvtColor(self._img, cv2.COLOR_BGR2GRAY)
    except RuntimeError as e:
      print("Error: {}".format(e))
  
  def _filterImage(self) -> None:
    """To clean noise"""
    pass
  
  def _thresholdImage(self) -> None:
    #TODO auto choose value of parameter
    ret, thresh = cv2.threshold(self._imgray, 50, 255, 0)
    self._th_ret = ret
    self._th_thresh = thresh

  def preprocess(self) -> None:
    self._readImage()
    self._filterImage()
    self._thresholdImage()
  
  def detect_rectangle(self) -> list: #list of tuples
    #TODO auto choose value of parameter
    contours, hierarchy = cv2.findContours(self._th_thresh, 1, 2)
    
    result = []
    for cnt in contours:
      approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
      if len(approx) == 4:
        x, y, w, h = cv2.boundingRect(cnt)
        result.append((x, y, w, h))
    
    return result

  def test(self):
    self.preprocess()
    img2 = self._img
    for rect in self.detect_rectangle():
      x,y,w,h = rect
      img2 = cv2.rectangle(img2, (x,y), (x+h,y+h), (255, 0, 0), 2)
    
    cv2.imwrite("rectangles.png", img2)

