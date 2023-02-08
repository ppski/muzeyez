import os, cv2

"""
Task:
  - Implement generic class for image processor
  - Refactor PlateProcessor and PreProcessor classes with this new generic class

Hint:
  - the process flow is generic: 
      init -> read image -> filter image -> threshold image -> filter thresholded image -> detect
              ----------------------------  prepare ---------------------------       --- run ---
  
  - some methods can be generic too, e.g. readImage
  - don't need to write prepare() and detect() in child classes, write them in parent class (this one)
"""

class ProcessorGeneric:
  def __init__(self, imagepath: str) -> None:
    pass
  
  def _readImage(self) -> None:
    pass

  def _filterImage(self) -> None:
    pass
  
  def _threshImage(self) -> None:
    pass
  
  def _filterThreshold(self) -> None:
    pass
  
  def prepare(self) -> None:
    self._readImage()
    self._filterImage()
    self._threshImage()
    self._filterThreshold()
  
  def detect(self, func=NotImplemented) -> None:
    func()
  
  def __do_nothing(self) -> None:
    pass
  
  def test(self):
    self.prepare()
    self.detect(func=self.__do_nothing)
