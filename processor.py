import os

import cv2
import pytesseract

import numpy as np

from processor_generic import ProcessorGeneric


class PlateProcessor(ProcessorGeneric):
    def __init__(self, imgpath: str):
        super().__init__(imgpath)

    def dilate_threshold_image(self) -> None:
        # Specify structure shape and kernel size
        # TODO auto selection of kernel size
        kernel_size = 10
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
        self._img2detect = cv2.dilate(self._thresh, kernel, iterations=1)

    def image2text(self) -> None:
        img2 = self._img.copy()

        # Find contours
        contours, hierarchy = cv2.findContours(
            self._img2detect, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
        )
        # Looping through the identified contours
        # Then rectangular part is cropped and passed on
        # to pytesseract for extracting text from it
        # Extracted text is then appended on the text

        counter = 1
        for cnt in contours:
            # get a rectangle of detected bounds
            x, y, w, h = cv2.boundingRect(cnt)

            # Cropping the text block for giving input to OCR
            cropped = img2[y : y + h, x : x + w]

            # to be deleted
            # cv2.imwrite(f"result/token_{counter}.png", cropped)
            counter += 1

            # Apply OCR on the cropped image
            result_txt = pytesseract.image_to_string(
                cropped, config=self._tessdata_dir_config
            )
            self._recognized.append(result_txt)

    def get_recognized_list(self) -> list:
        return self._recognized


if __name__ == "__main__":
    path = os.path.abspath(".")
    test_image = f"data/1_klee.jpeg"
    proc = PlateProcessor(test_image)
    proc.prepare()
    proc.dilate_threshold_image()
    proc.image2text()
    print(proc.getRecognizedList())
