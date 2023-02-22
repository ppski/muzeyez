import os

import cv2
import pytesseract

import numpy as np


class ProcessorGeneric:
    def __init__(self, imgpath: str) -> None:
        self._recognized = []
        if os.path.exists(imgpath):
            self._imgpath = os.path.abspath(imgpath)
            try:
                # set tessract environment
                self._set_tess_env()
                self._set_lang()
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

    def _set_lang(self) -> None:
        self._lang = "eng"

    def _set_tess_env(self) -> None:
        self._tessdata_dir_config = "--tessdata-dir " + os.getcwd() + "/tessdata"
        print(self._tessdata_dir_config)
        self._tessdata_bin = os.getcwd() + "/tesseract-5.3.0/build/bin/tesseract"
        pytesseract.pytesseract.tesseract_cmd = self._tessdata_bin
        os.environ["TESSDATA_PREFIX"] = os.getcwd() + "/tessdata"

    def read_image(self) -> None:
        """Read image from file"""
        try:
            self._img = cv2.imread(self._imgpath)
            self._imgray = cv2.cvtColor(self._img, cv2.COLOR_BGR2GRAY)
        except Exception as e:
            print("Image file is invalid: {}".format(e))

    def filter_image(self) -> None:
        """To clean noise"""
        kernel = np.ones((7, 7), np.float32) / 25
        self._imgray = cv2.filter2D(self._imgray, -1, kernel)

    def threshold_image(self) -> None:
        # get thresholded image
        ret, thresh = cv2.threshold(
            self._imgray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV
        )
        self._ret = ret
        self._thresh = thresh

    def filter_threshold(self) -> None:
        pass

    def prepare(self) -> None:
        self.read_image()
        self.filter_image()
        self.threshold_image()
        self.filter_threshold()

    def detect(self, func=NotImplemented) -> None:
        func()

    def __do_nothing(self) -> None:
        pass

    def test(self):
        self.prepare()
        self.detect(func=self.__do_nothing)


if __name__ == "__main__":
    test_image = "data/1_klee.jpeg"
    proc = ProcessorGeneric(test_image)
    print(proc.test())
