import os

os.system("rm tessdata/*")

link = "https://raw.githubusercontent.com/tesseract-ocr/tessdata/main/"

datalist = ["eng.traineddata",
            "fra.traineddata"]

for d in datalist:
  cmd = "wget -c -O " + d + " " + link + d
  os.system(cmd)
  os.system("mv " + d + " tessdata/")
  