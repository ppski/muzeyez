import os

import cv2
import pytesseract

import numpy as np

from processor_generic import ProcessorGeneric


class Preprocessor(ProcessorGeneric):
    def __init__(self, imgpath: str):
        super().__init__(imgpath)

    def threshold_image(self) -> None:
        # TODO: Update smart parameter choosing.
        # ret, thresh = cv2.threshold(self._imgray,50,255,0)
        thresh = cv2.adaptiveThreshold(
            self._imgray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        # self._th_ret = ret #TODO: Delete?
        self._th_thresh = thresh

    def detect_rectangle(self) -> list:  # list of tuples
        # TODO auto choose value of parameter
        contours, hierarchy = cv2.findContours(self._th_thresh, 1, 2)

        result = []
        for cnt in contours:
            # x1, y1 = cnt[0][0]
            approx = cv2.approxPolyDP(
                cnt, 0.01 * cv2.arcLength(cnt, True), True
            )  # detects poly
            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(cnt)
                result.append((x, y, w, h))
        return result

    def test(self):
        self.prepare()
        cv2.imwrite("threshold.png", self._th_thresh)
        img2 = self._img
        for rect in self.detect_rectangle():
            x, y, w, h = rect
            img2 = cv2.rectangle(img2, (x, y), (x + h, y + h), (255, 0, 0), 2)
        cv2.imwrite("rectangles.png", img2)


if __name__ == "__main__":
    p = Preprocessor("data/1_klee.jpeg")
    p.test()
