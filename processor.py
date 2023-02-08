import os, cv2
import pytesseract

class PlateProcessor:
  def __init__(self, imgpath: str) -> None:
    self._recognized = []
    if os.path.exists(imgpath):
      self._imgpath = os.path.abspath(imgpath)
      try:
      # set tessract environment
        self._setTessEnv()
        self._setLang()
      except Exception as e:
        print("Exception while reading image: {}".format(e))
        exit(1)
      except RuntimeError as e:
        print("RuntimeError while reading image: {}".format(e))
        exit(1)
      except pytesseract.TesseractError as e:
        print("Error while setting tesseract: {}".format(e))
        exit(1)
    else:
      raise Exception("Error: image path does not exist!")
      
  def _setTessEnv(self) -> None:
    self._tessdata_dir_config = "--tessdata-dir " + os.getcwd() + "/tessdata"
    self._tessdata_bin = os.getcwd() + "/tesseract-5.3.0/build/bin/tesseract"
    pytesseract.pytesseract.tesseract_cmd = self._tessdata_bin
    os.environ["TESSDATA_PREFIX"] = os.getcwd() + "/tessdata"
  
  def _setLang(self) -> None:
    # TODO auto detect language
    self._lang = "eng"
  
  def _readImg(self) -> None:
    try:
      # read image and convert to gray image
      self._img = cv2.imread(self._imgpath)
      self._imgray = cv2.cvtColor(self._img, cv2.COLOR_BGR2GRAY)
    except Exception as e:
      print("Image file is invalid: {}".format(e))
  
  def _filterImg(self) -> None:
    pass
  
  def _thresholdImage(self) -> None:
    # get thresholded image
    ret, thresh = cv2.threshold(self._imgray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    self._ret = ret
    self._thresh = thresh
  
  def _filterThreshold(self) -> None:
    pass
  
  def _dilateThresholdedImage(self) -> None:
    # Specify structure shape and kernel size
    # TODO auto selection of kernel size
    kernel_size = 10
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
  
    self._img2detect = cv2.dilate(self._thresh, kernel, iterations = 1)
  
  def preprocess(self) -> None:
    self._readImg()
    self._filterImg()
    self._thresholdImage()
    self._filterThreshold()
    self._dilateThresholdedImage()
    
  def image2text(self) -> None:
    img2 = self._img.copy()
    
    # Find contours
    contours, hierarchy = cv2.findContours(self._img2detect, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # Looping through the identified contours
    # Then rectangular part is cropped and passed on
    # to pytesseract for extracting text from it
    # Extracted text is then appended on the text
    
    counter = 1
    for cnt in contours:
      # get a rectangle of detected bounds
      x, y, w, h = cv2.boundingRect(cnt)
      
      # Cropping the text block for giving input to OCR
      cropped = img2[y:y + h, x:x + w]
      
      # to be deleted
      #cv2.imwrite(f"result/token_{counter}.png", cropped)
      counter += 1
      
      # Apply OCR on the cropped image
      result_txt = pytesseract.image_to_string(cropped, config=self._tessdata_dir_config)
      self._recognized.append(result_txt)
  
  def getRecognizedList(self) -> list:
    return self._recognized

if __name__ == '__main__':
  proc = PlateProcessor("data/test4.jpg")
  proc.preprocess()
  proc.image2text()
  print(proc.getRecognizedList())