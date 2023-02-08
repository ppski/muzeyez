#!/bin/bash
link="https://github.com/tesseract-ocr/tesseract/archive/refs/tags/"
version="5.3.0"
postfix=".tar.gz"
tarballname="tesseract-""${version}""${postfix}"

# Download, unzip
wget -c -O "${tarballname}" "${link}${version}${postfix}"
tar -xzf "${tarballname}"
rm "${tarballname}"
cd "tesseract-""${version}"

# Create build directory
mkdir build && cd build

# Build the source
cmake ..
make -j8
