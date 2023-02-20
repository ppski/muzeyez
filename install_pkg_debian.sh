#!/bin/bash
apt update -y
apt upgrade -y

apt install -y build-essential
apt install -y python3 python-is-python3
apt install -y python3-opencv
apt install -y wget curl
apt install -y cmake pkg-config
apt install -y leptonica-progs libleptonica-dev libicu-dev libidn11-dev libpango1.0-dev libcairo2-dev libcurl4-openssl-dev libarchive-dev libcurlpp-dev libssh2-1-dev libssl-dev